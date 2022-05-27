# This script merges all json file from two folders, one with face+body data and with body+hand dta into a JSON file 

# Dependecies
import glob, json
from sre_constants import SUCCESS
import sys
from datetime import timedelta
from tokenize import group
import os

keypoints_IDs = [[0,  "Nose"], [1,  "Neck"], [2,  "RShoulder"], [3,  "RElbow"], [4,  "RWrist"], [5,  "LShoulder"], [6,  "LElbow"], [7,  "LWrist"], [8,  "MidHip"], [9,  "RHip"],[10, "RKnee"], [11, "RAnkle"], [12, "LHip"], [13, "LKnee"], [14, "LAnkle"], [15, "REye"], [16, "LEye"], [17, "REar"], [18, "LEar"], [19, "LBigToe"], [20, "LSmallToe"], [21, "LHeel"], [22, "RBigToe"], [23, "RSmallToe"], [24, "RHeel"], [25, "Background"]]

face_IDs = [
    [0, "RChic_6"], [1, "RChic_5"], [2, "RChic_4"], [3, "RChic_3"], [4, "RChic_2"], [5, "RChic_1"], [6, "RChic_0"], [7, "RMento"], [8, "Mento"], [9, "LMento"], [10, "LChic_0"], [11, "LChic_1"], [12, "LChic_2"], [13, "LChic_3"], [14, "LChic_45"], [15, "LChic_5"], [16, "LChic_6"], 
    [17, "REyelashes_4"], [18, "REyelashes_3"], [19, "REyelashes_2"], [20, "REyelashes_1"], [21, "REyelashes_0"], 
    [22, "LEyelashes_0"], [23, "LEyelashes_1"], [24, "LEyelashes_2"], [25, "LEyelashes_3"], [26, "LEyelashes_4"], 
    [27, "Nose_0"], [28, "UNose_1"], [29, "UNose_2"], [30, "UNose_3"], 
    [31, "BNose_0"], [32, "BNose_1"], [33, "BNose_2"], [34, "BNose_3"], [35, "BNose_4"], 
    [36, "REye_R"], [37, "REye_U_1"], [38, "REye_U_0"], [39, "REye_L"], [40, "REye_B_0"], [41, "REye_B_1"], 
    [42, "LEye_R"], [43, "LEye_U_1"], [44, "LEye_U_0"], [45, "LEye_L"], [46, "LEye_B_0"], [47, "LEye_B_1"],
    [48, "OMouth_R"], [49, "OMouth_U_0"], [50, "OMouth_U_1"], [51, "OMouth_U_2"], [52, "OMouth_U_3"], [53, "OMouth_U_4"], [54, "OMouth_L"], [55, "OMouth_B_4"], [56, "OMouth_B_3"], [57, "OMouth_B_2"], [58, "OMouth_B_1"], [59, "OMouth_B_0"],
    [60, "IMouth_R"], [61, "IMouth_U_0"], [62, "IMouth_U_1"], [63, "IMouth_U_3"], [64, "IMouth_L"], [65, "IMouth_B_2"], [66, "IMouth_B_1"], [67, "IMouth_B_0"], [68, "REye"], [69, "LEye"]]
hand_IDs = [
    [0, "Palm"], 
    [1, "Thumb_0"], [2, "Thumb_1"], [3, "Thumb_2"], [4, "Thumb_3"],
    [5, "Index_0"], [6, "Index_1"], [7, "Index_2"], [8, "Index_3"],
    [9, "Midle_0"], [10, "Middle_1"], [11, "Middle_2"], [12, "Middle_3"],
    [13, "Ring_0"], [14, "Ring_1"], [15, "Ring_2"], [16, "Ring_3"],
    [17, "Little_0"], [18, "Little_1"], [19, "Little_2"], [20, "Little_3"]]


# Preparation of empty arrays 
empty_pose_keypoints_2d =[]
for index in range(75):
    empty_pose_keypoints_2d.append(0)

empty_face_keypoints_2d =[]
for index in range(210):
    empty_face_keypoints_2d.append(0)

empty_hand_keypoints_2d =[]
for index in range(63):
    empty_hand_keypoints_2d.append(0)

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
face_file_path = sys.argv[3] # Path to face data set
hand_file_path = sys.argv[4] # Path to face data set
FPS = float(sys.argv[5]) # framerate

# Lists and variables
pose_keypoints_2d = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []
data_list = []
face_data = []
hand_data = []
count_face_files = 0
count_hand_files = 1

no_of_files = (len([name for name in os.listdir(face_file_path) if os.path.isfile(os.path.join(face_file_path, name))]))


# Rename for data ordering
def reorder(path):
    for i in range(0, 13, 1):
        for f in glob.glob(path+"/*.json"):
            new_filename = f.replace("_0","_")
            os.rename(f,new_filename)

    for f in glob.glob(path+"/*.json"):
        new_filename = f.replace("__","_0_")
        os.rename(f,new_filename)

reorder(face_file_path)
reorder(hand_file_path)

# Extract and append data
for index in range(0, no_of_files-1):
    currentFacePath = str(face_file_path+"/"+song+"_"+participant+"_"+str(index)+"_keypoints.json")
    with open(currentFacePath, 'r') as f:
        data = json.load(f)
        face_data.append(data)

    currentHandPath = str(hand_file_path+"/"+song+"_"+participant+"_"+str(index)+"_keypoints.json")
    with open(currentHandPath, 'r') as f:
        data = json.load(f)
        hand_data.append(data)

face_data_tot = len(face_data)
hand_data_tot = len(hand_data)
   

# iterates through the JSON with the face data and extracts the face keypoints

for object in face_data:
    if len(object["people"]):
        for people in object["people"]:
            if len(people["face_keypoints_2d"]):
                face_keypoints_2d.append(people["face_keypoints_2d"])
            else:
                face_keypoints_2d.append(empty_face_keypoints_2d)
    else:
        face_keypoints_2d.append(empty_face_keypoints_2d)

# iterates through the JSON with the hand data and extracts the hand keypoints
for object in hand_data:
    if len(object["people"]):
        for people in object["people"]:
            if len(people["pose_keypoints_2d"]):
                pose_keypoints_2d.append(people["pose_keypoints_2d"])
            else:
                pose_keypoints_2d.append(empty_pose_keypoints_2d)
            
            if len(people["hand_left_keypoints_2d"]):
                hand_left_keypoints_2d.append(people["hand_left_keypoints_2d"])
            else:
                hand_left_keypoints_2d.append(empty_hand_keypoints_2d)
            if people["hand_right_keypoints_2d"]:
                hand_right_keypoints_2d.append(people["hand_right_keypoints_2d"])
            else:
                hand_right_keypoints_2d.append(empty_hand_keypoints_2d)
            
    else:
        pose_keypoints_2d.append(empty_pose_keypoints_2d)
        hand_left_keypoints_2d.append(empty_hand_keypoints_2d)
        hand_right_keypoints_2d.append(empty_hand_keypoints_2d)


if(len(pose_keypoints_2d)==len(hand_left_keypoints_2d)==len(hand_right_keypoints_2d)==len(face_keypoints_2d)==face_data_tot==hand_data_tot):
    def group(theList, N):
        return [theList[n:n+N] for n in range(0, len(theList), N)]
    
    pose_keypoints_2d_split = []
    for keypoint_body in pose_keypoints_2d:
        pose_keypoints_2d_split.append(group(keypoint_body, 3))

    hand_left_keypoints_2d_split = []
    for hand_left_keypoint in hand_left_keypoints_2d:
        hand_left_keypoints_2d_split.append(group(hand_left_keypoint, 3))

    hand_right_keypoints_2d_split = []
    for hand_right_keypoint in hand_right_keypoints_2d:
        hand_right_keypoints_2d_split.append(group(hand_right_keypoint, 3))

    face_keypoints_2d_split = []
    for face_keypoint in face_keypoints_2d:
        face_keypoints_2d_split.append(group(face_keypoint, 3))

    
     ## Adds body part name
    for keypoints in pose_keypoints_2d_split:
        for index in range(len(keypoints)):
            keypoints[index].append(keypoints_IDs[index][0])
            keypoints[index].append(keypoints_IDs[index][1])
    
    for keypoints_face in face_keypoints_2d_split:
        for index in range(len(keypoints_face)):
            keypoints_face[index].append(face_IDs[index][0])
            keypoints_face[index].append(face_IDs[index][1])

    for keypoints_hand_left in hand_left_keypoints_2d_split:
        for index in range(len(keypoints_hand_left)):
            keypoints_hand_left[index].append(hand_IDs[index][0])
            keypoints_hand_left[index].append(hand_IDs[index][1])

    for keypoints_hand_right in hand_right_keypoints_2d_split:
        for index in range(len(keypoints_hand_right)):
            keypoints_hand_right[index].append(hand_IDs[index][0])
            keypoints_hand_right[index].append(hand_IDs[index][1])
    
    for frame in range(len(face_data)):
        td = str(timedelta(seconds=(frame / FPS)))
        data_list.append({
            "time":td,
            "frame":frame, 
            "pose_keypoints_2d":pose_keypoints_2d_split[frame],
            "face_keypoints_2d":face_keypoints_2d_split[frame],
            "hand_left_keypoints_2d":hand_left_keypoints_2d_split[frame],
            "hand_right_keypoints_2d":hand_right_keypoints_2d_split[frame]
            })

    data_out = {
        "participant":participant,
        "song":song, 
        "data":data_list,
        "framerate":FPS
        }
        
    filename = "../data/" + song + "_" + participant + ".json"
    with open(filename, 'w') as f:
        json.dump(data_out, f)

    print("Merger SUCCESS")
else:
    print("ERROR: data totals do not match")

