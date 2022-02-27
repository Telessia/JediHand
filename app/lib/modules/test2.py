import time
from pymongo import MongoClient
import os
import numpy as np

from definitivefunctionssign import *


path = 'app/static/default_datas/train/' #Path of the images to load

files = os.listdir(path)

print("Debut !")

#Connection to running database
client = MongoClient('localhost', 27017, username='root', password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

print("Test ?")



#labels_skeleton = ["C", "D"]
labels_skeleton = ['A',"B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def extract_skeletons(labels, number_image): #Function that get the header of our base signs
  #letters = ['A',"B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  
  dictionary_skeletons = {}
  value_to_get = len(labels) * number_image
  print("Value : ", value_to_get)

  for image_name in labels: # create the dictionary
    dictionary_skeletons[image_name] = []

  models = db.models
  datas = models.find() #retrieve a cursor on all the DB
  for data in datas:
    
    if(value_to_get == 0): break

    #print(data['groupname'])
    if(len(dictionary_skeletons[data['groupname']]) < number_image):
      value_to_get -= 1
      tabTempo = np.multiply(data['skeleton'], 100)
      dictionary_skeletons[data['groupname']].append(tabTempo)


  return dictionary_skeletons


models = db.models
models_test = db.models_test

dict_skel = {}
dict_rev = {}
dict_bent = {}
dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, 30)



#for l in dict_skel.keys():
#  getLabelClosestSkeleton(dict_skel[l][0], dict_skel, dict_rev, dict_bent)

#functionTestPrecisionVersion2(0.68, models_test, dict_skel, dict_rev, dict_bent)

"""for i in range (19):
    print(0.05 + i*0.01)
    dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, 1)
    functionTestPrecisionVersion2(0.05 + i*0.01, models_test, dict_skel, dict_rev, dict_bent)"""

"""for i in range (2, 31,2):
    #print(0.05 + i*0.01)
    print(i)
    dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, i)
    start = time.perf_counter() # start of the timer
    functionTestPrecisionVersion2(0.68, models_test, dict_skel, dict_rev, dict_bent)
    end = time.perf_counter() # end of the timer
    print((end - start), " s !")"""

#dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, 30)
#functionTestPrecisionVersion2(0.68, models_test, dict_skel, dict_rev, dict_bent)

#print(constructTabReverseAndBentFingers(dict_skel['A']))
#print(len(dict_skel['B']))
#for x in dict_skel:
#  print(len(dict_skel[x]))
#print(np.sum(get_number_images(labels_skeleton)))



dict_test = { "A": [1 , 4], "B": [2, -1], "C": [3, 7] }
val_min = []
for v in dict_test:
  val_min.append(np.min(dict_test[v]))

#print(list(dict_test.keys())[np.argmin(val_min)])


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

minTrackingConfidence = 0.9

i = 0
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.68,
    min_tracking_confidence=minTrackingConfidence) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    start = time.perf_counter()
    results = hands.process(image)

    i += 1
    if(i == 45):

      if results.multi_hand_landmarks:

          #Récupération du tableau de points du skeleton
          skeleton = copyOfTabSkeletons(results.multi_hand_landmarks[0].landmark)
          skeleton = np.multiply(skeleton, 100)
          predicted_label = getLabelClosestSkeleton(skeleton, dict_skel, dict_rev, dict_bent)
          print(predicted_label)

          end = time.perf_counter()
          print("Temps : ", end-start, " s")

      i = 0



    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)#cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()


