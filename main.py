#import packages
import Jetson.GPIO as GPIO
import cv2
from utils import utils
import signal

#sets pins to use native numbers
GPIO.setmode(GPIO.BOARD)
inpin = 15
outpin = 23
GPIO.setup(inpin,GPIO.IN)
GPIO.setup(outpin,GPIO.OUT)

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    GPIO.output(outpin,0)
    exit(0)
    
signal.signal(signal.SIGINT, keyboardInterruptHandler)
    
#start Infinite loop to look for gpio header button to capture image, obj detect, east(text detect) and ocr(tesseract):
while True:
    x = GPIO.input(inpin)
    #lights up when ready
    GPIO.output(outpin,1)

        
    k = cv2.waitKey(1) & 0xFF
    # press 'q' to exit (if running diagnostics)
    if k == ord('q'):
        GPIO.output(outpin,0)
        break
    if x == 0:
        GPIO.output(outpin,0)
       
        #capture image
        image = utils.imageCap()
        print("img captured")
        
        #object detection
        roi, objname = utils.objDetect(image)  
        print("obj detected")        
        
        #text detection [returns ((startX, startY, endX, endY), text) ]
        text = utils.textDetection(image, roi)
        print("text detected")
        
        #order text
        textstring = utils.orderResults(text)
        print("text reordered")
        print(text)
        
        #read results
        utils.readResults(objname, textstring)
        print("process complete")