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
    myHandsType = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks is not None:
        for hand in results.multi_handedness:
            myHandType = hand.classification[0].label
            myHandsType.append(myHandType)
        for handLandMark in results.multi_hand_landmarks:
            myHand = []
            for landmark in handLandMark.landmark:
                myHand.append((int(landmark.x * width), int(landmark.y * height)))
            myHands.append(myHand)
    return myHands, myHandsType


paddleWidth = 25
paddleHeight = 150
paddleColorLeft = (255, 0, 0)
paddleColorRight = (0, 0, 255)
ballY = int(height / 2)
ballX = int(width / 2)
ballHeight = 25
ballWidth = 25
ballColor = (0, 0, 0)
ballSpeedY = 5
ballSpeedX = 5
scoreLeft = 1
scoreRight = 1

while True:
    ignore, frame = cam.read()
    frame = cv2.flip(frame, 1)
    ballX += ballSpeedX
    ballY += ballSpeedY
    handData, handType = parseLandmarks(frame)
    for hData, hType in zip(handData, handType):
        if hType == "Right":
            cv2.rectangle(frame, (width - paddleWidth, int(hData[8][1] - paddleHeight / 2)),
                          (width, int(hData[8][1] + paddleHeight / 2)), paddleColorRight, -1)
        if hType == "Left":
            cv2.rectangle(frame, (0, int(hData[8][1] - paddleHeight / 2)),
                          (paddleWidth, int(hData[8][1] + paddleHeight / 2)), paddleColorLeft, -1)

    cv2.rectangle(frame, (ballX, ballY), (ballX + ballHeight, ballY + ballWidth), ballColor, -1)
    cv2.putText(frame,str(scoreRight),(paddleWidth*20,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(paddleColorRight))
    cv2.putText(frame,str(scoreLeft),(paddleWidth*4,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,paddleColorLeft)
    if ballY <= 0 or ballY + ballHeight >= height:
        ballSpeedY *= -1
    if ballX <= paddleWidth:
        if hData[8][1] - paddleHeight / 2 <= ballY <= hData[8][1] + paddleHeight / 2:
            ballSpeedX *= -1
        else:
            ballX = int(width/2)
            ballY = int(height/2)
            scoreRight += 1
    if ballX+ballWidth >= width - paddleWidth:
        if int(hData[8][1] - paddleHeight / 2) <= ballY <= int(hData[8][1] + paddleHeight / 2):
            ballSpeedX *= -1
        else:
            ballX = int(width/2)
            ballY = int(height/2)
            scoreLeft += 1
    if scoreLeft % 5 == 0 or scoreRight % 5 == 0:
        ballSpeedY *= 2
        ballSpeedX *= 2
    # else:
    # break

    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
