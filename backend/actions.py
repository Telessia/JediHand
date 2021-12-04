from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("volume.GetVolumeRange(): (%s, %s, %s)" % volume.GetVolumeRange())
    min,max,unkown = volume.GetVolumeRange()
    if(volume.GetMasterVolumeLevel()-1<=min): #TODO fix decrease limits
        volume.SetMasterVolumeLevel(min , None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()-1, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())
    
    
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("volume.GetVolumeRange(): (%s, %s, %s)" % volume.GetVolumeRange())
    min,max,unkown= volume.GetVolumeRange()
    if(volume.GetMasterVolumeLevel()+1>=max): #TODO fix increase limits
        volume.SetMasterVolumeLevel(max, None)
    else: 
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()+1, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())