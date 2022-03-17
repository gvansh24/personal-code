import cv2
import face_recognition as fr

donFace = fr.load_image_file("known/Donald Trump.jpg")
faceloc = fr.face_locations(donFace)[0]
donFaceEncode = fr.face_encodings(donFace)[0]

knownEncodings = [donFaceEncode]
names = ["Donald Trump"]

unknownFace = fr.load_image_file("unknown/u1.jpg")
unknownFaceBGR = cv2.cvtColor(unknownFace,cv2.COLOR_RGB2BGR)
faceLocations = fr.face_locations(unknownFace)
unknownEncodings = fr.face_encodings(unknownFace,faceLocations)

for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
    top,right,bottom,left = faceLocation
    cv2.rectangle(unknownFaceBGR,(left,top),(right,bottom),(255,0,0),3)
    name = "not found"
    matches = fr.compare_faces(knownEncodings,unknownEncoding)
    if True in matches:
        matchIndex = matches.index(True)
        name = names[matchIndex]
    cv2.putText(unknownFaceBGR,name,(left,top),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),3)
cv2.imshow("my faces",unknownFaceBGR)

cv2.waitKey(5000)
