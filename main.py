#import packages
import Jetson.GPIO as GPIO
import cv2
from utils import utils
import signal
import os



#os.system(r"pulseaudio --start")
os.system(r"pactl set-default-sink 'alsa_output.usb-C-Media_Electronics_Inc._USB_Audio_Device-00.analog-stereo'")
os.system(r"pactl set-sink-volume 0 90")

#sets pins to use native numbers
GPIO.setmode(GPIO.BOARD)
inpin1 = 15
inpin2 = 29
GPIO.setup(inpin1,GPIO.IN)
GPIO.setup(inpin2,GPIO.IN)

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

#say ready when device is ready
os.system(r'speaker-test -c2 -t sine')


#start Infinite loop to look for gpio header button to capture image, obj detect, east(text detect) and ocr(tesseract):
while True:
    x = GPIO.input(inpin1)
    y = GPIO.input(inpin2)
    
    
    k = cv2.waitKey(1) & 0xFF
    # press 'q' to exit (if running diagnostics)
    if k == ord('q'):
        break
    if x == 0:
               
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
        
    if y == 0:
        #turns off machine if other button pressed, not working at this time, need to research
