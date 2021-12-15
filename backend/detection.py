import mediapipe as mp
import cv2
import actions

mp_hands = mp.solutions.hands

def process_image(image):
    # For static images:
    with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.5) as hands:
      image = cv2.flip(image, 1)
      results = hands.process(image)

      ## Print handedness and draw hand landmarks on the image.
      print('Handedness:', results.multi_handedness)
      if not results.multi_hand_landmarks:
        print("error")
        return -1
      for hand_landmarks in results.multi_hand_landmarks:
        digittab = [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP], hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]
        corehandlimits = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y)
        count = 0
        raisedfingers = 0
        for finger in digittab:
          #coords reverted?
          if finger.y > corehandlimits[3]:
            count = count+1
            
        raisedfingers = 5 - count
        print("Number of fingers" , raisedfingers)
          
        return raisedfingers
        