import json
import os

path = "frontend/static/js/config.json"

#https://www.programiz.com/python-programming/json

def load_config():
    try:
        with open(path) as f:
            data = json.load(f)
            # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
            return data
    except OSError:
        print('cannot open',path)
        
def save_config(listeCommand, listeFigure, listeAffectation):
    try:
        dict = json.loads(listeCommand)
        dict2 = json.loads(listeFigure)
        dict3 = json.loads(listeAffectation)

        test = { "test":"test"}
        test2 = { "test":"test2"}
        test3 = { "test":"test3"}

        finalDict = {'possibleCommands':dict}
        finalDict['possibleFigure'] = dict2
        finalDict['affectedCommandsFigure'] = dict3
        print(finalDict)

        #jsonObject = {'test': [{'command': "commandTest", "figure": "figureTest"}, {'command2': "commandTest2", "figure2": "figureTest2"}]}

        os.path.isfile(path)
        print(os.path.isfile(path))
        with open(path, 'w') as f:
            json.dump(finalDict, f)
            #json.dump(liste, f)
            #json.dump(datas , f)
    except OSError:
        print('cannot open',path)
    