import json
import numpy as np

songsFeatures = []
participants = ['P1', 'P2', 'P3']
songsTitle =['S1', 'S2']
SPstring = [
            'Goodbye by Apparat, P1', 
            'Goodbye by Apparat,  P2', 
            'Goodbye by Apparat,  P3', 
            'Crescendools by Daft Punk, P1', 
            'Crescendools by Daft Punk, P2', 
            'Crescendools by Daft Punk, P3'
            ]

SPstringRed = [
            'S1 P1', 
            'S1 P2', 
            'S1 P3', 
            'S2 P1', 
            'S2 P2', 
            'S2 P3'
            ]

colors = ['r', 'g', 'b', 'orangered', 'limegreen', 'deepskyblue']

songsTitleFull = ['Goodbye by Apparat', 'Crescendools by DaftPunk']

songsJ = ['Apparat_Goodbye', 'DaftPunk_Crescendools']
keypoints_IDs = [['0',  "Nose"], ['1',  "Neck"], ['2',  "RShoulder"], ['3',  "RElbow"], ['4',  "RWrist"], ['5',  "LShoulder"], ['6',  "LElbow"], ['7',  "LWrist"], ['8',  "MidHip"], ['9',  "RHip"],['10', "RKnee"], ['11', "RAnkle"], ['12', "LHip"], ['13', "LKnee"], ['14', "LAnkle"], ['15', "REye"], ['16', "LEye"], ['17', "REar"], ['18', "LEar"], ['19', "LBigToe"], ['20', "LSmallToe"], ['21', "LHeel"], ['22', "RBigToe"], ['23', "RSmallToe"], ['24', "RHeel"]]
jointNames = []
jointID = []

for k_string in keypoints_IDs:
    jointID.append(k_string[0])
    jointNames.append(k_string[1])

def loadJSONFiles():
    for indextSong in songsJ:
        for indexPart in participants:
            with open('data/'+indextSong+'_'+indexPart+'_features.json', 'r') as f:
                songsFeatures.append(json.load(f))
    
    print('Message: JSON files loaded')
    
rgb255 = [[245, 66, 132],[255, 0, 0],[247, 95, 0],[247, 193, 0],[247, 247, 0],[181, 247, 0],[103, 247, 0],[0, 255, 0],[247, 45, 0],[178, 102, 255],[51, 255, 51],[255, 255, 255],[102, 178, 255],[51, 153, 255],[51, 51, 255],[255, 0, 127],[178, 102, 255],[255, 0, 255],[102, 0, 204],[0, 0, 255],[0, 0, 255],[51, 51, 255],[0, 255, 255],[0, 255, 255],[0, 255, 255],[255, 255, 255]]

rgb01 = np.array(rgb255)/255
