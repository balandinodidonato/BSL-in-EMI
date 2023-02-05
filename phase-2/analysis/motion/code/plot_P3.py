import json

# data lists
wrists_distance_3A = []
RWrist_nose_distance_3A = []
RWrist_nose_angle_3A = []
LWrist_nose_distance_3A = []
LWrist_nose_angle_3A = []
direction_3A = []
qom_3A = []
qom_angle_3A = []
frame_count_3A = []
time_3A = []

wrists_distance_3D = []
RWrist_nose_distance_3D = []
RWrist_nose_angle_3D = []
LWrist_nose_distance_3D = []
LWrist_nose_angle_3D = []
direction_3D = []
qom_3D = []
qom_angle_3D = []
frame_count_3D = []
time_3D = []

raw_wrists_shoulders_3A = []

def fill_lists_p3():

    with open('data/Apparat_Goodbye_P3_features.json', 'r') as f:
        original_data_3A = json.load(f)
    
 #   with open('data/DaftPunk_Crescendools_P3_features.json', 'r') as f:
 #       original_data_3D = json.load(f)

    for keypoint in original_data_3A['data']:
        frame_count_3A.append(keypoint['raw']['frame'])
      #  time_3A.append(keypoint['time'])
        #wrists_distance_3A.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
        #RWrist_nose_distance_3A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        #RWrist_nose_angle_3A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        #LWrist_nose_distance_3A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        #LWrist_nose_angle_3A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        #direction_3A.append(keypoint['keypoints_direction'])
        qom_3A.append(keypoint['delta_mavg'])
        raw_wrists_shoulders_3A.append(keypoint['raw_wrists_shoulders']['raw_r_wrist'][1])

        #qom_angle_3A.append(keypoint['keypoints_fod']['angle_total'])

  #  for keypoint in original_data_3D['data']:
  #      frame_count_3D.append(keypoint['raw']['frame'])
  #      time_3D.append(keypoint['time'])
        #wrists_distance_3D.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
        #RWrist_nose_angle_3D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        #LWrist_nose_distance_3D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        #RWrist_nose_distance_3D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        #LWrist_nose_angle_3D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        #direction_3D.append(keypoint['keypoints_direction'])
  #      qom_3D.append(keypoint['keypoints_delta']['delta_total'])
        #qom_angle_3D.append(keypoint['keypoints_fod']['angle_total'])