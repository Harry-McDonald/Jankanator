import numpy
import cv2
from micromelon import *
from pyzbar import pyzbar
import math

def takeImage():
  image = Robot.getImageCapture(IMRES.R1920x1088)
  image = image.astype(numpy.uint8)
  barcodes = pyzbar.decode(image)
  if len(barcodes) == 0:
    return False
  #print(type(barcodes)) # returns an empty list if none 
  # loop over the detected barcodes
  for barcode in barcodes:
    # extract the bounding box location of the barcode and draw the
    # bounding box surrounding the barcode on the image
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    print(h)

    points = barcodes.polygon
    pts = np.array(points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    # the barcode data is a bytes object so if we want to draw it on
    # our output image we need to convert it to a string first
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw the barcode data and barcode type on the image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
      0.5, (0, 0, 255), 2)
        # show the output image
  cv2.imshow("Image", image)
  cv2.waitKey(0)
  barcode_data = {'x':x,'y':y,'w':w,'h':h,'x11':points[0][0], 'y11':points[0][1],'x12':points[3][0],'y12':points[3][1],'x21':points[1][0],'y21':points[1][1],'x22':points[2][0],'y22':points[2][1]}

  return barcode_data
     

def getQRdist(data):
  delta_y_left = data['y11']-data['y21']
  delta_y_right = data['y12']-data['y22']
  h = (delta_y_left+delta_y_right)/2
  F = 50*274/7.1
  d = (7.1*F/h)-8
  return d

def getAngle(data):
  #x11 = data['x11']
  x12 = data['x12']
  #x21 = data['x21']
  x22 = data['x22']
  #y11 = data['y11']
  y12 = data['y12']
  #y21 = data['y21']
  y22 = data['y22']
  dist = getQRdist(data)
  zpx = (1920/2-(x12+x22)/2) # distance from image center to QR center in pixels
  h_QR = 7.1 #cm
  L = math.sqrt((x22-x12)^2+(y22-y12)^2)
  cm2px = h_QR/dist
  z_cm = zpx*cm2px
  theta = math.atan(z_cm/dist)
  return theta

  



