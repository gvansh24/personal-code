import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cam.set(cv2.CAP_PROP_FPS, 30)

x1 = 200
x2 = 250
y1 = 200
y2 = 250
height = 360
width = 640
ix = 5
iy = 5

while True:
    ignore, frame = cam.read()

    frameROI = frame[x1:x2, y1:y2]
    grayROI = cv2.cvtColor(frameROI, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(grayROI, cv2.COLOR_GRAY2BGR)
    frame[x1:x2, y1:y2] = gray
    cv2.rectangle(frame, (y1, x1), (y2, x2), (0, 255, 0), 2)
    x1 += ix
    x2 += ix
    if x1 <= 0 or x2 >= height:
        ix *= -1
    y1 += iy
    y2 += iy
    if y1 <= 0 or y2 >= width:
        iy *= -1
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
