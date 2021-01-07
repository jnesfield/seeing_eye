#inspired by https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/
####################################################
#import packages
####################################################
from imutils.object_detection import non_max_suppression
import cv2 as cv2
import sys
import numpy as np
import os.path
import pytesseract
import pyttsx3
from pandas import DataFrame
import math

####################################################
#define base functions:
####################################################
#image capture
####################################################
def imageCap():
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    cap.release()
    
    return img

####################################################
#object detection
####################################################
# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, confThreshold, nmsThreshold):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        
    return boxes, classIds, confidences, indices 

def centerIndex(boxes, xcenter, ycenter):
    for i in range(len(boxes)):
        left, top, width, height = boxes[i]
        right = left + width
        bottom = top + height
        if left < xcenter and right > xcenter:
            if top < ycenter and bottom > ycenter:
                return i
            else:
                continue
        else:
            continue
     
def objDetect(image):
    # Initialize the parameters
    confThreshold = 0.5  #Confidence threshold
    nmsThreshold = 0.4   #Non-maximum suppression threshold
    inpWidth = 416       #Width of network's input image
    inpHeight = 416      #Height of network's input image
    
    # Load names of classes
    classesFile = r"~/seeing_eye/coco_names/coco.names"
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
        
    # Give the configuration and weight files for the model and load the network using them.
    modelConfiguration = r"~/seeing_eye/frozen_models/coco/yolov3.cfg"
    modelWeights = r"~/seeing_eye/frozen_models/coco/yolov3.weights"

    #load model
    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        
    #resize image
    orig = image.copy()
    (H, W) = image.shape[:2]
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (inpWidth, inpHeight)
    rW = W / float(newW)
    rH = H / float(newH)
    
    #determine image center
    xcenter = inpWidth/2
    ycenter = inpHeight/2   

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(image, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    
    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))

    # Remove the ROI with low confidence
    #boxes = [left, top, width, height]
    boxes, classIds, confidences, indices = postprocess(image, outs, confThreshold, nmsThreshold)
    
    #determine which indices from boxes is center of image
    centeridx = centerIndex(boxes, xcenter, ycenter)
    
    #check if centerObjName is Nonetype, if so, no object detected (force obj to say "no obj detected", and define roi as whole image
    if centeridx is None:
        centerObjName = "no object detected "
        roi = [0, 0, W, H]
        return roi, centerObjName
    
    #capture class name for object in center and coordinates
    centerObjName = classes[classIds[centeridx]]
    roi = boxes[centeridx]
    
    #convert roi to original image size
    l1, t1, w1, h1 = roi
    l2 = l1 * rW
    t2 = t1 * rH
    w2 = w1 * rW
    h2 = h1 * rH
    
    #new list with roi
    roi = [l2, t2, w1, h1]
    
    
    return roi, centerObjName
 
####################################################
#text detection and ocr
#################################################### 
def textDetection(image, roi):
    #define padding The (optional) amount of padding to add to each ROI border. You might try values of 0.05 for 5% or 0.10 for 10% (and so on) if you find that your OCR result is incorrect.
    padding = 0.05
    
    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    
    # load the pre-trained EAST text detector
    net = cv2.dnn.readNet(r"~/seeing_eye/frozen_models/east/frozen_east_text_detection.pb")
    
    #image preprocessing
    #crop roi from image
    y  = int(roi[1])
    y2 = int(roi[1]+roi[3]+1)
    x  = int(roi[0])
    x2 = int(roi[0]+roi[2]+1)
    
    if y == 0:
        y = 1
    if x == 0:
        x = 1
        
    if roi is None:
        (H, W) = image.shape[:2]
        y  = 1
        y2 = H
        x  = 1
        x2 = W
    
    image = image[y:y2, x:x2]
    orig = image.copy()
    (H, W) = image.shape[:2]
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    
    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < 0.5:
                continue
            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
            
    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes - contains coordinates for regions of interest containing identified text
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    #crop image using boxes roi defs and send for tesseract ocr:
    # initialize the list of results
    results = []
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * padding)
        dY = int((endY - startY) * padding)
        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))
        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]
        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)
        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))
    
    return results
    
####################################################
#order results in text detection for reading
####################################################
def column(matrix, i):
    return [row[i] for row in matrix]
    
def fixResults(results):
    data = []
    for i in range(len(results)):
        startX, startY, endX, endY = column(results,0)[i]         
        text = column(results,1)[i]
        data.append([text, startX, startY, endX, endY])
        
    dataFrame = DataFrame(data, columns = ['text', 'startX', 'startY', 'endX', 'endY'])
    
    return dataFrame
  
def orderResults(text):
    fixedResults = fixResults(text)
    fixedResults.sort_values(by = ['startX', 'startY'], inplace = True)
    
    textOut = ""
    for i in range(len(fixedResults)):
        textOut += (fixedResults['text'][i] + " ")
        
    return textOut
       
    

####################################################
#read text results
####################################################  
def readResults(objname, text):

    engine = pyttsx3.init()
    #set voice rate to slower than normal
    newVoiceRate = 95
    engine.setProperty('rate',newVoiceRate)
    #set volume
    engine.setProperty('volume', 0.95)  # Volume 0-1
    
    #assemble string
    string = "the object infront of you is a" + objname + " it says" + text
    
    #say string
    engine.say(string)
    engine.runAndWait()
    
