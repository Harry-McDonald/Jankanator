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
data = IT.takeImage()
dist = IT.getQRdist(data)
print("dist = ",dist)
angle = IT.getAngle(data)
print("theta = ", angle)

# phi = [360/8 for i in range(8)]
# print(phi)
# for i in phi:
#   Motors.turnDegrees(i)

