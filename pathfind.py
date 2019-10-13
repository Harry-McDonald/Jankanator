from micromelon import *
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import time
import numpy as np

# ~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~
def deg2rad(degrees):
  rads = degrees*pi/180
  return rads

# initialise variables
mtr_speed = 10 #cm/s
set_speed = np.arrar([mtr_speed,mtr_speed])
turn_inc = 20 #degrees
min_obj_IRdist = 20 #cm
min_obj_Ultradist = 20 #cm

# Initial states
AVOIDING = False # Status of the Jankanator while it is avoiding an object
target_timer = False # Timer used to record time elapsed while moving in the avoiding stage -> Initialise to off
avoiding_timer = False # Timer used to record time elapsed while moving towards target -> Initialise to off

# Define final goal
final_dist = 100 #cm
dist_target = final_dist # Initialise the distance from the Jankanator to the flagpole
# Initialise orientation, turning increment
orig_orient = 0 # degrees -> Facing the target
orient = orig_orient #initialise


# Start engine
Motors.write(set_speed)
t0 = time.clock() # Get the time the Jankanator starts moving towards the target
target_timer = True # Turn target timer on
#Begin algorithm
while True:
  ultra_dist = Ultrasonic.read() # centimeters
  ir_distL = IR.readLeft() #cm
  ir_distR = IR.readRight() #cm
  # Check if we have reached our desired distance
  target_check_time = time.clock()
  time_moving_to_target_check = target_check_time - target_time0
  dist_check = dist_target - (mtr_speed*time_moving_to_target_check)
  if dist_check <= 0:
    Motors.stop()
  if ultra_dist > min_obj_Ultradist: #Enter if there is no object infront of Jankanator
    if AVOIDING: # Check if we are in the avoiding stage
      if ir_distL < min_obj_IRdist:  #Check left IR sensor to see if it is next to an object -> if true we are still in the avoiding stage
        Motors.write(set_speed) # Keep moving until clear
        if not avoiding_timer: # if avoiding timer hasn't already been set -> set it
          avoiding_time0 = time.clock() # Get time when motors start in AVOIDING mode
          avoiding_timer = True # Record that avoiding timer has been set in this avoiding iteration
      else: # If we have cleared the object
        AVOIDING = False # No longer avoiding
        dist_moved_calc = False # Reinitialise until next avoiding stage
        avoiding_time1 = time.clock() # Get time when Jankanator has finished avoiding
        avoiding_timer = False # Re-initialise timer so that it can be restarted in the next avoiding stage
        time_avoiding = avoiding_time1 - avoiding_time0 # Total time elapsed while avoiding
        dist_avoiding = time_avoiding * mtr_speed # cm
        new_target_dist = math.sqrt(dist_target**2+dist_avoiding**2 - 2*dist_target*dist_avoiding*math.cos(deg2rad(orient))) #Re-calculate distnace as crow flies to the target -> cos rule
        beta = math.asin(dist_target*math.sin(orient)/new_target_dist) # Angle between new_target_dist and dist_travelled -> sine rule
        phi = phi - 180 # degrees the rover must turn to be facing the target -> remember positive angles are clockwise on the Jankanator, we want to go the opposite here
        Motors.turnDegrees(phi)
        dist_target = new_target_dist # Reinitialise the distance to the target
        orient = 0 # degrees - Reinitialise the orientation
        Motors.write(set_speed) # Get on your bike
        target_time0 = time.clock() # Get time that the Jankanator starts moving towards the target again
        target_timer = True # Turn target timer on
    else: # If object has been avoided
      Motors.write(set_speed) # Keep on trucking

  elif ultra_dist <= min_obj_Ultradist: # Sense object
    AVOIDING = True
    Motors.stop() #stop
    if not dist_moved_calc: # if we haven't already calculated the distance moved in the last targetting phase -> do the calculation
      target_time1 = time.clock() # Get the time at which the Jankanator stops moving towards the target
      target_timer = False # Turn target timer off because we aren't moving towards the target anymore
      targetting_time = target_time1 - target_time0 # Time elapsed while moving toward the target
      dist_target = dist_target - (mtr_speed*targetting_time) # Calculate the distance we moved toward the target
      dist_moved_calc = True # We have now done the calc so no need to re-do it on the next iteration
    Motors.turnDegrees(turn_inc) # Turn until no longer facing the object - this turns a set amount and then rechecks on the next iteration
    orient = orient + turn_inc # record orientation wrt to the target - i.e 0 is facing the target
  #time.sleep(0.05)
