from cProfile import label
import json
import sys
from matplotlib import pyplot as plt

filepath = str(sys.argv[1])

# Opening JSON file
with open(filepath, 'r') as f:
  original_data = json.load(f)

# data lists
keypoints_wrists_distance = []

keypoints_RWrist_nose_distance = []
keypoints_RWrist_nose_angle = []
keypoints_LWrist_nose_distance = []
keypoints_LWrist_nose_angle = []
keypoints_direction = []
keypoints_qom = []
keypoints_qom_angle = []
frame_count = []
time = []

# filling data lists with with data from json file
for keypoint in original_data['data']:
    frame_count.append(keypoint['raw']['frame'])
    time.append(keypoint['time'])
    keypoints_wrists_distance.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
    keypoints_RWrist_nose_distance.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
    keypoints_RWrist_nose_angle.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
    keypoints_LWrist_nose_distance.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
    keypoints_LWrist_nose_angle.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
    keypoints_direction.append(keypoint['keypoints_direction'])
    keypoints_qom.append(keypoint['keypoints_fod']['distance_total'])
    keypoints_qom_angle.append(keypoint['keypoints_fod']['angle_total'])

print('frames: '+str(len(frame_count)))

plt.title('Features')
plt.xlabel('Frames')
plt.ylabel('Pixels')

plt.plot(frame_count, keypoints_qom, label='Overall QoM')
plt.plot(frame_count, keypoints_wrists_distance, label='Wrist distances')
plt.plot(frame_count, keypoints_RWrist_nose_distance, label='R wrist-nose distance')
plt.plot(frame_count, keypoints_LWrist_nose_distance, label='L wrist-nose distance')
plt.legend()
plt.show()

