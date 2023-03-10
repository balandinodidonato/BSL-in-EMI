import json
from matplotlib import pyplot as plt
import sys
from plottingFunctions import *
import numpy as np

plots = int(sys.argv[1])
songsDeltas = []
songsDeltasAvg = []
songsJointsDelta = []
songsJointsNames = []
songsFrames = []
noFrames = []
shoulderX = []
rawWristShoulders = []
index = 0
dataFrames = []
songRaw = []

if plots < 8:
    loadJSONFiles()

    for index in range(6):
        songsJointsNames.append(jointNames)

    for songsData in songsFeatures:
        songsDeltas.append(songsData['deltaTotal'])
        songsDeltasAvg.append(songsData['deltaAvg'])
        songsJointsDelta.append(songsData['deltaTotalJoints'])
        dataFrames.append(songsData['data'])
        noFrames.append(songsData['totalFrames'])

    #for rawDataSong in dataFrames:
    #    rawFramesDataSong = []
    #    for rawFramesData in rawDataSong['data']:
    #        rawFramesDataSong.append(rawFramesData['raw_wrists_shoulders'])
    #    songRaw.append(rawFramesDataSong)

#    print(songRaw[0][0])

  #  print(rawWristShoulders[0])


# prints delta total of songs
if plots == 0:
    for index in range(6):
        plt.ylim(0, 70000000)
        plt.yticks([0, 10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000])
        plt.bar(SPstringRed[index], songsDeltas[index], color=colors[index])
        plt.grid(visible=True, axis='y', alpha=0.5)
        plt.title('Total delta') 
        plt.ylabel('Keypoint Delta / Frame')
        plt.xlabel('Interpretation')
    plt.savefig('./plot/deltaTotalParticipant.png')
    plt.show()

# prints 
if plots == 1:
    figure, axis = plt.subplots(6, 1, figsize=(7,10))
    
    for data in songsJointsDelta:
        axis[index].bar(jointID, data, color=rgb01)
        axis[index].set_title(SPstring[index]) 
        axis[index].set_ylim(0, 8000000)
        axis[index].set_yticks([0, 2000000, 4000000, 6000000, 8000000])

        axis[index].set_ylabel('Kpnt Delta / Frame')
        axis[index].set_xlabel('Keypoints')
        index += 1
        index %= 6    

    plt.title('Interpreations delta') 
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=1)
    plt.savefig('./plot/deltaTotalJoints.png')
    plt.show()

    
if plots == 2:
    x = jointID
    y = np.array(songsJointsDelta)

    plt.bar(x, y[0], color=colors[0])
    plt.bar(x, y[1], bottom=y[0], color=colors[1])
    plt.bar(x, y[2], bottom=y[0]+y[1], color=colors[2])
    plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], color=colors[3])
    plt.bar(x, y[4], bottom=y[0]+y[1]+y[2]+y[3], color=colors[4])
    plt.bar(x, y[5], bottom=y[0]+y[1]+y[2]+y[3]+y[4], color=colors[5])

    plt.ylim(0, 35000000)
    plt.ylabel('Keypoint Delta / Frame')
    plt.xlabel('Keypoint No.')
    plt.legend(SPstringRed)
    plt.savefig('./plot/deltaTotalJointsStack_All.png')

if plots == 4:

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

if plots == 5:
    plt.rc('font', size=12)

    figure, axis = plt.subplots(2, 1, figsize=(9,9))
    y = []
    kToOmit = [24, 23, 22, 21, 20, 19, 14, 13]

    for idx in range(6):
        for test in kToOmit:
            songsJointsDelta[idx].pop(test)
           # songsJointsDelta[idx].pop(11)
    
        y.append(np.array(songsJointsDelta[idx])/np.array(noFrames[idx]))



    for test2 in kToOmit:
        jointID.pop(test2)

   # jointID.pop(11)
    
    axis[0].bar(jointID, y[0], label='P1', color='r')
    axis[0].bar(jointID, y[1], label='P2', bottom=y[0], color='g')
    axis[0].bar(jointID, y[2], label='P3', bottom=y[0]+y[1], color='b')

    axis[1].bar(jointID, y[3], label='P1', color='r')
    axis[1].bar(jointID, y[4], label='P2', bottom=y[3], color='g')
    axis[1].bar(jointID, y[5], label='P3', bottom=y[3]+y[4], color='b')
    
    for index in range(0, 2):
        
       # axis[index].set_label(songsTitle)
        #axis[index].legend()
        plt.rc('font', size=12)
        axis[index].set_title(songsTitle[index]) 
       # axis[index].set_ylim(0, 2500)
     #   axis[index].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
        plt.rc('font', size=9)
        axis[index].set_ylabel('Tot. QoM (pixesls) / Song Frames No.')
        axis[index].set_xlabel('Keypoints')
        axis[index].grid(visible=True, axis='y', alpha=0.5)

    #plt.title('Particiapnts\' Kpnt Delta vs Songs')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95, wspace=0.2, hspace=0.4) 
    plt.savefig('./plot/deltaTotalJointsStack_Songs.png')
    plt.show()

if plots == 6:
    for index in range(6):
        plt.ylim(0, 9000)
        #plt.yticks([0, 1000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000])
        plt.bar(SPstringRed[index], songsDeltasAvg[index], color=colors[index])
        plt.grid(visible=True, axis='y', alpha=0.5)
        #plt.title('AVG delta') 
        plt.ylabel('Body keypoint delta (Pixels)')
        plt.xlabel('Interpretation')
    plt.savefig('./plot/deltaAVGParticipant.png')
    plt.show()


# average of
if plots == 7:
    figure, axis = plt.subplots(6, 1, figsize=(7,10))
    
    for index in range(6):

        data = np.array(songsJointsDelta[index])/np.array(noFrames[index])


        axis[index].bar(jointID, data, color=rgb01)
        axis[index].set_title(SPstring[index]) 
        axis[index].set_ylim(0, 1000)
  #      axis[index].set_yticks([0, 2000000, 4000000, 6000000, 8000000])

        axis[index].set_ylabel('QoM AVG (pxl)')
        axis[index].set_xlabel('Keypoints')
        index += 1
        index %= 6    

    #plt.title('Interpreations delta') 
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=1)
    plt.savefig('./plot/deltaAVGJoints.png')
    plt.show()
