#Set of predefined functions to calculate values
from math import sqrt

# Function that returns a copy of an array of points by removing the attributes
def copyOfTabSkeletons(tab_skeleton):
    tabReturn = []
    for tabP in tab_skeleton:
        tabT = []
        tabT.append(tabP.x)
        tabT.append(tabP.y)
        tabT.append(tabP.z)
        tabReturn.append(tabT)
    return tabReturn


# Function that returns whether the thumb is bent or not
def computeBentThumb(landmark):

    bool_bent_thumb = True # boolean that indicates if the thumb is bent
    distanceF = distanceEuclidean(landmark[2], landmark[4])
    distanceS1 = distanceEuclidean(landmark[2], landmark[3]) 
    distanceS2 = distanceEuclidean(landmark[3], landmark[4])
    
    # if the points of the thumb are aligned in the same axis then it is not bent
    if (distanceF > 0.95 * (distanceS1 + distanceS2)): bool_bent_thumb = False

    return bool_bent_thumb


# Function that returns whether the thumb should be counted as a raised finger even if it is not bent
def computeBentThumbVersion1(landmark, bool_vertical):

    bool_bent_thumb = False
    if bool_vertical: # hand is vertically aligned

        # allows to know if the hand is oriented in one direction or the other
        orientation = landmark[5][0] < landmark[17][0]
        # thumb bend value is calculated according to the orientation of the hand
        bool_bent_thumb = landmark[4][0] < landmark[5][0]
            
    else:
        orientation = landmark[5][1] < landmark[17][1]
        bool_bent_thumb = landmark[4][1] < landmark[5][1]
        
    if (orientation): bool_bent_thumb = not bool_bent_thumb
    return bool_bent_thumb


# Function that returns whether the fingers of the hand are bent or not
def computeBentFingers(landmark, bool_vertical):

    tab_bent_fingers = []
    if bool_vertical: # hand is vertically aligned

        limite_hand = [landmark[6][1], landmark[10][1], landmark[14][1], landmark[18][1]]
        bool_reverse_hand_verti = landmark[0][1] < landmark[4][1] # boolean that indicates if the hand is reversed

        for i in range(4):
            #Detection of raised fingers
            bool_bent_finger = landmark[8 + 4 * i][1] > limite_hand[i]
            tab_bent_fingers.append(not bool_bent_finger if bool_reverse_hand_verti else bool_bent_finger)
    else: # hand is horizontally aligned

        limite_hand = [landmark[6][0], landmark[10][0], landmark[14][0], landmark[18][0]]
        bool_reverse_hand_horiz = landmark[0][0] < landmark[4][0] # boolean that indicates if the hand is reversed
        
        for i in range(4):
            #Detection of raised fingers
            bool_bent_finger = landmark[8 + 4 * i][0] > limite_hand[i]
            tab_bent_fingers.append(not bool_bent_finger if bool_reverse_hand_horiz else bool_bent_finger)

    return tab_bent_fingers


# Function that returns the verticality of the hand
def computeIsHandVertical(landmark):
    bool_vertical = False # boolean indicating if the hand is vertical
    distX = abs(landmark[0][0] - landmark[9][0])
    distY = abs(landmark[0][1] - landmark[9][1])
    if(distX < distY): bool_vertical = True # if distance x is inferior to distance y then the hand is vertically aligned

    return bool_vertical


#Function which return the numbers of fingers raised, omitting the thumb
def computeRaisedFingers(landmark):

    # [ calculation of whether the hand is vertical ]
    bool_vertical = computeIsHandVertical(landmark)
    
    # [ calculation of the bent thumb ]
    bool_bent_thumb = computeBentThumb(landmark)
    if not bool_bent_thumb:
        bool_bent_thumb = computeBentThumbVersion1(landmark, bool_vertical)
    
    # [ calculation of the bent fingers ]
    tab_bent_fingers = computeBentFingers(landmark, bool_vertical)
  
    counter_thumb = 0
    # if the thumber is not bent  
    if(not bool_bent_thumb):
      counter_thumb = 1

    #Return the count of fingers that are NOT bent + if the thumb is raise
    return tab_bent_fingers.count(False) + counter_thumb


# Function that returns the Euclidean distance between two points
def distanceEuclidean(point1, point2):
    distance = sqrt(
        pow(point2[0] - point1[0], 2) 
        + pow(point2[1] - point1[1], 2))
    return distance