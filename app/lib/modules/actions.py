#Actions function the app can performs on the Host OS (only Windows here)

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
import webbrowser
import subprocess

#Function that decrease the volume on windows OS
def decrease_volume():
    devices = AudioUtilities.GetSpeakers() #Get device speakers
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min,max,unkown = volume.GetVolumeRange() #Get max and min value for the speakers
    if(volume.GetMasterVolumeLevel()-3<=min): #If the step goes under minimum we put the sound at minimum (prevent crash)
        volume.SetMasterVolumeLevel(min , None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()-3, None) #Else decrease the volume by 3 steps
    
#Function that increase the volume on windows OS
def increase_volume():
    devices = AudioUtilities.GetSpeakers() #Get devices speakers
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min,max,unkown= volume.GetVolumeRange()
    if(volume.GetMasterVolumeLevel()+3>=max):#If the step goes above maximum we put the sound at maximum (prevent crash)
        volume.SetMasterVolumeLevel(max, None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()+3, None) #Else we increase the volume by 3 steps
    
#Function that open the default browser on a specific link
def open_link(link):
    webbrowser.open(link, new=2)
    
#Function that open a give program on the host device
def open_program(program):
    subprocess.Popen(program)