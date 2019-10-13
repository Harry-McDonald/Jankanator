from micromelon import *
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# camera = PiCamera()
# res = (640, 480) # (1280, 720) (1920, 1088)
# camera.resolution = res
# rawCapture = PiRGBArray(camera)
rc = RoverController()
rc.connectSerial()

# ~~~~~~~~~~~ Test image output ~~~~~~~~~
# Motors.write(15,0)
# while True:
#   rawCapture.truncate(0)
#   camera.capture(rawCapture, format="bgr")
#   image = rawCapture.array
#   print(image)

#~~~~~~~~~~~ Display an image
#for i in range(3):
# rawCapture.truncate(0)
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array
# cv2.imshow('Image',image)

# ~~~~~~~ Basic obect avoid algorithn ~~~~~~~~~~~~~
Motors.write(30,30)
for i in range(200):
  dist = Ultrasonic.read() # centimeters
  if dist > 20:
    Motors.write(30,30)
  elif dist < 20:
    Motors.turnDegrees(10)
  time.sleep(0.1)
  
  
# ~~~~~~~~~~~~~~ Stop Motor ~~~~~~~~~~~~
#Motors.stop()




