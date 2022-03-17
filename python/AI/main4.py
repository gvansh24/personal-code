import cv2

height = 360
width = 640
xPos = 0
yPos = 0


# def myCallback1(event):
#     global width
#     width = event
# print(event)
def myCallback2(event):
    global height, width
    height = event
    width = int(height * 16 / 9)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # print(event)


def myCallback3(event):
    global xPos
    xPos = event
    # print(event)


def myCallback4(event):
    global yPos
    yPos = event
    # print(event)


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(cv2.CAP_PROP_FPS, 30)
cv2.namedWindow("my trackbar")
cv2.moveWindow("my trackbar", width, 0)
# cv2.createTrackbar("xlen", "my trackbar", 5, width, myCallback1)
cv2.createTrackbar("size", "my trackbar", height, 1000, myCallback2)
cv2.createTrackbar("xpos", "my trackbar", 0, 1366 - 640, myCallback3)
cv2.createTrackbar("ypos", "my trackbar", 0, 330, myCallback4)

while True:

    ignore, frame = cam.read()
    frame = frame[:height, :width]
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", xPos, yPos)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
