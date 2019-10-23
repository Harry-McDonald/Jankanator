import numpy
import cv2
from micromelon import *
rc = RoverController()
rc.connectIP() # default is 192.168.4.1
#image = Robot.getImageCapture(IMRES.R640x480)
#image = Robot.getImageCapture(IMRES.R1280x720)

while True:
  image = Robot.getImageCapture(IMRES.R1920x1088)
  image = image.astype(numpy.uint8)
  print("take image")
  #cv2.imshow('image', image)
  #cv2.waitKey(10)
  
