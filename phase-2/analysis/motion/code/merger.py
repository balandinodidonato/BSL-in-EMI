# This script merges all json file from two folders, one with face+body data and with body+hand dta into a JSON file 

# Dependecies
import glob, json
from sre_constants import SUCCESS
import sys
from datetime import timedelta

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

for f in glob.glob(face_file_path+"/*.json"):
    with open(f,) as infile:
        face_data.append(json.load(infile))

for f in glob.glob(hand_file_path+"/*.json"):
    with open(f,) as infile:
        hand_data.append(json.load(infile))

face_data_tot = len(face_data)
hand_data_tot = len(hand_data)

# iterates through the JSON with the face data and extracts the face keypoints

for object in face_data:
    if len(object["people"]):
        for people in object["people"]:
            face_keypoints_2d.append(people["face_keypoints_2d"])
    else:
        face_keypoints_2d.append(empty_face_keypoints_2d)

# iterates through the JSON with the hand data and extracts the hand keypoints
for object in hand_data:
    if len(object["people"]):
        for people in object["people"]:
            pose_keypoints_2d.append(people["pose_keypoints_2d"])
            hand_left_keypoints_2d.append(people["hand_left_keypoints_2d"])
            hand_right_keypoints_2d.append(people["hand_right_keypoints_2d"])
    else:
        pose_keypoints_2d.append(empty_pose_keypoints_2d)
        hand_left_keypoints_2d.append(empty_hand_keypoints_2d)
        hand_right_keypoints_2d.append(empty_hand_keypoints_2d)

if(len(pose_keypoints_2d)==len(hand_left_keypoints_2d)==len(hand_right_keypoints_2d)==len(face_keypoints_2d)==face_data_tot==hand_data_tot):
    for frame in range(len(face_data)):
        td = str(timedelta(seconds=(frame / FPS)))
        data_list.append({
            "participant":participant,
            "song":song, 
            "time":td,
            "frame":frame, 
            "pose_keypoints_2d":pose_keypoints_2d[frame],
            "face_keypoints_2d":face_keypoints_2d[frame],
            "hand_left_keypoints_2d":hand_left_keypoints_2d[frame],
            "hand_right_keypoints_2d":hand_right_keypoints_2d[frame]
            })

    filename = "../data/" + song + "_" + participant + ".json"
    with open(filename, 'w') as f:
        json.dump(data_list, f)
    print("Merger SUCCESS")
else:
    print("ERROR: data totals do not match")