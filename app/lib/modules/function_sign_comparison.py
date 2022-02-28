# Set of functions that allow the comparison of two skeletons

import numpy as np
from computefunction import *


# Function that returns whether the thumb is bent or not
def computeBentThumbV2(landmark):

    bool_bent_thumb = True # boolean that indicates if the thumb is bent
    distanceF = distanceMinkowski(landmark[2], landmark[4])
    distanceS1 = distanceMinkowski(landmark[2], landmark[3]) 
    distanceS2 = distanceMinkowski(landmark[3], landmark[4])
    
    # if the points of the thumb are aligned in the same axis then it is not bent
    if (distanceF > 0.95 * (distanceS1 + distanceS2)): bool_bent_thumb = False

    return bool_bent_thumb


# Function that returns the boolean to determine if the skeleton of the hand passed in parameter is upside down
# and if the fingers are bent
def constructReverseAndBentFingers(skeleton):

    bool_vertical = computeIsHandVertical(skeleton)
    
    # boolean that indicates if the hand is reversed vertically
    bool_reverse_hand_verti = skeleton[0][1] < skeleton[1][1] and skeleton[0][1] < skeleton[17][1]
     # boolean that indicates if the hand is reversed horizontally
    bool_reverse_hand_horiz = skeleton[0][0] < skeleton[1][0] and skeleton[0][0] < skeleton[17][0]

    bool_hands = [bool_vertical, bool_reverse_hand_verti, bool_reverse_hand_horiz]

    tab_bent_fingers = []
    tab_bent_fingers.append(computeBentThumbV2(skeleton))

    if bool_vertical: # hand is vertically aligned

        limite_hand = [skeleton[6][1], skeleton[10][1], skeleton[14][1], skeleton[18][1]]
        bool_reverse_hand_verti = skeleton[0][1] < skeleton[4][1] 

        for i in range(4):
            #Detection of raised fingers
            bool_bent_finger = skeleton[8 + 4 * i][1] > limite_hand[i]
            tab_bent_fingers.append(not bool_bent_finger if bool_reverse_hand_verti else bool_bent_finger)
    else: # hand is horizontally aligned

        limite_hand = [skeleton[6][0], skeleton[10][0], skeleton[14][0], skeleton[18][0]]
        
        for i in range(4):
            #Detection of raised fingers
            bool_bent_finger = skeleton[8 + 4 * i][0] > limite_hand[i]
            tab_bent_fingers.append(not bool_bent_finger if bool_reverse_hand_horiz else bool_bent_finger)


    return bool_hands, tab_bent_fingers


# Function that returns the arrays of booleans and bent fingers of skeletons in the passed skeleton array
# in parameter
def constructTabReverseAndBentFingers(tab_skeletons):
    
    tab_reverse = []
    tab_bent_fingers = []

    for skeleton in tab_skeletons:
        bool_reverse, bent_fingers = constructReverseAndBentFingers(skeleton)
        tab_reverse.append(bool_reverse)
        tab_bent_fingers.append(bent_fingers)
    
    return tab_reverse, tab_bent_fingers


# Function that returns 3 dictionaries: for the skeleton, for the inverted hand, for the bent fingers
def constructBaseImages(models, labels_image, number_images):

    dictionary_skeletons = {}
    dictionary_reverse_hand = {}
    dictionary_bent_fingers = {}

    value_to_get = len(labels_image) * number_images

    for image_name in labels_image: # creation of dictionaries
        dictionary_skeletons[image_name] = []
        dictionary_reverse_hand[image_name] = []
        dictionary_bent_fingers[image_name] = []

    datas = models.find() # recovery of the cursor on the data of the database
    for data in datas:
        
        if(value_to_get == 0): break

        if(len(dictionary_skeletons[data['groupname']]) < number_images):
            value_to_get -= 1
            tab_tempo = np.multiply(data['skeleton'], 100)
            bool_reverse, bent_fingers = constructReverseAndBentFingers(tab_tempo)

            dictionary_skeletons[data['groupname']].append(tab_tempo)
            dictionary_reverse_hand[data['groupname']].append(bool_reverse)
            dictionary_bent_fingers[data['groupname']].append(bent_fingers)

    return dictionary_skeletons, dictionary_reverse_hand, dictionary_bent_fingers


# Function that returns the Minkowski distance between two 3D points p1 and p2
def distanceMinkowski(p1, p2):
    distance = pow(
        (pow(abs(p2[0] - p1[0]), 3) 
        + pow(abs(p2[1] - p1[1]), 3) 
        + pow(abs(p2[2] - p1[2]), 3)), 1/3
    )
    return distance


# Function that returns the array of distances between the points of the fingers
def getTabDistanceAllFingers(skeleton):
    tab_distance_fingers = []

    # distance base, hand point for each hand point
    for i in range (1,21):
        tab_distance_fingers.append(distanceMinkowski(skeleton[0], skeleton[i]))
    
    # distance fingertip, other fingertip for each finger
    for i in range (1, 5):
        for j in range (i + 1, 6):
            tab_distance_fingers.append(distanceMinkowski(skeleton[i * 4], skeleton[j * 4]))
    #This part improves the accuracy from 49% to 63%.
    return tab_distance_fingers


# Function that returns the cumulative distance between two skeletons
def compareSkeletons(tab_dist_skeleton1, tab_dist_skeleton2):
    sommeDistance = 0
    for i in range(len(tab_dist_skeleton1)):
        sommeDistance += abs(tab_dist_skeleton1[i] - tab_dist_skeleton2[i])
    return sommeDistance


# Function that returns the label of the closest sign in the list of basic signs
def getLabelClosestSkeleton(skeleton, dictionary_skeleton, dictionary_reverse, dictionary_bent_fingers):

    labels_skeleton = list(dictionary_skeleton.keys())

    distance_normal_skeleton = distanceMinkowski(skeleton[0], skeleton[17])
    tab_distance_skeleton = getTabDistanceAllFingers(skeleton)
    bool_reverse, bent_fingers = constructReverseAndBentFingers(skeleton)

    value_similarity = []
    for label in labels_skeleton:
        
        values_similar = []

        for i in range(len(dictionary_skeleton[label])):
            
            skeleton_tempo = dictionary_skeleton[label][i]
            distance_normal_tempo = distanceMinkowski(skeleton_tempo[0], skeleton_tempo[17])
            tauxM_multiplication = distance_normal_skeleton / distance_normal_tempo
            tab_points_tempo_normalized = np.multiply(skeleton_tempo, tauxM_multiplication)
            tab_distance_tempo = getTabDistanceAllFingers(tab_points_tempo_normalized)

            # the distance between each finger is recovered
            value_similar = compareSkeletons(tab_distance_skeleton, tab_distance_tempo)


            # we add a penalty for each direction that are not identical
            for j in range(len(dictionary_reverse[label][i])):
                if(bool_reverse[j] != dictionary_reverse[label][i][j]):
                    value_similar += 30

            # a penalty is added for each finger that is not bent in the same direction
            for j in range(len(dictionary_bent_fingers[label][i])):
                if(bent_fingers[j] != dictionary_bent_fingers[label][i][j]):
                    value_similar += 30
            
            values_similar.append(value_similar)

        value_similarity.append(np.min(values_similar))

    # we get the label of the most similar skeleton
    return labels_skeleton[np.argmin(value_similarity)]


