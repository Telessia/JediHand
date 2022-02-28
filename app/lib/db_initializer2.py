from modules.computefunction import copyOfTabSkeletons
from pymongo import MongoClient

import mediapipe as mp
import cv2
import os

path = 'app/static/default_datas/test/' #Path of the images to load

files = os.listdir(path)

#Connection to running database
client = MongoClient('localhost', 27017,
                     username='root',
                 password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

mp_hands = mp.solutions.hands

#Function that try to Initialize the DB with default commands (if empty)
def initCollectionTest():
  
  if 'models_test' in db.list_collection_names(): #models is the name of the object collection in our database
    print("\nAlready Initialized\n")
    return False #if the DB is not empty we skip the initialization

  with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=1,
      min_detection_confidence=0.68) as hands:
    for _, file in enumerate(files):
        
      image = cv2.imread(path + file)
      image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      # Convert the BGR image to RGB before processing.
      results = hands.process(image)
      
      if not results.multi_hand_landmarks:
          continue
      
      #getting the skeleton container for the current sign
      skeleton_to_store = results.multi_hand_landmarks[0].landmark
      skeleton_to_store = copyOfTabSkeletons(skeleton_to_store) #convert the skeleton (type : google.protobuf etc..) to an array of floats
      
      hand_to_post = {
          
              "groupname": file[0] , #groupname to identify to which sign the picture/skeleton belongs

              "picpath": "static/default_datas/test/"+file, #path to the picture of the sign

              "skeleton": skeleton_to_store, #skeleton of the sign (list of lists of floats)
              }
      
      models_test = db.models_test #load the cursor on our "table"
      models_test.insert_one(hand_to_post).inserted_id #insert the current hand datas in the DB under "models"
      
  return True

initCollectionTest()