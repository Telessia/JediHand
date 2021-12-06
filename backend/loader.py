import json
path = "../shared/config.json"

f = open(path)

data = json.load(f)
 
for d in data['commands']:
    print(d)
 
f.close()