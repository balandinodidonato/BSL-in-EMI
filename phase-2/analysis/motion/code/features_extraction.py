from cmath import sqrt
import numpy as np
import json, sys

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
data_file_path = sys.argv[3]

# Opening JSON file
data_file = open(data_file_path)

# lists
pose_keypoints_2d = []
pose_keypoints_2d_split = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []

pose_fod = []
pose_fod_max = 0
pose_fod_min = 2000

# Returns JSON object as a dictionary
data = json.load(data_file)
dataN= len(data)

for index in data:
    pose_keypoints_2d.append(index["pose_keypoints_2d"])
    face_keypoints_2d.append(index["face_keypoints_2d"])
    hand_left_keypoints_2d.append(index["hand_left_keypoints_2d"])
    hand_right_keypoints_2d.append(index["hand_right_keypoints_2d"])    
    
# split list
def group(theList, N):
    return [theList[n:n+N] for n in range(0, len(theList), N)]

for data_ in pose_keypoints_2d:
    pose_keypoints_2d_split.append(group(data_, 3))

# ------ First order difference, displacement of each joint frame by frame ------ #
def fod(x0, y0, x1, y1):
    return sqrt(pow((x1-x0),2)+pow((y1-y0),2))

previous = pose_keypoints_2d_split[0][0]
for keypoints in pose_keypoints_2d_split:
    for keypoint in keypoints:
        pose_fod.append(fod(previous[0], previous[1], keypoint[0], keypoint[1]))
        previous = keypoint

print(len(pose_fod))
print(dataN)

data_out = []
for frame in range(dataN):
    test = pose_fod[frame]
    data_out.append({"participant":participant, "song":song, "fod":test})

filename = song + "_" + participant + "_features.json"
with open(filename, 'w') as f:
    json.dump(data_out, f)