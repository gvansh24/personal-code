import cv2
import mediapipe as mp
import numpy
import numpy as np

width = 640
height = 360
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

hands = mp.solutions.hands.Hands()
pose = mp.solutions.pose.Pose()
findFace = mp.solutions.face_detection.FaceDetection()
findFaceMesh = mp.solutions.face_mesh.FaceMesh()

mpDraw = mp.solutions.drawing_utils
drawSpecLine = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 0, 255))
drawSpecCircle = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0))


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
    return myHands, myHandsType


def parsePoseLandmarks(frame):
    myPose = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frameRGB)
    if results.pose_landmarks is not None:
        for landmark in results.pose_landmarks.landmark:
            myPose.append((int(landmark.x * width), int(landmark.y * height)))
    return myPose


def parseFaceLandmarks(frame):
    myFaces = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = findFace.process(frameRGB)
    if results.detections is not None:
        for face in results.detections:
            # drawFace.draw_detection(frame,face)
            bBox = face.location_data.relative_bounding_box
            topLeft = (int(bBox.xmin * width), int(bBox.ymin * height))
            bottomRight = (int((bBox.xmin + bBox.width) * width), int((bBox.ymin + bBox.height) * height))
            # cv2.rectangle(frame, topLeft, bottomRight, (255, 0, 0), 3)
            myFaces.append((topLeft, bottomRight))
    return myFaces


def parseFaceMeshLandmarks(frame):
    myFacesMesh = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = findFaceMesh.process(frameRGB)
    if results.multi_face_landmarks is not None:
        for faceMesh in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(frame, faceLandMarks, mp.solutions.face_mesh.FACEMESH_TESSELATION, drawSpecLine,
            #                       drawSpecCircle)
            myFaceMesh = []
            for lm in faceMesh.landmark:
                # cv2.putText(frame, str(indx), (int(lm.x * width), int(lm.y * height)), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                #             (255, 0, 0), )
                loc = (int(lm.x * width), int(lm.y * height))
                myFaceMesh.append(loc)
            myFacesMesh.append(myFaceMesh)
    # mpDraw.draw_landmarks(frame,faceMesh)
    return myFacesMesh


def findDistances(handData):
    distMatrix = np.zeros([len(handData), len(handData)], dtype="float")
    palmSize =  ((handData[0][0] - handData[9][0]) ** 2 + (handData[0][1] - handData[9][1]) ** 2) ** (1. / 2.)
    for row in range(0, len(handData)):
        for col in range(0, len(handData)):
            distMatrix[row][col] = (((handData[row][0] - handData[col][0]) ** 2 + (handData[row][1] - handData[col][1]) ** 2) ** (1. / 2.))/palmSize
    return distMatrix


def findError(gestMatrix, unknownMatrix, keyPoints):
    error = 0
    for row in keyPoints:
        for col in keyPoints:
            error = error + abs(gestMatrix[row][col] - unknownMatrix[row][col])
    return error


def findGesture(unknownGesture, knownGesture, keyPoints, gestName, tol):
    errorArray = []
    for i in range(0, len(gestName)):
        error = findError(knownGesture[i], unknownGesture, keyPoints)
        errorArray.append(error)
    errorMin = errorArray[0]
    minIndex = 0
    for i in range(0, len(errorArray)):
        if errorArray[i] <= errorMin:
            errorMin = errorArray[i]
            minIndex = i
    if errorMin < tol:
        gesture = gestName[minIndex]
    else:
        gesture = "unknown"
    return gesture


keyPoints = [0, 4, 5, 9, 13, 17, 8, 12, 16, 20]
trainCount = 1
knownGestures = []
tol = 10
gestName = []
for i in range(trainCount):
    name = input()
    gestName.append(name)
print(gestName)

while True:
    ignore, frame = cam.read()
    frame = cv2.flip(frame, 1)

    myhand = parseHandLandmarks(frame)
    if len(myhand) != 0:
        if trainCount != 0:

        print("show your gesture "+str(trainCount)+" press t when ready")
        if cv2.waitKey(1) & 0xff == ord('t'):
            knownGesture = findDistances(myhand[0][0])
            knownGestures.append(knownGesture)
            trainCount -= 1
    if trainCount == 0:
        if len(myhand) != 0:
            unknownGesture = findDistances(myhand[0][0])
            myGesture = findGesture(unknownGesture, knownGestures, keyPoints,gestName,tol)
            print(myGesture)

    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
