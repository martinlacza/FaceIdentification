import sklearn
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

landmarkLines = []
with open("outputformatLandmarks.txt", "r") as fp:
    for lines in fp:
        landmarkLines.append(lines.strip())

landmarks = []
for i in range(len(landmarkLines)):
    landmarks.append(landmarkLines[i].split(","))

predictLines = []
with open("out.txt", "r") as f:
    for lines in f:
        predictLines.append(lines.strip())

predictions = []
for i in range(len(predictLines)):
    predictions.append(predictLines[i].split(","))

print(predictions[0][0])
print(landmarks[0][2])

error=[]

for i in range(len(landmarkLines)):
    if landmarks[i][0] == predictions[i][0]:
        MSE = []
        lefteyeannot = [int(landmarks[i][1]),int(landmarks[i][2])]
        lefteyepred = [int(predictions[i][1]),int(predictions[i][2])]
        righteyeannot = [int(landmarks[i][3]),int(landmarks[i][4])]
        righteyepred = [int(predictions[i][3]),int(predictions[i][4])]
        noseannot = [int(landmarks[i][5]), int(landmarks[i][6])]
        nosepred = [int(predictions[i][5]), int(predictions[i][6])]
        leftmouthannot = [int(landmarks[i][7]), int(landmarks[i][8])]
        leftmouthpred = [int(predictions[i][7]), int(predictions[i][8])]
        rightmouthannot = [int(landmarks[i][9]), int(landmarks[i][10])]
        rightmouthpred = [int(predictions[i][9]), int(predictions[i][10])]
        MSE.append(landmarks[i][0])
        MSE.append(mean_squared_error(lefteyeannot,lefteyepred,squared=False))
        MSE.append(mean_squared_error(righteyeannot, righteyepred, squared=False))
        MSE.append(mean_squared_error(noseannot, nosepred, squared=False))
        MSE.append(mean_squared_error(righteyeannot, righteyepred, squared=False))
        MSE.append(mean_squared_error(leftmouthannot, leftmouthpred, squared=False))
        MSE.append(mean_squared_error(rightmouthannot, rightmouthpred, squared=False))
        error.append(MSE)

graph = []
y = []
for i in range(len(error)):
    s = error[i][0].replace(".jpg","")
    graph.append(int(s))
    y.append(error[i][3])

plt.plot(graph,y)
plt.show()


with open("mseout.txt","w") as o:
    for i in range(len(error)):
        print(error[i],file=o)