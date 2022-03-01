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
        