import json

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

songs = ['Apparat_Goodbye', 'DaftPunk_Crescendools']
keypoints_IDs = [['0',  "Nose"], ['1',  "Neck"], ['2',  "RShoulder"], ['3',  "RElbow"], ['4',  "RWrist"], ['5',  "LShoulder"], ['6',  "LElbow"], ['7',  "LWrist"], ['8',  "MidHip"], ['9',  "RHip"],['10', "RKnee"], ['11', "RAnkle"], ['12', "LHip"], ['13', "LKnee"], ['14', "LAnkle"], ['15', "REye"], ['16', "LEye"], ['17', "REar"], ['18', "LEar"], ['19', "LBigToe"], ['20', "LSmallToe"], ['21', "LHeel"], ['22', "RBigToe"], ['23', "RSmallToe"], ['24', "RHeel"]]
jointNames = []
jointID = []

for k_string in keypoints_IDs:
    jointID.append(k_string[0])
    jointNames.append(k_string[1])

def loadJSONFiles():
    for indextSong in songs:
        for indexPart in participants:
            with open('data/'+indextSong+'_'+indexPart+'_features.json', 'r') as f:
                songsFeatures.append(json.load(f))
    
    print('Message: JSON files loaded')
    