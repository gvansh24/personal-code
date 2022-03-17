import cv2
import numpy as np

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cam.set(cv2.CAP_PROP_FPS, 30)
# cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

faceCascade = cv2.CascadeClassifier("haar/haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("haar/haarcascade_eye.xml")
while True:
    ignore, frame = cam.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(grey, 1.3, 5)
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
    eyes = eyeCascade.detectMultiScale(grey,1.3,5)
    for eye in eyes:
        x, y, w, h = eye
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
