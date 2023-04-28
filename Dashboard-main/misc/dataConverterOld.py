import json
import numpy as np
import glob
import os
from PIL import Image
from misc import keypointMappings

body25Mappings={
	0:	"Nose",
	1:	"Neck",
	2:	"RShoulder",
	3:	"RElbow",
	4:	"RWrist",
	5:	"LShoulder",
	6:	"LElbow",
	7:	"LWrist",
	8:	"MidHip",
	9:	"RHip",
	10:	"RKnee",
	11:	"RAnkle",
	12:	"LHip",
	13:	"LKnee",
	14:	"LAnkle",
	15:	"REye",
	16:	"LEye",
	17:	"REar",
	18:	"LEar",
	19:	"LBigToe",
	20:	"LSmallToe",
	21:	"LHeel",
	22:	"RBigToe",
	23:	"RSmallToe",
	24:	"RHeel"
}

faceMappings={
    0: 'RChic_6',
    1:'RChic_5',
    2:'RChic_4',
    3:'RChic_3',
    4:'RChic_2',
    5:'RChic_1',
    6:'RChic_0',
    7:'RMento',
    8:'Mento',
    9: 'LMento',
    10: 'LChic_0',
    11: 'LChic_1',
    12: 'LChic_2',
    13: 'LChic_3',
    14: 'LChic_45',
    15: 'LChic_5',
    16: 'LChic_6',
    17: 'REyelashes_4',
    18: 'REyelashes_3',
    19: 'REyelashes_2',
    20: 'REyelashes_1',
    21: 'REyelashes_0',
    22: 'LEyelashes_0',
    23: 'LEyelashes_1',
    24: 'LEyelashes_2',
    25: 'LEyelashes_3',
    26: 'LEyelashes_4',
    27: 'Nose_0',
    28: 'UNose_1',
    29: 'UNose_2',
    30: 'UNose_3',
    31: 'BNose_0',
    32: 'BNose_1',
    33: 'BNose_2',
    34: 'BNose_3',
    35: 'BNose_4',
    36: 'REye_R',
    37: 'REye_U_1',
    38: 'REye_U_0',
    39: 'REye_L',
    40: 'REye_B_0',
    41: 'REye_B_1',
    42: 'LEye_R',
    43: 'LEye_U_1',
    44: 'LEye_U_0',
    45: 'LEye_L',
    46: 'LEye_B_0',
    47: 'LEye_B_1',
    48: 'OMouth_R',
    49: 'OMouth_U_0',
    50: 'OMouth_U_1',
    51: 'OMouth_U_2',
    52: 'OMouth_U_3',
    53: 'OMouth_U_4',
    54: 'OMouth_L',
    55: 'OMouth_B_4',
    56: 'OMouth_B_3',
    57: 'OMouth_B_2',
    58: 'OMouth_B_1',
    59: 'OMouth_B_0',
    60: 'IMouth_R',
    61: 'IMouth_U_0',
    62: 'IMouth_U_1',
    63: 'IMouth_U_3',
    64: 'IMouth_L',
    65: 'IMouth_B_2',
    66: 'IMouth_B_1',
    67: 'IMouth_B_0',
    68: 'REye',
    69: 'LEye'
}

hand_mappings={
    0: 'Palm',
    1: 'Thumb_0',
    2: 'Thumb_1',
    3: 'Thumb_2',
    4: 'Thumb_3',
    5: 'Index_0',
    6: 'Index_1',
    7: 'Index_2',
    8: 'Index_3',
    9: 'Midle_0',
    10: 'Middle_1',
    11: 'Middle_2',
    12: 'Middle_3',
    13: 'Ring_0',
    14: 'Ring_1',
    15: 'Ring_2',
    16: 'Ring_3',
    17: 'Little_0',
    18: 'Little_1',
    19: 'Little_2',
    20: 'Little_3'
}

def ConvertData(inputFile,outputFolder,videoWidth=1,videoHeight=1):
    #load json
    f=open(inputFile,"r").read()
    data=json.loads(f)

    allData_body=[]
    for i in range(25):
        allData_body.append([])
        allData_body.append([])
    allData_face=[]
    for i in range(70):
        allData_face.append([])
        allData_face.append([])
    allData_hand_left=[]
    for i in range(21):
        allData_hand_left.append([])
        allData_hand_left.append([])
    allData_hand_right=[]
    for i in range(21):
        allData_hand_right.append([])
        allData_hand_right.append([])
    allData_frame_time=[]

    for frameId in range(len(data["data"])):
        pose_keypoints_2d=data["data"][frameId]["raw"]["pose_keypoints_2d"]
        face_keypoints_2d=data["data"][frameId]["raw"]["face_keypoints_2d"]
        hand_left_keypoints_2d=data["data"][frameId]["raw"]["hand_left_keypoints_2d"]
        hand_right_pose_keypoints_2d=data["data"][frameId]["raw"]["hand_right_keypoints_2d"]

        allData_frame_time.append(data["data"][frameId]["raw"]["time"])
        for i in range(25):
            allData_body[i*2].append(pose_keypoints_2d[i][0])
            allData_body[i*2+1].append(pose_keypoints_2d[i][1])
        for i in range(70):
            allData_face[i*2].append(face_keypoints_2d[i][0])
            allData_face[i*2+1].append(face_keypoints_2d[i][1])
        for i in range(21):
            allData_hand_left[i*2].append(hand_left_keypoints_2d[i][0])
            allData_hand_left[i*2+1].append(hand_left_keypoints_2d[i][1])
        for i in range(21):
            allData_hand_right[i*2].append(hand_right_pose_keypoints_2d[i][0])
            allData_hand_right[i*2+1].append(hand_right_pose_keypoints_2d[i][1])

    dict_body={}
    dict_face={}
    dict_hand_left={}
    dict_hand_right={}
    #combine x,y
    for i in range(25):
        partX=np.array(allData_body[i*2])/videoWidth
        partY=np.array(allData_body[i*2+1])/videoWidth
        partArray=np.stack([partX,partY],axis=0)
        dict_body[body25Mappings[i]]=partArray

    for i in range(70):
        partX=np.array(allData_face[i*2])/videoWidth
        partY=np.array(allData_face[i*2+1])/videoWidth
        partArray=np.stack([partX,partY],axis=0)
        dict_face[faceMappings[i]]=partArray

    for i in range(21):
        partX=np.array(allData_hand_left[i*2])/videoWidth
        partY=np.array(allData_hand_left[i*2+1])/videoWidth
        partArray=np.stack([partX,partY],axis=0)
        dict_hand_left[hand_mappings[i]]=partArray

    for i in range(21):
        partX=np.array(allData_hand_right[i*2])/videoWidth
        partY=np.array(allData_hand_right[i*2+1])/videoWidth
        partArray=np.stack([partX,partY],axis=0)
        dict_hand_right[hand_mappings[i]]=partArray

    outputDict={}
    outputDict["body"]=dict_body
    outputDict["face"]=dict_face
    outputDict["hand_left"]=dict_hand_left
    outputDict["hand_right"]=dict_hand_right
    outputDict["frame_time"]=allData_frame_time
    return outputDict

def getDeltaFromPositions(inputArray):
    outputArray=inputArray+0

    arrayLength=outputArray.shape[1]

    for i in range(arrayLength-1):
        outputArray[:,arrayLength-1-i]=outputArray[:,arrayLength-1-i]-outputArray[:,arrayLength-2-i]

    outputArray[:,0]=0
    return outputArray