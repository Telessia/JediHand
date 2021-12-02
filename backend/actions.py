from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    if(volume.GetMasterVolumeLevel()>-98): #TODO fix decrease limits
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()-1, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())
    
    
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    if(volume.GetMasterVolumeLevel()<-2): #TODO fix increase limits
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()+1, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())