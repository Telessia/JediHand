import time
from pymongo import MongoClient
import os
import numpy as np

from definitivefunctionssign import *
from function_test import *


path_app_v2 = 'app/static/default_datas/train/' #Path of the images to load

files = os.listdir(path_app_v2)

#Connection to running database
client = MongoClient('localhost', 27017, username='root', password='root')
db = client['jedihand_development'] #name of the database, see docker-compose


labels_skeleton = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

models = db.models
models_test = db.models_test

dict_skel = {}
dict_rev = {}
dict_bent = {}
dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, 1)


#functionTestPrecisionVersion2(0.68, models_test, dict_skel, dict_rev, dict_bent)
functionTestVersion2Camera(0.7, dict_skel, dict_rev, dict_bent)


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


