from micromelon import *
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
res = (640, 480) # (1280, 720) (1920, 1088)
camera.resolution = res
rawCapture = PiRGBArray(camera)
rc = RoverController()
rc.connectSerial()
#Motors.write(15,0)
Motors.stop()

# while True:
#   rawCapture.truncate(0)
#   camera.capture(rawCapture, format="bgr")
#   image = rawCapture.array
#   print(image)

