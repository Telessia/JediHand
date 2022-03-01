#Functions that choose the right action to execute on the OS following the config.json file
import actions as actions
from pymongo import MongoClient

client = MongoClient('localhost', 27017, username='root', password='root')
db = client['jedihand_development'] #name of the database, see docker-compose

def interprete(label):
    models = db.models
    result = models.find_one({"groupname": label })
    cmd = result["command"]
    arg = None
    if(("launch_a_link" in cmd) or ("launch_a_program" in cmd)):
        cmd,arg = cmd.split(" ")
    launch(cmd,arg)
    
    
def launch(inst,arg):#Function that call the right action
    
    if(inst == "turn_up_volume"):
        actions.increase_volume()
    elif(inst == "turn_down_volume"):
        actions.decrease_volume()
    elif(inst == "launch_a_link"):
        actions.open_link(arg)
    elif(inst == "launch_a_program"):
        actions.open_program(arg)
        
    
    
    
    

