import numpy as np
import cv2
import mediapipe as mp
from math import sqrt

import time

from computefunction import *

mp_hands = mp.solutions.hands


# Function that returns whether the thumb is bent or not
def computeBentThumbV2(landmark):

    bool_bent_thumb = True # boolean that indicates if the thumb is bent
    distanceF = distanceMinkowski(landmark[2], landmark[4])
    distanceS1 = distanceMinkowski(landmark[2], landmark[3]) 
    distanceS2 = distanceMinkowski(landmark[3], landmark[4])
    
    # if the points of the thumb are aligned in the same axis then it is not bent
    if (distanceF > 0.95 * (distanceS1 + distanceS2)): bool_bent_thumb = False

    return bool_bent_thumb


# Fonction qui retourne le booléen pour déterminer si le skeleton de la main passé en paramètre est à l'envers
# et si les doigts sont pliés
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


# Fonction qui retourne les tableaux des booléens et des doigts pliés des skeletons dans le tableau de skeleton passé
# en paramètre
def constructTabReverseAndBentFingers(tab_skeletons):
    
    tab_reverse = []
    tab_bent_fingers = []

    for skeleton in tab_skeletons:
        bool_reverse, bent_fingers = constructReverseAndBentFingers(skeleton)
        tab_reverse.append(bool_reverse)
        tab_bent_fingers.append(bent_fingers)
    
    return tab_reverse, tab_bent_fingers


# Fonction qui retourne 3 dictionnaires : pour le skeleton, pour la main inversé, pour les doigts pliés
def constructBaseImages(models, labels_image, number_images):

    dictionary_skeletons = {}
    dictionary_reverse_hand = {}
    dictionary_bent_fingers = {}

    value_to_get = len(labels_image) * number_images
    #print("Value : ", value_to_get)

    for image_name in labels_image: # création des dictionnaires
        dictionary_skeletons[image_name] = []
        dictionary_reverse_hand[image_name] = []
        dictionary_bent_fingers[image_name] = []

    datas = models.find() # récupération du curseur sur les données de la base de données
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


# Fonction qui retourne la distance de Minkowski entre deux points 3D p1 et p2
def distanceMinkowski(p1, p2):
    distance = pow(
        (pow(abs(p2[0] - p1[0]), 3) 
        + pow(abs(p2[1] - p1[1]), 3) 
        + pow(abs(p2[2] - p1[2]), 3)), 1/3
    )
    return distance


#On travaille sur les fonctions afin de détecter le signe peut importe la position de la main devant la caméra
def getTabDistanceAllFingers(skeleton):
    tab_distance_fingers = []

    #Distance base, point de la main pour chaque point de la main
    for i in range (1,21):
        tab_distance_fingers.append(distanceMinkowski(skeleton[0], skeleton[i]))
    
    #Distance extrémité doigt, extrémité autre doigt pour chaque doigt
    for i in range (1, 5):
        for j in range (i + 1, 6):
            tab_distance_fingers.append(distanceMinkowski(skeleton[i * 4], skeleton[j * 4]))
    #Cette partie améliore la précision de 49% à 63%
    return tab_distance_fingers

#Fonction qui retourne la distance cumulée entre deux skeletons
def compareSkeletons(tab_dist_skeleton1, tab_dist_skeleton2):
    sommeDistance = 0
    for i in range(len(tab_dist_skeleton1)):
        sommeDistance += abs(tab_dist_skeleton1[i] - tab_dist_skeleton2[i])
    return sommeDistance

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

            #On récupère l'écart des distances entre chaque doigt
            value_similar = compareSkeletons(tab_distance_skeleton, tab_distance_tempo)


            #On ajoute une pénalité pour chaque doigt qui ne sont pas plié dans le même sens
            for j in range(len(dictionary_reverse[label][i])):
                if(bool_reverse[j] != dictionary_reverse[label][i][j]):
                    value_similar += 30

            #On ajoute une pénalité pour chaque doigt qui ne sont pas plié dans le même sens
            for j in range(len(dictionary_bent_fingers[label][i])):
                if(bent_fingers[j] != dictionary_bent_fingers[label][i][j]):
                    value_similar += 30
            
            #On va comparer les angles entre les doigts cependant ça marche PAS bien
            #valueSimilar += getDistanceAngle(newSkeleton, tabPointsTempo)
            values_similar.append(value_similar)

        value_similarity.append(np.min(values_similar))

    #On récupère le label du skeleton le plus similaire
    #print("Labels choisis : ", labels_skeleton[np.argmin(value_similarity)])
    return labels_skeleton[np.argmin(value_similarity)]


