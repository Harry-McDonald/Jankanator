from micromelon import *
import math
#from picamera.array import PiRGBArray
#from picamera import PiCamera
from timeit import default_timer as timer
import time
import cv2
import time
import numpy as np
import timeit
from pyzbar import pyzbar
import imageTester as IT


rc = RoverController()
rc.connectIP()

# ~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~
def angleAdjust(dist_target):
  QR_FOUND = True
  image_data = IT.takeImage()
  if image_data == []:
    QR_FOUND = False
    final_dist = dist_target
  elif QR_FOUND:
    dist_target = IT.getQRdist(image_data) #cm
    theta = IT.getAngle(image_data)
    print("theta1 = ",theta)
    Motors.turnDegrees(theta)
    time.sleep(1)
  time.sleep(2)
  print("QR FOUND from angle = ",QR_FOUND)
  return (QR_FOUND,dist_target)

def findQR(turn_direction = None, dist_target = 200):
  orient = 0
  TURN_BACK = False
  MOVE_FORWARD = False
  QR_SEARCHED = False
  if turn_direction == "right" or turn_direction == None:
    turn_inc = -30
  elif turn_direction == "left":
    turn_inc = 30
  QR_FOUND = angleAdjust(dist_target)
  print(QR_FOUND)
  while QR_FOUND[0] == False:
    if QR_SEARCHED == True:
      orient = 0
      turn_inc = -turn_inc     
      break
    turnDeg(turn_inc)
    dist_moved = 0
    ultra_dist = Ultrasonic.read() # centimeters
    #Motors.turnDegrees(turn_inc) # Turn until no longer facing the object - this turns a set amount and then rechecks on the next iteration
    orient = orient + turn_inc # record orientation wrt to the target - i.e 0 is facing the target    
    time.sleep(1)
    QR_FOUND = angleAdjust(dist_target)
    if abs(orient) >= 60 and TURN_BACK == False:
      turn_inc = -turn_inc
      TURN_BACK = True
      orient = 0
    elif MOVE_FORWARD == True:
      if abs(orient) >= 60:
        print("\ncheck done\n")
        QR_SEARCHED = True
        while ultra_dist > 30 and dist_moved < 60:
          print("\ncheck done done\n")
          ultra_dist = Ultrasonic.read()
          Motors.moveDistance(15)
          dist_moved += 15
          time.sleep(2)
        MOVE_FORWARD = False
    elif TURN_BACK == True:
      turnDeg(turn_inc*3)
      # if abs(orient)>=120:
      turn_inc = -turn_inc
      MOVE_FORWARD = True
      orient = 0
  return QR_FOUND[1]

def deg2rad(degrees):
  rads = degrees*math.pi/180
  return rads

def rad2deg(rads):
  degs = rads*180/math.pi
  return degs

def checkSet():
  image_data = IT.takeImage()
  if image_data == []:
    print("return")
    return
  theta = IT.getAngle(image_data)
  print("theta1 = ",theta)
  Motors.turnDegrees(theta)
  time.sleep(4)

def turnDeg(degrees_fake):
    if degrees_fake > 0:
        degrees = degrees_fake*(1/1.1)
        turns = int((degrees - degrees%15)/15)
        #print("turns = ",turns)
        small_turn = degrees%15
        #print("small turn",small_turn)
        for turn in range(turns):
            Motors.moveDistance(-3)
            time.sleep(0.5)
            Motors.moveDistance(3)
            time.sleep(0.5)
            Motors.turnDegrees(15,speed=15)
            time.sleep(1)
            turn+=1
            #print("in for loop1")
        Motors.turnDegrees(small_turn,speed=20)
    else:
        degrees = abs(degrees_fake*(1/1.1))
        turns = int((degrees - degrees%15)/15)
        #print(turns)
        small_turn = degrees%15
        #print(small_turn)
        for turn in range(abs(turns)):
            Motors.moveDistance(-3)
            time.sleep(0.5)
            Motors.moveDistance(3)
            time.sleep(0.5)
            Motors.turnDegrees(15,speed=15, reverse = True)
            time.sleep(1)
            turn+=1
            #print("in for loop2")
        Motors.turnDegrees(small_turn,speed=20, reverse = True)

# def QRdistance(h):
#   F = 50*274/7.1
#   d = 7.1*F/h -8
#   return d

# Initial states
AVOIDING = False # Status of the Jankanator while it is avoiding an object
target_timer = False # Timer used to record time elapsed while moving in the avoiding stage -> Initialise to off
AVOIDING_TIMER = False # Timer used to record time elapsed while moving towards target -> Initialise to off
dist_moved_calc = False # Initialise
INITIAL_EVADE = False # When an object is sensed the first manouever is to move 10cm in the clear direction and then run checks on the left ir
QR_FOUND = True # initialise as true
ULTRA_ON = True
TAKE_PHOTO = True
HEAD_HOME = False
CHOOSE_IR = "LEFT"
IR_CHOSEN = False
QR_SEARCHED = False

# initialise variables
mtr_speed = 8 #cm/s
turn_inc = 15 #degrees
min_obj_IRdist = 50 #cm
min_obj_Ultradist = 30 #cm
evade_dist = 10 #cm
final_dist = 150
dist_target = final_dist # Initialise the distance from the Jankanator to the flagpole


# if doesnt work pass in final_dist to the function
dist_target = findQR(None,dist_target)
#angleAdjust(dist_target)

# Initialise orientation, turning increment
orig_orient = 0 # degrees -> Facing the target
orient = orig_orient #initialise

# Start engine
Motors.write(mtr_speed, mtr_speed)
target_time0 = timer() # Get the time the Jankanator starts moving towards the target
gunning_time = timer()
print("Started moving to the target at: ",target_time0)
target_timer = True # Turn target timer on
#Begin algorithm
while True:
  if HEAD_HOME == True:
    Motors.moveDistance(-7)
    time.sleep(2)
    print("Turn 180")
    turnDeg(180)
    print("head home FALSE")
    HEAD_HOME = False
    dist_target = findQR(None,dist_target)
  
  print("\n dist_target = ", dist_target,"\n")
  if dist_target >= 80:
    photo_interval = 2.5
  else:
    photo_interval = 1
  
  if timer()-gunning_time > photo_interval and TAKE_PHOTO == True:
    print("VIBE CHECK")
    Motors.stop()
    QR_FOUND = angleAdjust(dist_target)
    dist_target = QR_FOUND[1]
    gunning_time = timer()
    if QR_FOUND[0] == None:
      findQR(dist_target)
    
  # if dist_target<min_obj_Ultradist+10:
  #   ULTRA_ON = False
  #   HEAD_HOME = True
  #   Motors.moveDistance(dist_target-4)
  #   print("we're going dbah")

  ultra_dist = Ultrasonic.read() # centimeters
  ir_distL = IR.readLeft() #cm
  ir_distR = IR.readRight() #cm
  print("ir_dist_measured = ", ir_distL)

  #print("Ultra dist = ",ultra_dist)
  #print("IR dist Left = ",ir_distL)

  if dist_target <= min_obj_Ultradist + 20:
    print("we're going dbah")
    IR_OFF = True
    Motors.stop()
    Motors.moveDistance(dist_target+5)
    time.sleep(2)
    HEAD_HOME = True

  
  if CHOOSE_IR == "LEFT":
    ir_dist = ir_distL
    print("we chose LEFT = ", ir_dist)
  elif CHOOSE_IR == "RIGHT":
    ir_dist = ir_distR
    print("we chose RIGHT = ", ir_dist)

  if ultra_dist > min_obj_Ultradist: #Enter if there is no object infront of Jankanator
    if AVOIDING: # Check if we are in the avoiding stage
      TAKE_PHOTO = False
      print("avoiding")
      if INITIAL_EVADE:
        print("initial evade")
        Motors.stop()
        Motors.turnDegrees(turn_inc)
        orient = orient + turn_inc
        time.sleep(2)
        Motors.moveDistance(evade_dist,mtr_speed,mtr_speed)
        dist_avoiding = evade_dist
        time.sleep(2) # adjustable when optimising -> could make a min sleep function that determines time needed to move based on mtr_speed
        INITIAL_EVADE = False # We have finished our initial move - next iteration should check if there is a object on our left
      elif ir_dist < min_obj_IRdist:  #Check left IR sensor to see if it is next to an object -> if true we are still in the avoiding stage

        print("ir is LESS = ",ir_dist)
        #print('Object on my left')
        #Motors.move(mtr_speed, mtr_speed) # Keep moving until clear
        Motors.moveDistance(5)
        dist_avoiding += 3
        time.sleep(1)
        # if not AVOIDING_TIMER: # if avoiding timer hasn't already been set -> set it
        #   avoiding_time0 = timer() # Get time when motors start in AVOIDING mode
        #   print("started avoiding at: ",avoiding_time0)
        #   #print("Timer0 set")
        #   AVOIDING_TIMER = True # Record that avoiding timer has been set in this avoiding iteration
      else: # If we have cleared the object
        #print('STOP AVOIDING')
        #TAKE IMAGE AND FIND TARGET
        print("START TURNING TOWARDS IR")
        Motors.stop()
        AVOIDING = False # No longer avoiding
        IR_CHOSEN = False

        TAKE_PHOTO = True
        dist_moved_calc = False # Reinitialise until next avoiding stage
        avoiding_time1 = timer() # Get time when Jankanator has finished avoiding
        gunning_time = timer()
        print("stopped avoiding at: ",avoiding_time1)

        # if AVOIDING_TIMER: # check if extra avoiding was necessary
        #   time_avoiding = avoiding_time1 - avoiding_time0 # Total time elapsed while avoiding
        #   print("total elapsed avoiding: ",time_avoiding)
        #   # print("time 0 = ", avoiding_time0)
        #   # print("time 1 = ", avoiding_time1)
        #   # print("time_avoiding",time_avoiding)
        #   dist_avoiding = evade_dist + time_avoiding * mtr_speed # cm
        #   print("dist_avoiding = ",dist_avoiding)
        # else: # if no extra avoiding was necessary
        #   dist_avoiding = evade_dist
        #   #print("dist_avoiding = ",dist_avoiding)

        new_target_dist = math.sqrt(dist_target**2+dist_avoiding**2 - 2*dist_target*dist_avoiding*math.cos(deg2rad(orient))) #Re-calculate distnace as crow flies to the target -> cos rule
        beta = 180 - rad2deg(math.asin(dist_target*math.sin(deg2rad(orient))/new_target_dist)) # Angle between new_target_dist and dist_avoiding -> sine rule -> also not its 180 due to quadrants
        phi = beta - 180 # degrees the rover must turn to be facing the target -> remember positive angles are clockwise on the Jankanator, we want to go the opposite here
        print("phi = ",phi)
        if phi < 0:
          turn_direction = "left"
          print("turn_direction = ", turn_direction)
        else:
          turn_direction = "right"
        inc = 5 # How many steps to break the turn int
        if phi > 45 or phi < -45 : # Break turn into 'inc' increments so that the tracks dont fall off
          turns = np.array([phi/inc for i in range(inc)])
          print(turns)
        else:
          turns = np.array([phi])
        for i in range(len(turns)):
          turn = turns[i].item()
          Motors.turnDegrees(turn,30)
          time.sleep(1)
        #turnDeg(phi)
        
        dist_target = findQR(turn_direction,dist_target) # search algorithm to find QR
        
        #angleAdjust(dist_target)
        #dist_target = new_target_dist # Reinitialise the distance to the target
        orient = 0 # degrees -> Reinitialise the orientation 0 deg is facing the target
        dist_avoiding = 0 # re-initialse dist_avoiding
        #Motors.write(mtr_speed, mtr_speed) # Get on your bike
        target_time0 = timer() # Get time that the Jankanator starts moving towards the target again
        target_timer = True # Turn target timer on
        print("Started moving toward target again: ",target_time0)
        AVOIDING_TIMER = False # Re-initialise timer so that it can be restarted in the next avoiding stage
    else: # If object has been avoided
      Motors.write(mtr_speed, mtr_speed) # Keep on trucking

  elif ultra_dist <= min_obj_Ultradist and ULTRA_ON == True:# and not IR_OFF: # Sense object
    if IR_CHOSEN == False:
      if ir_distL <= ir_distR:
        turn_inc = 20
        CHOOSE_IR = "LEFT"
      else:
        turn_inc = -20
        CHOOSE_IR = "RIGHT"
    print("IR has been chosen")
    IR_CHOSEN = True
    AVOIDING = True
    INITIAL_EVADE = True
    Motors.stop() #stop
    if not dist_moved_calc: # if we haven't already calculated the distance moved in the last targetting phase -> do the calculation
      QR_FOUND = angleAdjust(dist_target)
      dist_target = QR_FOUND[1]
      TAKE_PHOTO = False
      # target_time1 = timer() # Get the time at which the Jankanator stops moving towards the target
      # print("Stopped moving toward target: ",target_time1)
      # target_timer = False # Turn target timer off because we aren't moving towards the target anymore
      # targetting_time = target_time1 - target_time0 # Time elapsed while moving toward the target
      # print("Time spent moving toward target: ",targetting_time)
      # dist_target = dist_target - (mtr_speed*targetting_time) # Calculate the distance we moved toward the target
      # print("dist moving to target = ",mtr_speed*targetting_time)
      dist_moved_calc = True # We have now done the calc so no need to re-do it on the next iteration
    #turnDeg(turn_inc)
    Motors.turnDegrees(turn_inc,30) # Turn until no longer facing the object - this turns a set amount and then rechecks on the next iteration
    time.sleep(1)
    orient = orient + turn_inc # record orientation wrt to the target - i.e 0 is facing the target