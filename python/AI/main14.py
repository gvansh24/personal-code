import cv2
import mediapipe as mp

height = 360
width = 640
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils


def parseLandmarks(frame):
    myHands = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks is not None:
        for handLandMark in results.multi_hand_landmarks:
            myHand = []
            for landmark in handLandMark.landmark:
                myHand.append((int(landmark.x * width), int(landmark.y * height)))
            myHands.append(myHand)
    return myHands


paddleWidth = 125
paddleHeight = 15
paddleColor = (0, 0, 0)
ballY = int(height/2)
ballX = int(width/2)
ballHeight = 25
ballWidth = 25
ballColor = (0, 0, 0)
ballSpeedY = 5
ballSpeedX = 5
score = 1

while True:
    ignore, frame = cam.read()
    handData = parseLandmarks(frame)
    for hand in handData:
        cv2.rectangle(frame, (int(hand[8][0] - paddleWidth / 2), 0), (int(hand[8][0] + paddleWidth / 2), paddleHeight),paddleColor,-1)
    cv2.rectangle(frame,(ballX,ballY),(ballX+ballHeight,ballY+ballWidth),ballColor,-1)
    if ballX <= 0 or ballX+ballWidth >= width:
        ballSpeedX *= -1
    if ballY + ballHeight >= height:
        ballSpeedY *= -1
    if ballY < paddleHeight:
        if ballX >= hand[8][0] - paddleWidth / 2 and ballX+ballWidth <= hand[8][0] + paddleWidth / 2:
            ballSpeedY *= -1
            score +=1

            if score%5 == 0:
                ballSpeedY *= 2
                ballSpeedX *= 2
        else:
            break

    ballX += ballSpeedX
    ballY += ballSpeedY

    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
