import lib.modules.loader as ld
import lib.modules.actions as actions

d = ld.load_from_json()

for dx in d:
    if dx["figure"] == "OneHand_OneFinger" :
        onefinger = dx
    if dx["figure"] == "OneHand_TwoFinger" :
        twofinger = dx
    if dx["figure"] == "OneHand_ThreeFinger" :
        threefinger = dx
    if dx["figure"] == "OneHand_FourFinger" :
        fourfinger = dx
    if dx["figure"] == "OneHand_FiveFinger":
        fivefinger = dx

def select(raisedfingers):
    
    if raisedfingers == 0 :
        return -1
    elif raisedfingers == 1:
        launch(onefinger)
        return 0
    elif raisedfingers == 2:
        launch(twofinger)
        return 0
    elif raisedfingers == 3:
        launch(threefinger)
        return 0
    elif raisedfingers == 4:
        launch(fourfinger)
        return 0
    elif raisedfingers == 5:
        launch(fivefinger)
        return 0
        
def launch(inst):
    
    if(inst['command'] == "turn_up_volume"):
        actions.increase_volume()
    elif(inst['command']== "turn_down_volume"):
        actions.decrease_volume()
    elif(inst['command'] == "launch_a_link"):
        actions.open_link(inst["link"])
    elif(inst['command'] == "launch_a_program"):
        actions.open_program(inst["program"])
        
    
    
    
    

