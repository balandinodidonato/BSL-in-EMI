# Created by Balandino Di Donato as part of the BSL in EMI project funded by Creative Informatics
# This script merges body, face and hand data into a single json file.

import json, sys

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
face_file_path = sys.argv[3] # Path to face data set
hand_file_path = sys.argv[4] # Path to face data set

# Opening JSON file
face_file = open(face_file_path)
hand_file = open(hand_file_path)

# Returns JSON object as a dictionary
face_data = json.load(face_file)
hand_data = json.load(hand_file)
  
# Lists and variables
pose_keypoints_2d = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []
data_list = []
participantNo = 1

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

# Closing file
face_file.close()
hand_file.close()

# tests on wether the two JSON contains the same number of objects
if(len(face_data)==len(face_data)):
    for frame in range(len(face_data)):
        body = pose_keypoints_2d[frame]
        f_data = face_keypoints_2d[frame]
        hl_data = hand_left_keypoints_2d[frame]
        hr_data = hand_right_keypoints_2d[frame]
        data_list.append({"participant":participantNo, "song":song, "frame":frame, "pose_keypoints_2d":body, "face_keypoints_2d":f_data, "hand_left_keypoints_2d":hl_data, "hand_right_keypoints_2d":hr_data})

    filename = song + "_" + participant + ".json"
    with open(filename, 'w') as f:
        json.dump(data_list, f)