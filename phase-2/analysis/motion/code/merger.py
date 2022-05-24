# This script merges all json file from two folders, one with face+body data and with body+hand dta into a JSON file 

# Dependecies
import glob, json
import sys

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
face_file_path = sys.argv[3] # Path to face data set
hand_file_path = sys.argv[4] # Path to face data set

# Lists and variables
pose_keypoints_2d = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []
data_list = []
face_data = []
hand_data = []

for f in glob.glob(face_file_path+"/*.json"):
    with open(f,) as infile:
        face_data.append(json.load(infile))

for f in glob.glob(hand_file_path+"/*.json"):
    with open(f,) as infile:
        hand_data.append(json.load(infile))

# iterates through the JSON with the face data and extracts the face keypoints
for object in face_data:
    for people in object["people"]:
        face_keypoints_2d.append(people["face_keypoints_2d"])

# iterates through the JSON with the hand data and extracts the hand keypoints
for object in hand_data:
    for people in object["people"]:
        pose_keypoints_2d.append(people["pose_keypoints_2d"])
        hand_left_keypoints_2d.append(people["hand_left_keypoints_2d"])
        hand_right_keypoints_2d.append(people["hand_right_keypoints_2d"])

# tests on wether the two JSON contains the same number of objects
if(len(face_data)==len(face_data)):
    for frame in range(len(face_data)):
        body = pose_keypoints_2d[frame]
        f_data = face_keypoints_2d[frame]
        hl_data = hand_left_keypoints_2d[frame]
        hr_data = hand_right_keypoints_2d[frame]
        data_list.append({"participant":participant, "song":song, "frame":frame, "pose_keypoints_2d":body, "face_keypoints_2d":f_data, "hand_left_keypoints_2d":hl_data, "hand_right_keypoints_2d":hr_data})

    filename = "../data/" + song + "_" + participant + ".json"
    with open(filename, 'w') as f:
        json.dump(data_list, f)