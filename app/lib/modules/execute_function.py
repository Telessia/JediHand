from function_test import *
from function_sign_comparison import constructBaseImages
from pymongo import MongoClient
import os



labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
  "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

dictionary_sign_fingers = { "A": 0, "B": 4, "C": 5, "D": 1, "E": 0, "F": 3, "G": 1, "H": 2, "I": 1, "J": 1,
  "K": 2, "L": 2, "M": 0, "N": 0, "O": 0, "P": 3, "Q": 2, "R": 2, "S": 0, "T": 0, "U": 2, "V": 2, "W": 3,
  "X": 1, "Y": 2, "Z": 1 }

labelsTest = ["A2", "A22", "B14", "B15", "B19", "C17", "C19", "C22", "C23", "D1", "F3", "F17",
  "G3", "G4", "G7", "G11", "G20", "H5", "H19", "H25", "I17", "I28",
  "J6", "J9", "J27", "J28", "K6", "K12", "K13", "K24", "M14", "M20",
  "N6", "N9", "N22", "O4", "O12", "O20", "P24", "Q7", "Q10", "R5", "R18", "S0", "S6", 
  "S16", "T1", "T13", "T17", "T18", "T24", "U5", "U6", "V2", "V10", 
  "V12", "V27", "W7", "W16", "W19", "W23", "W24", "X9", "X14", "X20",
  "X24", "Y5", "Y25", "Z9", "Z16", "Z18", "Z27"]


path_app_v2 = 'app/static/default_datas/train/' #Path of the images to load

files = os.listdir(path_app_v2)

#Connection to running database
client = MongoClient('localhost', 27017, username='root', password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

models = db.models
models_test = db.models_test

labels_skeleton = extract_labels(models)
print(len(labels_skeleton))

dict_skel = {}
dict_rev = {}
dict_bent = {}
dict_skel, dict_rev, dict_bent = constructBaseImages(models, labels_skeleton, 50)


#functionTestPrecisionVersion2(0.68, models_test, dict_skel, dict_rev, dict_bent)
functionTestVersion2Camera(0.7, dict_skel, dict_rev, dict_bent)


#functionTestPrecisionVersion1(0.68, 0.7, labels, dictionary_sign_fingers)
#functionTestVersion1Camera(0.7)

"""for i in range (19):
    print(0.05 + i*0.05)
    functionTestPrecisionVersion1(0.05 + i*0.05, 0.7, labels, dictionary_sign_fingers)"""

