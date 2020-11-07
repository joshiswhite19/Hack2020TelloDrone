import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from djitellopy import Tello
import cv2
import time
 
#################### DEFINE GLOBAL VARIABLES #########################
X_BOUND = 4 * 30.48 # 4 feet in centimeters
Y_BOUND = 6 * 30.48 # 6 feet in centimeters
img_width = 320  # WIDTH OF THE IMAGE
img_height = 240  # HEIGHT OF THE IMAGE
simulation = 0   #  0 FOR FLIGHT 1 FOR TESTING
state = {
    "x": 0,
    "y": 0,
    "z": 0,
    "theta": 0
}
######################################################################
 
################## CONNECT TO TELLO & INIT ###########################
drone = Tello()
drone.connect()
drone.for_back_velocity = 0
drone.left_right_velocity = 0
drone.up_down_velocity = 0
drone.yaw_velocity = 0
drone.speed = 0
######################################################################

##################### COLLECT BASIC HEALTH INFO ######################
print(drone.get_battery())
######################################################################

drone.streamoff()
drone.streamon()
 
#################### IMPLEMENT MAIN FUNCTION #########################
def main():
    while True:
    
        # GET THE IMGAE FROM TELLO
        frame_read = drone.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (img_width, img_height))
    
        # TO GO UP IN THE BEGINNING
        if simulation == 0:
            drone.takeoff()
            time.sleep(8)
            drone.rotate_clockwise(90)
            time.sleep(3)
            drone.move_left(35)
            time.sleep(3)
            drone.land()
            startCounter = 1
    
        # # SEND VELOCITY VALUES TO TELLO
        # if me.send_rc_control:
        #     me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
    
        # DISPLAY IMAGE
        cv2.imshow("MyResult", img)
    
        # WAIT FOR THE 'Q' BUTTON TO STOP
        if cv2.waitKey(33) == ord('a'):
            drone.land()
            break
######################################################################
if __name__ == "__main__":
    main()
######################################################################

####################### AUXILIARY FUNCTIONS ##########################
### DETERMINE PATROL PERIMETER FUNCTIONALITY

def setState(state, x, y, z, theta):
    state["x"] = x
    state["y"] = y
    state["z"] = z
    state["theta"] = theta
    
def checkBounds(state):
    lala = 1

# Set initial state to zero
# Update whenever a move happens

### MAIN PATROL FUNCTIONALITY



### IDENTIFY OBJECT FUNCTIONALITY



### APPROPRIATE ACTION FUNCTIONALITY

