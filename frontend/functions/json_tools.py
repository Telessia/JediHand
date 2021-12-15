import json
import os

path = "./../shared/config.json"

#https://www.programiz.com/python-programming/json

def load_config():
    try:
        with open(path) as f:
            data = json.load(f)
            # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
            print(data)
    except OSError:
        print('cannot open',path)
        
def save_config(datas):
    try:
        os.path.isfile(path)
        print(os.path.isfile(path))
        with open(path, 'w') as f:
            json.dump(datas, f)
    except OSError:
        print('cannot open',path)
    