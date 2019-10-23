import numpy
import cv2
from micromelon import *
from pyzbar import pyzbar
rc = RoverController()
rc.connectIP() # default is 192.168.4.1
#image = Robot.getImageCapture(IMRES.R640x480)
#image = Robot.getImageCapture(IMRES.R1280x720)

# cap = cv2.VideoCapture(0)

# while True:
#  # Take each frame
#   image = cap.read()
#   barcodes = pyzbar.decode(image)

#   # loop over the detected barcodes
#   for barcode in barcodes:
#     # extract the bounding box location of the barcode and draw the
#     # bounding box surrounding the barcode on the image
#     (x, y, w, h) = barcode.rect
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

#     # the barcode data is a bytes object so if we want to draw it on
#     # our output image we need to convert it to a string first
#     barcodeData = barcode.data.decode("utf-8")
#     barcodeType = barcode.type

#     # draw the barcode data and barcode type on the image
#     text = "{} ({})".format(barcodeData, barcodeType)
#     cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
#       0.5, (0, 0, 255), 2)

#   # show the output image
#   cv2.imshow("Image", image)
#   cv2.waitKey(0)
#   time.sleep(1)

#while True:
image = Robot.getImageCapture(IMRES.R1920x1088)
image = image.astype(numpy.uint8)
barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:
  # extract the bounding box location of the barcode and draw the
  # bounding box surrounding the barcode on the image
  (x, y, w, h) = barcode.rect
  cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

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

    #print("take image")
    #cv2.imshow('image', image)
    #cv2.waitKey(10)