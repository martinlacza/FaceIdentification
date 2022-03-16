import sys
import dlib
import cv2
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
folder="C:/Users/Uzivatel/Downloads/newStuff/CelebA-small"
#cam = cv2.VideoCapture(0)
color_green = (0,255,0)
line_width = 3
foundface = []
notFoundFaceFileName = []
for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder,filename))
    rgb_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    dets = detector(rgb_image)
    if len(dets) == 0:
        print(filename)
        notFoundFaceFileName.append(filename)
    if len(dets) == 1:
        for face in dets:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            #cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, line_width)
            landmarks = predictor(rgb_image, face)
            keypoints = []
            keypoints.append(filename)
            keypoints.append(landmarks.part(40).x)
            keypoints.append(landmarks.part(40).y)
            keypoints.append(landmarks.part(46).x)
            keypoints.append(landmarks.part(46).y)
            keypoints.append(landmarks.part(30).x)
            keypoints.append(landmarks.part(30).y)
            keypoints.append(landmarks.part(60).x)
            keypoints.append(landmarks.part(60).y)
            keypoints.append(landmarks.part(54).x)
            keypoints.append(landmarks.part(54).y)
            foundface.append(keypoints)
            #print(foundface)
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(img, (x, y), 4, (255, 255, 255), -1)

        cv2.imshow('blabla',img)
        cv2.destroyAllWindows()



with open("out.txt","w") as o:
    for i in range(len(foundface)):
        print(foundface[i], file=o)

with open("out2.txt", "w") as o:
    for i in range(len(notFoundFaceFileName)):
        print(notFoundFaceFileName[i], file=o)


