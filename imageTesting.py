import numpy
import cv2
from micromelon import *
from pyzbar import pyzbar
#rc = RoverController()
#rc.connectIP() # default is 192.168.4.1
#image = Robot.getImageCapture(IMRES.R640x480)
#image = Robot.getImageCapture(IMRES.R1280x720)

def QRdistance(h):
  # x is width of QR box = 7.1cm
  # w is width of QR rectangle
  # at 40cm from QR -> w = 291
  # at 70cm from QR -> w = 179
  # therefore 30cm = 116px
  #y = -2*10**(-5)*x**3 + 0.0129*x**2 - 3.2978*x + 349.32
  F = 50*274/7.1
  d = 7.1*F/h -8
  return d

#_____________ Code for VIDEO ___________-----
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
## ______________ Code for IMAGES _______________
#while True:
def getQRdist():
  image = Robot.getImageCapture(IMRES.R1920x1088)
  image = image.astype(numpy.uint8)
  barcodes = pyzbar.decode(image)
  #print(type(barcodes)) # returns an empty list if none 
  # loop over the detected barcodes
  for barcode in barcodes:
    # extract the bounding box location of the barcode and draw the
    # bounding box surrounding the barcode on the image
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    print(h)
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
  return QRdistance(h)

# at 40cm from QR -> w = 291 -> 0.1375 cm/px
# at 50cm -> w = 240
# at 60cm -> w = 212
# at 70cm from QR -> w = 179 -> 0.391 cm/px
# at 80cm from QR -> w = 156 -> 0.51 cm /px
# at 100cm from QR -> w = 127 -> 0.78 cm/px
