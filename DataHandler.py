def remove_items(test_list, item):
    # remove the item for all its occurrences
    for i in test_list:
        if (i == item):
            test_list.remove(i)

    return test_list

alllines = []
with open("out.txt", "r") as o:
    for lines in o:
        alllines.append(lines.strip())

line = []
for i in range(len(alllines)):
    line.append(alllines[i].split(","))
#line.append(alllines[0].split(","))
landmarkLines = []
with open("list_landmarks_celeba.txt", "r") as o:
    for lines in o:
        landmarkLines.append(lines.strip())

linesLandmark = []
for i in range(len(landmarkLines)):
    linesLandmark.append(landmarkLines[i].split(" "))

print(linesLandmark[113])
for i in range(len(linesLandmark)):
        linesLandmark[i] = remove_items(linesLandmark[i],'')
print(linesLandmark[0])
print(line[0][0])
print(linesLandmark[113][0])
print(linesLandmark[113][0] == line[0][0])
output = []
for i in range(len(linesLandmark)):
    for j in range(len(line)):
        if linesLandmark[i][0] == line[j][0]:
            output.append(linesLandmark[i])

for i in range(len(output)):
    print(output[i])
print(len(output))
with open("outputformatLandmarks.txt","w") as op:
    for i in range(len(output)):
        print(output[i],file=op)


print(line[1])