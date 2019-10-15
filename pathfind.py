from micromelon import *
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import time
import numpy as np

rc = RoverController()
rc.connectSerial()

# ~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~
def deg2rad(degrees):
  rads = degrees*math.pi/180
  return rads

def rad2deg(rads):
  degs = rads*180/math.pi
  return degs

# initialise variables
mtr_speed = 10 #cm/s
turn_inc = 10 #degrees
min_obj_IRdist = 50 #cm
min_obj_Ultradist = 30 #cm
evade_dist = 10 #cm
# Define final goal
final_dist = 150 #cm
dist_target = final_dist # Initialise the distance from the Jankanator to the flagpole

# Initial states
AVOIDING = False # Status of the Jankanator while it is avoiding an object
target_timer = False # Timer used to record time elapsed while moving in the avoiding stage -> Initialise to off
AVOIDING_TIMER = False # Timer used to record time elapsed while moving towards target -> Initialise to off
dist_moved_calc = False # Initialise
INITIAL_EVADE = False # When an object is sensed the first manouever is to move 10cm in the clear direction and then run checks on the left ir


# Initialise orientation, turning increment
orig_orient = 0 # degrees -> Facing the target
orient = orig_orient #initialise


# Start engine
Motors.write(mtr_speed, mtr_speed)
target_time0 = time.clock() # Get the time the Jankanator starts moving towards the target
target_timer = True # Turn target timer on
#Begin algorithm
while True:
  ultra_dist = Ultrasonic.read() # centimeters
  ir_distL = IR.readLeft() #cm
  print("Ultra dist = ",ultra_dist)
  print("IR dist Left = ",ir_distL)
  ir_distR = IR.readRight() #cm
  # Check if we have reached our desired distance
  # target_check_time = time.clock()
  # time_moving_to_target_check = target_check_time - target_time0
  # print("time movng check", time_moving_to_target_check)
  # dist_check = dist_target - (mtr_speed*time_moving_to_target_check)
  # print("distcheck = ",dist_check)
  # if dist_check <= 0:
  #   Motors.stop()
  #   break
  if ultra_dist > min_obj_Ultradist: #Enter if there is no object infront of Jankanator
    if AVOIDING: # Check if we are in the avoiding stage
      if INITIAL_EVADE:
        print("INITIAL EVADE")
        Motors.moveDistance(evade_dist,mtr_speed,mtr_speed)
        time.sleep(2) # adjustable when optimising -> could make a min sleep function that determines time needed to move based on mtr_speed
        INITIAL_EVADE = False # We have finished our initial move - next iteration should check if there is a object on our left
      elif ir_distL < min_obj_IRdist:  #Check left IR sensor to see if it is next to an object -> if true we are still in the avoiding stage
        print('Object on my left')
        Motors.write(mtr_speed, mtr_speed) # Keep moving until clear
        if not AVOIDING_TIMER: # if avoiding timer hasn't already been set -> set it
          avoiding_time0 = time.clock() # Get time when motors start in AVOIDING mode
          print("Timer0 set")
          AVOIDING_TIMER = True # Record that avoiding timer has been set in this avoiding iteration
      else: # If we have cleared the object
        print('STOP AVOIDING')
        Motors.stop()
        AVOIDING = False # No longer avoiding
        dist_moved_calc = False # Reinitialise until next avoiding stage
        avoiding_time1 = time.clock() # Get time when Jankanator has finished avoiding

        if AVOIDING_TIMER: # check if extra avoiding was necessary
          time_avoiding = avoiding_time1 - avoiding_time0 # Total time elapsed while avoiding
          print("time 0 = ", avoiding_time0)
          print("time 1 = ", avoiding_time1)
          print("time_avoiding",time_avoiding)
          dist_avoiding = evade_dist + time_avoiding * mtr_speed # cm
          print("dist_avoiding = ",dist_avoiding)
        else: # if no extra avoiding was necessary
          dist_avoiding = evade_dist
          print("dist_avoiding = ",dist_avoiding)

        new_target_dist = math.sqrt(dist_target**2+dist_avoiding**2 - 2*dist_target*dist_avoiding*math.cos(deg2rad(orient))) #Re-calculate distnace as crow flies to the target -> cos rule
        beta = 180 - rad2deg(math.asin(dist_target*math.sin(deg2rad(orient))/new_target_dist)) # Angle between new_target_dist and dist_avoiding -> sine rule -> also not its 180 due to quadrants
        phi = beta - 180 # degrees the rover must turn to be facing the target -> remember positive angles are clockwise on the Jankanator, we want to go the opposite here
        print("dist to target = ",dist_target)
        print("Dist avoiding = ",dist_avoiding)
        print("new_target_dist = ", new_target_dist)
        print("orient = ",orient)
        print('BETA = ',beta)
        print('PHI = ',phi)
        inc = 5 # How many steps to break the turn int
        if phi > 45 or phi < -45 : # Break turn into 'inc' increments so that the tracks dont fall off
          turns = np.array([phi/inc for i in range(inc)])
          print(turns)
        else:
          turns = np.array([phi])
        for i in range(len(turns)):
          turn = turns[i].item()
          Motors.turnDegrees(turn,speed = 5)
          time.sleep(1)

        dist_target = new_target_dist # Reinitialise the distance to the target
        orient = 0 # degrees -> Reinitialise the orientation 0 deg is facing the target
        Motors.write(mtr_speed, mtr_speed) # Get on your bike
        target_time0 = time.clock() # Get time that the Jankanator starts moving towards the target again
        target_timer = True # Turn target timer on
        print("Should be moving towards target - start time:",target_time0)
        AVOIDING_TIMER = False # Re-initialise timer so that it can be restarted in the next avoiding stage
    else: # If object has been avoided
      print("STILL NOT AVOIDING")
      Motors.write(mtr_speed, mtr_speed) # Keep on trucking

  elif ultra_dist <= min_obj_Ultradist: # Sense object
    AVOIDING = True
    INITIAL_EVADE = True
    print("AVOIDING")
    Motors.stop() #stop
    if not dist_moved_calc: # if we haven't already calculated the distance moved in the last targetting phase -> do the calculation
      target_time1 = time.clock() # Get the time at which the Jankanator stops moving towards the target
      target_timer = False # Turn target timer off because we aren't moving towards the target anymore
      targetting_time = target_time1 - target_time0 # Time elapsed while moving toward the target
      dist_target = dist_target - (mtr_speed*targetting_time) # Calculate the distance we moved toward the target
      dist_moved_calc = True # We have now done the calc so no need to re-do it on the next iteration
    Motors.turnDegrees(turn_inc) # Turn until no longer facing the object - this turns a set amount and then rechecks on the next iteration
    orient = orient + turn_inc # record orientation wrt to the target - i.e 0 is facing the target