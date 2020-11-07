import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from djitellopy import Tello
import cv2
import time
import math
import numpy as np

#################### DEFINE GLOBAL VARIABLES #########################
X_BOUND = 4 * 30.48 # 4 feet in centimeters
Y_BOUND = 6 * 30.48 # 6 feet in centimeters
Z_BOUND = 8 * 30.48 # 8 feet in centimeters
img_width = 320  # WIDTH OF THE IMAGE
img_height = 240  # HEIGHT OF THE IMAGE
state = {
    'x': 0, # x position in cm
    'y': 0, # y position in cm
    'z': 0, # height in cm
    'theta': 0 # Direction in radians
}

######################################################################
 
flight = 0     #  1 FOR FLIGHT 0 FOR NO FLIGHT TESTING
vision = 1     #  1 FOR ACTIVE VISION TESTING
verbose = 1    #  1 FOR ADDED LOGGING, 0 OTHERWISE

################## CONNECT TO TELLO & INIT ###########################
if flight or vision:
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

####################### AUXILIARY FUNCTIONS ##########################
### DETERMINE PATROL PERIMETER FUNCTIONALITY / MAIN MOVEMENT FUNCTION WRAPPERS

# Straight set of the state dictionary
def setState(x, y, z, theta):
    state["x"] = x
    state["y"] = y
    state["z"] = z
    state["theta"] = theta

# Update the state dictionary
def updateState(x, y, z, theta):
    state['x'] += x
    state['y'] += y
    state['z'] += z
    state['theta'] = (state['theta'] + theta) % (2 * np.pi)
    if verbose: printState()

def printState():
    print(f'''
    x = {state['x'] * (1/30.48)} ft
    y = {state['y'] * (1/30.48)} ft
    z = {state['z'] * (1/30.48)} ft
    theta = {state['theta'] * (180/np.pi)} degrees
    ''')
    
# Wrapper for Tello.move_foward function
def moveForward(x):
    if flight: drone.move_forward(x)
    updateState(
        x * math.cos(state['theta']),
        x * math.sin(state['theta']),
        0, 0
    )

# Wrapper for Tello.move_back function
def moveBack(x):
    if flight: drone.move_back(x)
    updateState(
        -1 * x * math.cos(state['theta']),
        -1 * x * math.sin(state['theta']),
        0, 0
    )

# Wrapper for Tello.move_left function
def moveLeft(x):
    if flight: drone.move_left(x)
    thet = state['theta'] + (np.pi/2)
    updateState(
        x*math.cos(thet),
        x*math.sin(thet),
        0, 0
    )

# Wrapper for Tello.move_right function
def moveLeft(x):
    if flight: drone.move_right(x)
    thet = state['theta'] - (np.pi/2)
    updateState(
        x*math.cos(thet),
        x*math.sin(thet),
        0, 0
    )

# Wrapper for Tello.move_up function
def moveUp(x):
    if flight: drone.move_up(x)
    updateState(0, 0, x, 0)

# Wrapper for Tello.move_down function
def moveDown(x):
    if flight: drone.move_down(x)
    updateState(0, 0, -1 * x, 0)

# Wrapper for Tello.rotate_clockwise function
def rotateCW(x):
    if flight: drone.rotate_clockwise(x)
    updateState(0, 0, 0, -1 * x * (np.pi/180))

# Wrapper for Tello.rotate_counter_clockwise function
def rotateCCW(x):
    if flight: drone.rotate_counter_clockwise(x)
    updateState(0, 0, 0, x * (np.pi/180))

def checkBounds(state):
    todo = 1

# Set initial state to zero
# Update whenever a move happens

### MAIN PATROL FUNCTIONALITY



### IDENTIFY OBJECT FUNCTIONALITY



### APPROPRIATE ACTION FUNCTIONALITY



######################################################################
#################### IMPLEMENT MAIN FUNCTION #########################
def main():
    runtime = time.time()

    while True:

        dt = time.time() - runtime
        if verbose: print(f'Current runtime: {dt} seconds')
    # NEED TO REDO ALL OF THIS
        # GET THE IMAGE FROM TELLO
        #frame_read = drone.get_frame_read()
        #myFrame = frame_read.frame
        #img = cv2.resize(myFrame, (img_width, img_height))


        if flight: drone.takeoff()
        time.sleep(2)
        rotateCW(90)
        time.sleep(2)
        moveLeft(35)
        time.sleep(2)
        if flight: drone.land()
        startCounter = 1
    
        # # SEND VELOCITY VALUES TO TELLO
        # if me.send_rc_control:
        #     me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
    
        # DISPLAY IMAGE
        
        #cv2.imshow("MyResult", img)
    
        
######################################################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n KeyboardInterrupt recorded! Landing drone and quitting!')
        if flight: drone.land()
######################################################################



