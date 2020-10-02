import cv2
import numpy as np
import keyboard

#Virtual painting

#First we need to capture our cam

#Set the size
frameWidth = 1200
frameHeight = 800

#Capture webcam
cap = cv2.VideoCapture(0)  # capture from default  webcam
cap.set(3, frameWidth)  # set the Width
cap.set(4, frameHeight)  # set the Height
#cap.set(10, 10)  # set the brightness


myColors = [[153, 215, 125, 179, 255, 255]]
myColorsValues = [[0, 0, 255]]


#We have to find the  colors
def findColor(img, myColors, myColorsValues, drawPoints):
    #convert the img into HSV base
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # loop through the colors
    for color, colorValue in zip(myColors, myColorsValues):
        # lower and upper boundings for color
        lower = np.array(myColors[0][:3])
        upper = np.array(myColors[0][3:])

        #create a mask for that color
        mask = cv2.inRange(imgHSV, lower, upper)

        # Now for each detected mask we have to find where is the object in the image
        cntCenters = getContours(mask, colorValue)

        for center in cntCenters:

            x = center[0]
            y = center[1]

            #Draw a circle on the center of the contour
            #cv2.circle(imgResult, (x, y), 5, colorValue, cv2.FILLED)

            drawPoints.append([x, y, colorValue])

    return drawPoints



def getContours(img, colorValue):

    # min area
    minArea = 100

    # img, method to find/finds external corners, get all the contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    x, y, w, h = 0, 0, 0, 0

    cntCenters = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        #we set a minimal threshold for the area so it does not detect any noise as a shape
        if area > minArea:
            #Draw the contours
            cv2.drawContours(imgResult, cnt, -1, colorValue, 3)  # image, contours, all contours  = -1, color, thickness

            #now we want to aproximate the corners of our shapes
            #calculate the perimeter
            peri = cv2.arcLength(cnt, True)  #curve, its the curve closed? arclength = longitud del arco

            # aproximate the corners of the shape, if we get 3 corners > triangle, 4>square, and so on
            aprox = cv2.approxPolyDP(cnt, 0.02*peri, True) #curve, tweakable hyperparameter, its closed?

            #creates a bounding box around the points
            x, y, w, h = cv2.boundingRect(aprox)

            cntCenters.append([x+w//2, y])

    return cntCenters


def draw(myPoints):

    if myPoints == []:
        return
    else:

        initialPoint = myPoints[0]

        for finalPoint in myPoints[1:]:

            cv2.line(imgResult, (initialPoint[0], initialPoint[1]), (finalPoint[0], finalPoint[1]), finalPoint[2], 3)

            initialPoint = finalPoint

drawPoints = []

while True:
    success, img = cap.read()

    #We will paint all the information in this image
    imgResult = img.copy()

    drawPoints = findColor(img, myColors, myColorsValues, drawPoints)

    draw(drawPoints)

    imgResult = cv2.flip(imgResult, 1)

    imgResult = cv2.putText(imgResult, 'Q: quit  R: reset', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    
    cv2.imshow("Video", imgResult)

    if cv2.waitKey(1) & keyboard.is_pressed('q'):  # pressing q will quit the display
        break

    if cv2.waitKey(1) & keyboard.is_pressed('r'):  # restart canvas
        drawPoints = []





