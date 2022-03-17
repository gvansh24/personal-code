import cv2
import time


tlast = time.time()
time.sleep(.5)
fps = 15
height = 360
width = 640

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)


while True:
    dt = time.time() - tlast
    fps = 1 / dt * 0.03 + fps * 0.97
    tlast = time.time()
    ignore, frame = cam.read()
    cv2.putText(frame, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0, 0), 1)
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()