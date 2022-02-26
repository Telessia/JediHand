import ast
import shutil
from tokenize import group
from pymongo import MongoClient
import mediapipe as mp
import cv2
import os
from datetime import datetime

path = 'app/static/default_datas/train/' #Path of the images to load

files = os.listdir(path)

#Connection to running database
client = MongoClient('localhost', 27017,
                     username='root',
                 password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

mp_hands = mp.solutions.hands

def copyOfTabSkeletons(tabSkeleton):
    tabReturn = []
    for tabP in tabSkeleton:
        tabT = []
        tabT.append(tabP.x)
        tabT.append(tabP.y)
        tabT.append(tabP.z)
        tabReturn.append(tabT)
    return tabReturn

#Function that try to Initialize the DB with default commands (if empty)
def init():
  
  if 'models' in db.list_collection_names(): #models is the name of the object collection in our database
    print("\nAlready Initialized\n")
    return False #if the DB is not empty we skip the initialization

  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(files):
        
      #print("File name :", path+file,"\n")
      image = cv2.flip(cv2.imread(path+file), 1)
      # Convert the BGR image to RGB before processing.
      results = hands.process(image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      
      if not results.multi_hand_landmarks:
          continue
      
      #getting the skeleton container for the current sign
      skeleton_to_store = results.multi_hand_landmarks[0].landmark
      skeleton_to_store = copyOfTabSkeletons(skeleton_to_store) #convert the skeleton (type : google.protobuf etc..) to an array of floats
      
      hand_to_post = {
          
              "groupname": file[0] , #groupname to identify to which sign the picture/skeleton belongs

              "picpath": "static/default_datas/train/"+file, #path to the picture of the sign

              "skeleton": skeleton_to_store, #skeleton of the sign (list of lists of floats)

              "default": True, #tell if the sign canno't be deleted or not, in this function we store default sign so : TRUE
              
              "command": ""} #command key : empty for now
      
      models = db.models #load the cursor on our "table"
      models.insert_one(hand_to_post).inserted_id #insert the current hand datas in the DB under "models"
      
  return True  

def extract_head(): #Function that get the header of our base signs
  extracted = []
  models = db.models
  groupbase = models.distinct("groupname")
  print(groupbase)
  for x in groupbase: #We will loop over all the base groupnames
    result = models.find_one({"groupname": x })
    #print(result['_id'])
    extracted.append(result)
  return extracted

def insert_sign(groupname,original_path,skeleton):
  try:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    new_path = "static/user_datas/"+groupname+dt_string+".jpg"
    shutil.move("app/"+original_path,"app/"+new_path)
  except FileNotFoundError:
    return False
  hand_to_post = {
          
              "groupname": groupname , #groupname to identify to which sign the picture/skeleton belongs

              "picpath": new_path, #path to the picture of the sign

              "skeleton": skeleton, #skeleton of the sign (list of lists of floats)

              "default": False, #tell if the sign canno't be deleted or not
              
              "command": ""} #command key : empty for now
      
  models = db.models #load the cursor on our "table"
  models.insert_one(hand_to_post).inserted_id #insert the current hand datas in the DB under "models"  
  return True
    
    
def update_commands(listIds, listCommands):
  models = db.models
  for idx,x in enumerate(listIds):
    print(x)
    print(listCommands[idx])
    models.update_one({ '_id' : x }, {"$set": { 'command' : str(listCommands[idx]) }}, upsert = False)
    print("updated")
  return
    
