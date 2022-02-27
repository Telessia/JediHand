#Functions that return the correct sign according to the project versions

from computefunction import *

# Function that returns the number of raised fingers from version 1
def processImageVersion1(res_multi_hand):

    counter_raised_fingers = 0
    # for each hand
    for hand_landmarks in res_multi_hand:
        #add the number of finger raised
        landmark = copyOfTabSkeletons(hand_landmarks.landmark)
        counter_raised_fingers += computeRaisedFingers(landmark)

    return counter_raised_fingers


"""def process_image_version1b(image):
    # For static images:
    with mp_hands.Hands(
      static_image_mode=True,
      max_num_hands=2,
      min_detection_confidence=0.7) as hands:
        #image = cv2.flip(image, 1)
        results = hands.process(image)

        ## Print handedness and draw hand landmarks on the image.
        #('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
          print("error")
          return -1
        
        counterRaisedFingers = 0
        # for each hand
        for hand_landmarks in results.multi_hand_landmarks:
          # add the number of finger raised
          counterRaisedFingers += compute_raised_fingers(hand_landmarks.landmark)
        return counterRaisedFingers"""
        