from micromelon import *
from micromelon.comms_constants import MicromelonType as OPTYPE
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

def tacho2distance(tacho):
    left_wheel_deg = (((tacho[0])/255)*360 + ((tacho[1]))*360 + ((tacho[2])*360*360))
    right_wheel_deg = (((tacho[3])/255)*360 + ((tacho[4]))*360 + ((tacho[5])*360*360))
    left_wheel_revs = left_wheel_deg/360
    distance = left_wheel_revs*4*math.pi -14
    return distance

# target_dist0 = tacho2distance(rc.readAttribute(OPTYPE.MOTOR_TACHO))
# target_time0 = timer()
# #Motors.moveDistance(110)

# Motors.write(10,10,5)
# target_dist1 = tacho2distance(rc.readAttribute(OPTYPE.MOTOR_TACHO))
# target_time1 = timer()

# distance = target_dist1 - target_dist0
# time = target_time1-target_time0
# dist_travelled = 10*time
# print(time)
# print(distance)
# print("dist travelled = ", dist_travelled)


def turnCunt(degrees_fake):
    if degrees_fake > 0:
        degrees = degrees_fake*(1.1/1)
        turns = int((degrees - degrees%15)/15)
        print(turns)
        small_turn = degrees%15
        print(small_turn)
        for turn in range(turns):
            if turn%3 == 0:
                Motors.moveDistance(-3)
                time.sleep(0.5)
                Motors.moveDistance(3)
                time.sleep(0.5)
            Motors.turnDegrees(15,speed=10)
            time.sleep(1)
            turn+=1
        Motors.turnDegrees(small_turn,speed=10)
    else:
        degrees = abs(degrees_fake*(1.1/1))
        turns = int((degrees - degrees%15)/15)
        print(turns)
        small_turn = degrees%15
        print(small_turn)
        for turn in range(abs(turns)):
            if turn%3 == 0:
                Motors.moveDistance(-3)
                Motors.moveDistance(3)
            Motors.turnDegrees(15,speed=10, reverse = True)
            time.sleep(1)
            turn+=1
        Motors.turnDegrees(small_turn,speed=30, reverse = True)

turnCunt(180)

#distance = IT.getQRdist(IT.takeImage())


