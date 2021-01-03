#import packages
import Jetson.GPIO as GPIO
import cv2
from utils import utils


#sets pins to use native numbers
GPIO.setmode(GPIO.BOARD)
inpin = 15
GPIO.setup(inpin,GPIO.IN)
x = GPIO.input(15)


#start Infinite loop to look for gpio header button to capture image, obj detect, east(text detect) and ocr(tesseract):
while True:
    x = GPIO.input(inpin)
    k = cv2.waitKey(1) & 0xFF
    # press 'q' to exit (if running diagnostics)
    if k == ord('q'):
        break
    if x == 0:
       
        #capture image
        image = utils.imageCap()
        
        #object detection
        roi, objname = utils.objDetect(image)     
        
        #text detection [returns ((startX, startY, endX, endY), text) ]
        text = utils.textDetection(image, roi)
        
        #order text
        textstring = utils.orderResults(text)
        
        #read results
        utils.readResults(objname, textstring)