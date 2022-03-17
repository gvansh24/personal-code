import cv2
import mediapipe as mp

width = 640
height = 360
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

faceMesh = mp.solutions.face_mesh.FaceMesh()
mpDraw = mp.solutions.drawing_utils
drawSpecLine = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 0, 255))
drawSpecCircle = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0))

while True:
    ignore, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)
    if results.multi_face_landmarks is not None:
        for faceLandMarks in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(frame, faceLandMarks, mp.solutions.face_mesh.FACEMESH_TESSELATION, drawSpecLine,
            #                       drawSpecCircle)
            indx = 0
            for lm in faceLandMarks.landmark:
                cv2.putText(frame, str(indx), (int(lm.x * width), int(lm.y * height)), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 0, 0),)
                indx += 1
    cv2.imshow("my webcam", frame)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
