from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
import webbrowser
import subprocess

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("volume.GetVolumeRange(): (%s, %s, %s)" % volume.GetVolumeRange())
    min,max,unkown = volume.GetVolumeRange()
    if(volume.GetMasterVolumeLevel()-3<=min):
        volume.SetMasterVolumeLevel(min , None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()-3, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())
    
    
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("volume.GetVolumeRange(): (%s, %s, %s)" % volume.GetVolumeRange())
    min,max,unkown= volume.GetVolumeRange()
    if(volume.GetMasterVolumeLevel()+3>=max):
        volume.SetMasterVolumeLevel(max, None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()+3, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())
    
def open_link(link):
    webbrowser.open(link, new=2)
    
def open_program(program):
    subprocess.Popen(program)