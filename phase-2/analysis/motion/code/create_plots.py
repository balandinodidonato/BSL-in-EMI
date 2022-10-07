from cProfile import label
import json
import sys
from matplotlib import pyplot as plt

filepath = str(sys.argv[1])
plots = str(sys.argv[2])
participant_no = str(sys.argv[3])

my_dpi = 100

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

plt.figure(figsize=(2000/my_dpi, 720/my_dpi), dpi=my_dpi)

plt.title('Participant no. '+participant_no)
plt.xlabel('Frames')
plt.ylabel('Pixels')

if plots == 'qom':
    plt.plot(frame_count, keypoints_qom, label='Overall QoM')

elif plots == 'wrists':
    plt.plot(frame_count, keypoints_wrists_distance, label='Wrist distances')
    plt.plot(frame_count, keypoints_RWrist_nose_distance, label='R wrist-nose distance')
    plt.plot(frame_count, keypoints_LWrist_nose_distance, label='L wrist-nose distance')


plt.legend()
plt.savefig('./plot/'+plots+'_P'+participant_no+'.png', bbox_inches='tight')

