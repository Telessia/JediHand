import json
path = "shared/config.json"

array = []
def load_from_json():
    f = open(path)

    data = json.load(f)
    
    d = data["affectedCommandsFigure"]
    
    f.close()
    
    return d