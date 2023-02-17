import json
from matplotlib import pyplot as plt
import sys
from plottingFunctions import *
import numpy as np

plots = str(sys.argv[1])
#part = int(sys.argv[2])


loadJSONFiles()
songsDeltas = []
songsJointsDelta = []
songsJointsNames = []
index = 0

for index in range(6):
    songsJointsNames.append(jointNames)

for songsData in songsFeatures:
    songsDeltas.append(songsData['deltaTotal'])
    songsJointsDelta.append(songsData['deltaTotalJoints'])

#print(songsDeltas)
if plots == '0':
    for index in range(6):
        plt.bar(SPstringRed[index], songsDeltas[index], color='b')
        plt.ylim(0, 70000000)
        plt.yticks([0, 2000000, 4000000, 6000000, 7000000])
        plt.title('Total delta') 
        plt.ylabel('Keypoint Delta / Frame')
        plt.xlabel('Interpretation')
    plt.savefig('./plot/deltaTotalParticipant.png')

if plots == '1':
    figure, axis = plt.subplots(6, 1, figsize=(7,10))
    
    for data in songsJointsDelta:
        axis[index].bar(jointID, data)
        axis[index].set_title(SPstring[index]) 
        axis[index].set_ylim(0, 8000000)
        axis[index].set_yticks([0, 2000000, 4000000, 6000000, 8000000])
        axis[index].set_ylabel('Kpnt Delta / Frame')
        axis[index].set_xlabel('Keypoints')
        index += 1
        index %= 6    
   
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=1)
    plt.savefig('./plot/deltaTotalJoints.png')

    
if plots == '2':
    x = jointID
    y = np.array(songsJointsDelta)

    plt.bar(x, y[0], color='r')
    plt.bar(x, y[1], bottom=y[0], color='g')
    plt.bar(x, y[2], bottom=y[0]+y[1], color='b')
    plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], color='orangered')
    plt.bar(x, y[4], bottom=y[0]+y[1]+y[2]+y[3], color='limegreen')
    plt.bar(x, y[5], bottom=y[0]+y[1]+y[2]+y[3]+y[4], color='deepskyblue')

    plt.ylim(0, 35000000)
    plt.ylabel('Keypoint Delta / Frame')
    plt.xlabel('Keypoint No.')
    plt.legend(SPstringRed)
    plt.savefig('./plot/deltaTotalJointsStack_All.png')

if plots == '3':
    plt.bar(jointID, songsJointsDelta[part-1], label=SPstringRed[part-1], color='r')
    plt.bar(jointID, songsJointsDelta[part+2], label=SPstringRed[part+2], bottom=songsJointsDelta[part-1], color='b')
    plt.ylabel('Keypoint Delta / Frame')
    plt.xlabel('Keypoint No.')
    plt.ylim(0, 15000000)
    plt.grid(visible=True, axis='y', alpha=0.5)

    plt.legend()
    plt.savefig('./plot/deltaTotalJointsStack_S12_P'+str(part)+'.png')


if plots == '4':

    figure, axis = plt.subplots(3, 1, figsize=(7,9))

    for index in range(0, 3):
        axis[index].bar(jointID, songsJointsDelta[index], label=songsTitle[0], color='r')
        axis[index].bar(jointID, songsJointsDelta[index+3], label=songsTitle[1], bottom=songsJointsDelta[index], color='b')
       # axis[index].set_label(songsTitle)
        axis[index].legend()
        axis[index].set_title('Participant '+str(index+1)) 
        axis[index].set_ylim(0, 13000000)
        axis[index].set_yticks([0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000])
        axis[index].set_ylabel('Kpnt Delta / Frame')
        axis[index].set_xlabel('Keypoints')
        axis[index].grid(visible=True, axis='y', alpha=0.5)


    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.5)
    plt.savefig('./plot/deltaTotalJointsStack_Participants.png')


if plots == '5':
    figure, axis = plt.subplots(2, 1, figsize=(7,9))
    y = np.array(songsJointsDelta)

    axis[0].bar(jointID, y[0], label='P1', color='r')
    axis[0].bar(jointID, y[1], label='P2', bottom=y[0], color='g')
    axis[0].bar(jointID, y[2], label='P3', bottom=y[0]+y[1], color='b')

    axis[1].bar(jointID, y[3], label='P1', color='r')
    axis[1].bar(jointID, y[4], label='P2', bottom=y[3], color='g')
    axis[1].bar(jointID, y[5], label='P3', bottom=y[3]+y[4], color='b')
    
    for index in range(2):
       # axis[index].set_label(songsTitle)
        axis[index].legend()
        axis[index].set_title(songsTitle[index]) 
        axis[index].set_ylim(0, 18000000)
        axis[index].set_yticks([0, 2000000, 4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000])
        axis[index].set_ylabel('Kpnt Delta / Frame')
        axis[index].set_xlabel('Keypoints')
        axis[index].grid(visible=True, axis='y', alpha=0.5)

    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.3) 
    plt.savefig('./plot/deltaTotalJointsStack_Songs.png')