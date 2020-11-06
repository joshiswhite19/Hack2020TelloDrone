import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from djitellopy import Tello
import cv2
import time

######################################################################

####################### AUXILIARY FUNCTIONS ##########################

### DETERMINE PATROL PERIMETER FUNCTIONALITY



### MAIN PATROL FUNCTIONALITY



### IDENTIFY OBJECT FUNCTIONALITY



### APPROPRIATE ACTION FUNCTIONALITY
