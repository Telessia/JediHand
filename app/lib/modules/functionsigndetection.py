import numpy as np
import cv2
import mediapipe as mp

from math import degrees

#labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
#  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

mp_hands = mp.solutions.hands


def getAngle(base, points1, points2):

    vecteur1, vecteur2 = [], []
    vecteur1 = [points1[0] - base[0], points1[1] - base[1], points1[2] - base[2]]
    vecteur2 = [points2[0] - base[0], points2[1] - base[1], points2[2] - base[2]]

    valeurRadian = 0.0
    #dot = produit scalaire, linalg.norm = norme d'un vecteur
    valeurRadian = np.arccos(np.dot(vecteur1, vecteur2) / 
    (np.linalg.norm(vecteur1) * np.linalg.norm(vecteur2)))
    return degrees(valeurRadian)


def copyOfTabSkeletons(tabSkeleton):
    tabReturn = []
    for tabP in tabSkeleton:
        tabT = []
        tabT.append(tabP.x)
        tabT.append(tabP.y)
        tabT.append(tabP.z)
        tabReturn.append(tabT)
    return tabReturn

def printStateFingers(tabPoints):
    limiteHand = [tabPoints[6].y, tabPoints[10].y, tabPoints[14].y, tabPoints[18].y]

    tabBentFingers = []

    reverseHandTempo = tabPoints[0].y < tabPoints[4].y

    #Construction du tableau de booléen qui détermine si un doigt est replié et du calcul de l'angle formé par les doigts
    for i in range(4):
                    
        #Détection des doigts pliés
        boolBentFinger = tabPoints[8 + 4 * i].y > limiteHand[i]
        tabBentFingers.append(not boolBentFinger if reverseHandTempo else boolBentFinger)
    
    print("Main renversé : ", reverseHandTempo)
    print("Tableau doigt pliés : ", tabBentFingers)
    
    print("Base main : ", tabPoints[0].y, " index : ", tabPoints[4].y, " majeur : ", tabPoints[12].y, " annulaire : ", 
        tabPoints[16].y, " auriculaire : ", tabPoints[20].y)


def distanceMinkowski2(p1, p2):
    distance = pow(
        (pow(abs(p2[0] - p1[0]), 3) 
        + pow(abs(p2[1] - p1[1]), 3) 
        + pow(abs(p2[2] - p1[2]), 3)), 1/3
    )
    return distance

#On travaille sur les fonctions afin de détecter le signe peut importe la position de la main devant la caméra
def getTabDistanceAllFingers(skeleton):
    tabDistanceFingers = []

    #Distance base, point de la main pour chaque point de la main
    for i in range (1,21):
        tabDistanceFingers.append(distanceMinkowski2(skeleton[0], skeleton[i]))
        #print(i)
    
    #Distance extrémité doigt, extrémité autre doigt pour chaque doigt
    for i in range (1, 5):
        for j in range (i + 1, 6):
            #print(i * 4, j * 4)
            tabDistanceFingers.append(distanceMinkowski2(skeleton[i * 4], skeleton[j * 4]))
    #Cette partie améliore la précision de 49% à 63%
    return tabDistanceFingers

def compareDistanceSkeletons2(skeleton1, skeleton2):
    somme = 0
    for i in range(0, len(skeleton1)):
        somme += distanceMinkowski2(skeleton1[i], skeleton2[i])
        print("- somme : ", somme)
    return somme

def compareSkeletons(tabDistSkeleton1, tabDistSkeleton2):
    sommeDistance = 0
    for i in range(len(tabDistSkeleton1)):
        sommeDistance += abs(tabDistSkeleton1[i] - tabDistSkeleton2[i])
    return sommeDistance





def constructValuesFromImages(labels, minDetectionConfidence, tabSkeletons, tabReversedHands, 
    tabBentFingersHands, tabValueAngleHands):

    with mp_hands.Hands(
    static_image_mode=True, max_num_hands=1, min_detection_confidence=minDetectionConfidence, min_tracking_confidence=0.5) as hands:

        for str in labels:
            #Récupération de l'image
            image = cv2.imread("app/lib/modules/image/apprentissage/" + str + ".jpg")
            #Récupération du skeleton de l'image
            skeleton = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            #print(str, " en cours !")

            #Récupération du tableau de points du skeleton
            tabPointsTempo = copyOfTabSkeletons(skeleton.multi_hand_landmarks[0].landmark)
            tabPointsTempo = np.multiply(tabPointsTempo, 100)
            tabSkeletons.append(tabPointsTempo)

            #Calcul si la main est à l'envers ou non
            reverseHandTempo = tabPointsTempo[0][1] < tabPointsTempo[4][1]
            tabReversedHands.append(reverseHandTempo)

            #print("Main Reverse ? : ", reverseHandTempo)

            #Construction d'un tableau des coordonnées limites à laquelle l'extrémité doit être 
            #au dessus pour ne pas être considéré comme plié
            limiteHand = [tabPointsTempo[6][1], tabPointsTempo[10][1], tabPointsTempo[14][1], tabPointsTempo[18][1]]
            #print("Tab des limites : ", limiteHand)

            tabBentFingers = []
            vecteur1 = []
            vecteur2 = []
            valeurRadian = []

            #Construction du tableau de booléen qui détermine si un doigt est replié et du calcul de l'angle formé par les doigts
            for i in range(4):
                
                #Détection des doigts pliés
                boolBentFinger = tabPointsTempo[8 + 4 * i][1] > limiteHand[i]
                tabBentFingers.append(not boolBentFinger if reverseHandTempo else boolBentFinger)

                vecteur1.append([tabPointsTempo[4 + 4 * i][0] - tabPointsTempo[0][0], 
                  tabPointsTempo[4 + 4 * i][1] - tabPointsTempo[0][1], 
                  tabPointsTempo[4 + 4 * i][2] - tabPointsTempo[0][2]])

                vecteur2.append([tabPointsTempo[8 + 4 * i][0] - tabPointsTempo[0][0], 
                  tabPointsTempo[8 + 4 * i][1] - tabPointsTempo[0][1], 
                  tabPointsTempo[8 + 4 * i][2] - tabPointsTempo[0][2]])

                #dot = produit scalaire, linalg.norm = norme d'un vecteur
                valeurRadian.append(np.arccos(np.dot(vecteur1[i], vecteur2[i]) / 
                    (np.linalg.norm(vecteur1[i]) * np.linalg.norm(vecteur2[i]))))

            #print("Tableau doigt pliés : ", tabBentFingers)
            #print("Valeur des angles : ", degrees(valeurRadian[0]), degrees(valeurRadian[1]), 
            #    degrees(valeurRadian[2]), degrees(valeurRadian[3]), "\n")

            tabValueAngleHands.append(valeurRadian)
            tabBentFingersHands.append(tabBentFingers)

            #print(str, " done !")



def getDistanceAngle(tabNew, tabReference):
    distance = 0.0
    for i in range (1, 5):
        for j in range (i + 1, 6):
            distance += abs(getAngle(tabNew[0], tabNew[i], tabNew[j]) - 
                getAngle(tabReference[0], tabReference[i], tabReference[j]))
    return distance


#Fonction qui retourne le label du signe le plus proche du skeleton en entrée
def getClosestLabels(labels, tabSkeletons, tabReversedHands, tabBentFingersHands, newSkeleton):
    #print("Labels : ", labels)
    distanceNormalNew = distanceMinkowski2(newSkeleton[0], newSkeleton[17])
    tabDistanceNew = getTabDistanceAllFingers(newSkeleton)

    reverseHandNew = newSkeleton[0][1] < newSkeleton[4][1]
    #print("Main reverse ? ", reverseHandNew)

    limiteHand = [newSkeleton[6][1], newSkeleton[10][1], newSkeleton[14][1], newSkeleton[18][1]]

    tabBentFingers = []
    for i in range(4):
        #Détection des doigts pliés
        boolBentFinger = newSkeleton[8 + 4 * i][1] > limiteHand[i]
        tabBentFingers.append(not boolBentFinger if reverseHandNew else boolBentFinger)

    #print("Tableau doigt pliés : ", tabBentFingers)
    valueSimilarity = []

    for i in range(len(tabSkeletons)):
        tabPointsTempo = tabSkeletons[i]
        distanceNormalCamera = distanceMinkowski2(tabPointsTempo[0], tabPointsTempo[17])
        tauxMultiplication = distanceNormalNew / distanceNormalCamera
        tabPointsTempoNormalized = np.multiply(tabPointsTempo, tauxMultiplication)
        tabDistanceTempo = getTabDistanceAllFingers(tabPointsTempoNormalized)

        #On récupère l'écart des distances entre chaque doigt
        valueSimilar = compareSkeletons(tabDistanceNew, tabDistanceTempo)

        #Si la direction de la main n'est pas la même alors c'est une pénalité
        if (reverseHandNew != tabReversedHands[i]):
            valueSimilar += 50

        #On ajoute une pénalité pour chaque doigt qui ne sont pas plié dans le même sens
        for j in range(len(tabBentFingersHands[i])):
            if(tabBentFingers[j] != tabBentFingersHands[i][j]):
                valueSimilar += 30
        
        #On va comparer les angles entre les doigts cependant ça marche PAS bien
        #valueSimilar += getDistanceAngle(newSkeleton, tabPointsTempo)

        valueSimilarity.append(valueSimilar)

    #On récupère le label du skeleton le plus similaire
    #print("Labels choisis : ", labels[np.argmin(valueSimilarity)])
    return labels[np.argmin(valueSimilarity)]


def functionTestPrecision(minDetectConfidence, labelsTest, namesTest, labels, tabSkeletons, tabReversedHands, tabBentFingersHands):
    #print(len(labelsTest), "   ", len(namesTest))

    sommeGoodPredictions = 0.0 #Compteur de bonne réponse
    totalPredictions = 0 #Total de réponses prédites, des fois il n'y a pas de skeleton avec mediapipe

    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=1, 
        min_detection_confidence=minDetectConfidence, min_tracking_confidence=0.5
        ) as hands:

        for i in range(len(namesTest)):
            #Récupération de l'image
            #print("Names Actuel : ", namesTest[i])

            image = cv2.imread("app/lib/modules/image/test/" + namesTest[i] + ".jpg")
            #Récupération du skeleton de l'image
            skeletonTest = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            #Pas de problème de détection
            if(skeletonTest.multi_hand_landmarks != None):
                tabPointsTempoTest = copyOfTabSkeletons(skeletonTest.multi_hand_landmarks[0].landmark)

            #On multiplie par 100 pour rendre plus sensible aux divergences
            tabPointsTempoTest = np.multiply(tabPointsTempoTest, 100)
            #On récupère le label prédit par l'algorithme
            predictedLabel = getClosestLabels(labels, tabSkeletons, tabReversedHands, tabBentFingersHands, tabPointsTempoTest)
            #print("Predit ? : ", predictedLabel)

            if(predictedLabel == labelsTest[i]):
                sommeGoodPredictions += 1
            
            totalPredictions += 1
    
    print("Good Predictions : ", sommeGoodPredictions, "  Total Predictions : ", totalPredictions)
    print("Precision de l'algorithme : ", (sommeGoodPredictions / totalPredictions) * 100, "%")


