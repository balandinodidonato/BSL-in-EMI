# Created by Balandino Di Donato as part of the BSL in EMI project funded by Creative Informatics

import json, sys

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
face_file_path = sys.argv[3]
hand_file_path = sys.argv[4]

# Opening JSON file
face_file = open(face_file_path)
hand_file = open(hand_file_path)

# Returns JSON object as a dictionary
face_data = json.load(face_file)
hand_data = json.load(hand_file)
  
# Lists and variables
countFace = 0
countHand = 0
pose_keypoints_2d = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []
data_list = []
participantNo = 1

# iterates through the JSON with the face data and extracts the face keypoints
for object in face_data:
    countFace = countFace + 1
    for people in object["people"]:
        face_keypoints_2d.append(people["face_keypoints_2d"])

# iterates through the JSON with the hand data and extracts the hand keypoints
for object in hand_data:
    countHand = countHand + 1
    for people in object["people"]:
        pose_keypoints_2d.append(people["pose_keypoints_2d"])
        hand_left_keypoints_2d.append(people["hand_left_keypoints_2d"])
        hand_right_keypoints_2d.append(people["hand_right_keypoints_2d"])

# Closing file
face_file.close()
hand_file.close()

# tests on wether the two JSON contains the same number of objects
if(countFace==countHand):
    for index in range(countFace):
        body = pose_keypoints_2d[index]
        f_data = face_keypoints_2d[index]
        hl_data = hand_left_keypoints_2d[index]
        hr_data = hand_right_keypoints_2d[index]
        data_list.append({"participant":participantNo, "song":"goodbye_apparat", "index":index, "pose_keypoints_2d":body, "face_keypoints_2d":f_data, "hand_left_keypoints_2d":hl_data, "hand_right_keypoints_2d":hr_data})

    filename = song + "_" + participant + ".json"
    with open(filename, 'w') as f:
        json.dump(data_list, f)