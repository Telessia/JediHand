#Functions that let us read and write commands affected to a hand sign into config.json
import json
import os

path = "frontend/static/js/config.json"

#https://www.programiz.com/python-programming/json

#Load and return datas from config.json
def load_config():
    try:
        with open(path) as f:
            data = json.load(f)
            return data
    except OSError:
        print('cannot open',path)
        
#Save commands and figures match in config.json
def save_config(listeCommand, listeFigure, listeAffectation):
    try:
        dict = json.loads(listeCommand)
        dict2 = json.loads(listeFigure)
        dict3 = json.loads(listeAffectation)

        finalDict = {'possibleCommands':dict}
        finalDict['possibleFigure'] = dict2
        finalDict['affectedCommandsFigure'] = dict3
        
        print(finalDict)
        os.path.isfile(path)
        print(os.path.isfile(path))
        
        with open(path, 'w') as f:
            json.dump(finalDict, f)
    except OSError:
        print('cannot open',path)
    