import cv2
import mediapipe as mp

height = 360
width = 640
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

while True:
    ignore, frame = cam.read()
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks is not None:
        for handLandMark in results.multi_hand_landmarks:
            myHand = []
            # mpDraw.draw_landmarks(frame,handLandMark,mp.solutions.hands.HAND_CONNECTIONS)
            for landmark in handLandMark.landmark:
                myHand.append((int(landmark.x*width),int(landmark.y*height)))
            cv2.circle(frame,myHand[20],25,(255,0,0),-1)
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()





