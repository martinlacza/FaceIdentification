import cv2
import os

folder = "C:/Users/Uzivatel/Downloads/newStuff/CelebA-small"
path = "C:/Users/Uzivatel/Documents/NotFound"

nameoffiles = []
with open("out2.txt","r") as fp:
    for lines in fp:
        nameoffiles.append(lines.strip())
#for i in range(len(nameoffiles)):
    #print(type(nameoffiles[i]))

f = folder+"/"+nameoffiles[0]

print(len("C:/Users/Uzivatel/Downloads/newStuff/CelebA-small/000093.jpg"))
print("C:/Users/Uzivatel/Downloads/newStuff/CelebA-small/000093.jpg" == f)
file = cv2.imread("C:/Users/Uzivatel/Downloads/newStuff/CelebA-small/000114.jpg")




for i in range(len(nameoffiles)):
    path = "C:/Users/Uzivatel/Documents/NotFound"
    nameOfImage= folder + "/" + nameoffiles[i]
    print(nameOfImage)
    theImage = cv2.imread(nameOfImage)
    cv2.imshow("file", theImage)
    cv2.waitKey(1000)
    path = path +"/"+ str(i) + ".jpg"
    cv2.imwrite(path, theImage)
