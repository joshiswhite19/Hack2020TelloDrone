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
# Personality states (what the drone should be doing):
# 'STARTUP' - initial state of drone
# 'PATROL' - default normal state, just traverse patrol zone and keep watch
#            for any objects that will cause a personality change
# 'FOLLOW' - follow an object tagged for following
personality = 'STARTUP' 

####################### OPERATING MODES ##############################
 
flight = 1     #  1 FOR FLIGHT 0 FOR NO FLIGHT TESTING
vision = 1     #  1 FOR ACTIVE VISION TESTING
verbose = 1    #  1 FOR ADDED LOGGING, 0 OTHERWISE

######################################################################
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

######################################################################
####################### AUXILIARY FUNCTIONS ##########################
######################################################################
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
def moveRight(x):
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



# Set initial state to zero
# Update whenever a move happens

### MAIN PATROL FUNCTIONALITY

# If moving out of bounds, correct position
def checkBounds():
    # Calculate difference between current state and bounds, store in variables
    x_dif = X_BOUND - state['x'] # if negative, outside bounds
    y_dif = Y_BOUND - state['y'] # if negative, outside bounds
    # If difference is negative, move it back in bounds
    if (x_dif < 0):
        print(f'OUTSIDE RIGHT BOUND BY {x_dif} cm')
        corrAngle = np.pi-state['theta']
        if (corrAngle < 0):
            print(f'input corrAngle: {-1*corrAngle*(180/np.pi)} degrees')
            rotateCW(-1*corrAngle*(180/np.pi))
        else: 
            print(f'input corrAngle: {corrAngle*(180/np.pi)} degrees')
            rotateCCW(corrAngle*(180/np.pi))

        moveForward(-1*x_dif)

    if (y_dif < 0):
        print(f'OUTSIDE TOP BOUND BY {y_dif} cm')
        corrAngle = (np.pi*(3/2))-state['theta']
        if (corrAngle < 0):
            rotateCW(-1*corrAngle*(180/np.pi))
        else:
            rotateCCW(corrAngle*(180/np.pi))

        moveForward(-1*y_dif)
        
    if (x_dif > X_BOUND):
        print(f'OUTSIDE LEFT BOUND BY {x_dif} cm')
        corrAngle = np.pi-state['theta']
        if (corrAngle < 0):
            rotateCCW((np.pi + corrAngle)*(180/np.pi))
        else:
            rotateCW(state['theta']*(180/np.pi))
        
        moveForward(-1*state['x'])

    if (y_dif > Y_BOUND):
        print(f'OUTSIDE BOTTOM BOUND BY {y_dif} cm')
        corrAngle = (np.pi*(1/2)) - state['theta']
        if (corrAngle < 0):
            rotateCW(-1*corrAngle*(180/np.pi))
        else:
            rotateCCW(corrAngle*(180/np.pi))

        moveForward(-1*state['y'])



# Define a basic patrol pattern
def Patrol():
    
    while personality == 'PATROL':
        todo = 1
        # Move about pre-defined area
        # Check that I am in bounds
        # Keep an eye out for objects that will cause me to change personality


### IDENTIFY OBJECT FUNCTIONALITY



### APPROPRIATE ACTION FUNCTIONALITY



######################################################################
#################### IMPLEMENT MAIN FUNCTION #########################
def main():
    t0 = time.time()
    runtime = t0

    #if personality == 'STARTUP':
    if flight: drone.takeoff()
        #personality = 'PATROL'

    while True:

        t_old = runtime
        runtime = time.time() - t0
        dt = runtime - t_old
        
        if verbose: print(f'Current runtime: {runtime} seconds\n Current looptime: {dt}')
    # NEED TO REDO ALL OF THIS
        # GET THE IMAGE FROM TELLO
        #frame_read = drone.get_frame_read()
        #myFrame = frame_read.frame
        #img = cv2.resize(myFrame, (img_width, img_height))

        time.sleep(2)
        rotateCCW(45)
        moveForward(100)
        rotateCW(45)
        moveForward(60)
        checkBounds()
        time.sleep(10)
        #moveLeft(35)
        #time.sleep(2)
        #if flight: drone.land()
        #startCounter = 1
    
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
        if flight or vision: del drone
        #drone.STATE_UDP_PORT
        
######################################################################



