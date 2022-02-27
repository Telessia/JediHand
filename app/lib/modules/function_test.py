# Set of function to test precision, test camera

import time
import cv2
import mediapipe as mp
from detection import processImageVersion1

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
path_apprentissage = "app/lib/modules/image/apprentissage/"


# Function to test the precision of the version 1
def functionTestPrecisionVersion1(minDetectConfidence, minTrackingConfidence, labels, dictionary):

    sommeGoodPredictions = 0.0 #Compteur de bonne réponse
    totalPredictions = 0 #Total de réponses prédites, des fois il n'y a pas de skeleton avec mediapipe

    nb_iteration = 1
    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=1,
        min_detection_confidence=minDetectConfidence, min_tracking_confidence=minTrackingConfidence
        ) as hands:

        sumTime = 0.0
        for i in range(len(labels)):
            #Récupération de l'image
            image = cv2.imread(path_apprentissage + labels[i] + ".jpg")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            for _ in range(nb_iteration):
                start = time.perf_counter() # start of the timer

                #Récupération du skeleton de l'image
                skeletonTest = hands.process(image)
                
                #Pas de problème de détection
                if(skeletonTest.multi_hand_landmarks != None):
                    
                    predictedLabel = processImageVersion1(skeletonTest.multi_hand_landmarks)

                    if(predictedLabel == dictionary[labels[i][0]]):
                        sommeGoodPredictions += 1
                    
                    totalPredictions += 1

                end = time.perf_counter() # end of the timer
                sumTime += end - start # get the time execution

        #print(sumTime * 1000 / totalPredictions)
        
    #print(totalPredictions / nb_iteration)
    print("Good Predictions : ", sommeGoodPredictions, "  Total Predictions : ", totalPredictions)
    print("Precision de l'algorithme : ", (sommeGoodPredictions / totalPredictions) * 100, "%\n\n")


# Function to test the precision of the version 1 with camera
def functionTestVersion1Camera(valueOfMinTracking):
    i = 0
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.67,
        min_tracking_confidence=valueOfMinTracking) as hands:
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
            results = hands.process(image)

            i += 1
            if(i == 30):
                if results.multi_hand_landmarks:
                    print(processImageVersion1(results.multi_hand_landmarks))
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
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()