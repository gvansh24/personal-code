import cv2
width = 640
height = 360
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)


while True:
    ignore, frame = cam.read()
    frame = cv2.flip(frame,1)
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()





