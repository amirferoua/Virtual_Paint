import cv2
import numpy as np

def empty(a):
    pass


#color detection



#now we have to define some values between we want our color to be.
# but we dont know what values are. so we will define some trackbars to obtain the
# optimal minimun and maximun value of our color
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)  #name, which window, initial val, max value,
                                                           # function that runs when something changes
cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 153, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

#PLAYING WITH THE TRACKBARS LEAD US TO THE NUMBERS 0, 19, 110, 240, 153, 255 FOR OUR ORANGE

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()
    #convert image to HSV base
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")


    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHSV, lower, upper)

    #this function checks where we have white pixels and changes them for the original colors
    imgResult = cv2.bitwise_and(img, img, mask = mask)

    cv2.imshow('original', img)
    cv2.imshow('imgHSV', imgHSV)
    cv2.imshow('mask', mask)
    cv2.imshow('imgResult', imgResult)
    cv2.waitKey(1)