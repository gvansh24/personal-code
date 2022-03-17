import cv2
import numpy as np

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cam.set(cv2.CAP_PROP_FPS, 30)


def onTrack1(val):
    global hueLow
    hueLow = val


def onTrack2(val):
    global hueHigh
    hueHigh = val


def onTrack3(val):
    global satLow
    satLow = val


def onTrack4(val):
    global satHigh
    satHigh = val


def onTrack5(val):
    global valLow
    valLow = val


def onTrack6(val):
    global valHigh
    valHigh = val


hueLow = 10
hueHigh = 20
satLow = 10
satHigh = 250
valLow = 10
valHigh = 250
height = 360
width = 640

cv2.namedWindow("my Tracker")
cv2.createTrackbar("Hue Low", "my Tracker", 15, 179, onTrack1)
cv2.createTrackbar("Hue High", "my Tracker", 30, 179, onTrack2)
cv2.createTrackbar("Sat Low", "my Tracker", 80, 255, onTrack3)
cv2.createTrackbar("Sat High", "my Tracker", 250, 255, onTrack4)
cv2.createTrackbar("Val Low", "my Tracker", 140, 255, onTrack5)
cv2.createTrackbar("Val High", "my Tracker", 250, 255, onTrack6)
cv2.moveWindow("my Tracker", width, 0)

while True:
    ignore, frame = cam.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])

    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    myMask = cv2.bitwise_not(myMask)
    final = cv2.bitwise_and(frame, frame, mask=myMask)

    contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 200:
            # cv2.drawContours(frame,[contour],0,(255,0,0),3)
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    cv2.imshow("my filter", final)
    cv2.moveWindow("my filter", 0, height)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()