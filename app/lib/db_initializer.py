import ast
from pymongo import MongoClient
import mediapipe as mp
import cv2
import os

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

              "default": True, #tell if the sign can be deleted of not, in this function we store base sign so : TRUE
              
              "command": ""} #command key : empty for now
      
      models = db.models #load the cursor on our "table"
      models.insert_one(hand_to_post).inserted_id #insert the current hand datas in the DB under "models"
      
  return True  
      
def extract_head(): #Function that get the header of our base signs
  letters = ['A',"B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  extracted = []
  models = db.models
  datas = models.find() #retrieve a cursor on all the DB
  for x in letters: #We will loop over all the base groupnames
    strtemp = ('%s "%s"' %('this.groupname ==',x)) #the Query we will use on the DB (equivalent to SQL -> WHERE "Conditons")
    groupname_head = datas.limit(1).where(strtemp) #we search for the first skeleton that belong to the current groupname
    extracted.append(dict(list(groupname_head)[0]))
    groupname_head.rewind() #empty the result cursor for the next query 
    #print("Affiche un truc bordel : ",extracted,"\n")
  return extracted
    
    
