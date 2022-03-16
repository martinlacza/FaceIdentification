import os

folder="C:/Users/Uzivatel/Downloads/CelebA-subset-7200-7500/CelebA-small"
list = []
for filename in os.listdir(folder):
    list.append(filename)

print(list[0]+".txt" == list[1])
for i in range(len(list)-1):
    if ".txt" not in list[i]:
        string = list[i] + ".txt"
        if string != list[i+1]:
            print(list[i])