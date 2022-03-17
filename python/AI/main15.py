import cv2
import mediapipe as mp

height = 360
width = 640
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

hands = mp.solutions.hands.Hands()
mpDraw = mp.solutions.drawing_utils


def parseHandLandmarks(frame):
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
    return myHands,myHandsType


while True:
    ignore, frame = cam.read()
    frame = cv2.flip(frame, 1)
    handsData,handsType = parseHandLandmarks(frame)
    for Hdata,Htype in zip(handsData,handsType):
        print(Htype)
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
