import cv2
import face_recognition as fr

vanFace = fr.load_image_file("known/vansh gupta.jpg")
faceloc = fr.face_locations(vanFace)[0]
vanFaceEncode = fr.face_encodings(vanFace)[0]

knownEncodings = [vanFaceEncode]
names = ["Vansh Gupta"]

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cam.set(cv2.CAP_PROP_FPS, 30)

while True:
    ignore, unknownFace = cam.read()
    unknownFaceRGB = cv2.cvtColor(unknownFace, cv2.COLOR_BGR2RGB)
    faceLocations = fr.face_locations(unknownFaceRGB)
    unknownEncodings = fr.face_encodings(unknownFaceRGB, faceLocations)
    for faceLocation, unknownEncoding in zip(faceLocations, unknownEncodings):
        top, right, bottom, left = faceLocation
        cv2.rectangle(unknownFace, (left, top), (right, bottom), (255, 0, 0), 3)
        name = "not found"
        matches = fr.compare_faces(knownEncodings, unknownEncoding)
        if True in matches:
            matchIndex = matches.index(True)
            name = names[matchIndex]
        cv2.putText(unknownFace, name, (left, top), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 3)

    cv2.imshow("my webcam", unknownFace)
    cv2.moveWindow("my webcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()












