import json

# data lists
wrists_distance_2A = []
RWrist_nose_distance_2A = []
RWrist_nose_angle_2A = []
LWrist_nose_distance_2A = []
LWrist_nose_angle_2A = []
direction_2A = []
qom_2A = []
qom_angle_2A = []
frame_count_2A = []
time_2A = []

wrists_distance_2D = []
RWrist_nose_distance_2D = []
RWrist_nose_angle_2D = []
LWrist_nose_distance_2D = []
LWrist_nose_angle_2D = []
direction_2D = []
qom_2D = []
qom_angle_2D = []
frame_count_2D = []
time_2D = []
raw_wrists_shoulders_2A = []

def fill_lists_p2():

    with open('data/Apparat_Goodbye_P2_features.json', 'r') as f:
        original_data_2A = json.load(f)
    
#    with open('data/DaftPunk_Crescendools_P2_features.json', 'r') as f:
#        original_data_2D = json.load(f)

    for keypoint in original_data_2A['data']:
        frame_count_2A.append(keypoint['raw']['frame'])
     #   time_2A.append(keypoint['time'])
      #  wrists_distance_2A.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
      #  RWrist_nose_distance_2A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
      #  RWrist_nose_angle_2A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
      #  LWrist_nose_angle_2A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
      #  LWrist_nose_distance_2A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
      #  direction_2A.append(keypoint['keypoints_direction'])
        qom_2A.append(keypoint['delta_mavg'])
        raw_wrists_shoulders_2A.append(keypoint['raw_wrists_shoulders']['raw_r_wrist'][1])
      #  qom_angle_2A.append(keypoint['keypoints_fod']['angle_total'])

 #   for keypoint in original_data_2D['data']:
      #  frame_count_2D.append(keypoint['raw']['frame'])
      #  wrists_distance_2D.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
      #  time_2D.append(keypoint['time'])
      #  RWrist_nose_distance_2D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
      #  RWrist_nose_angle_2D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
      #  LWrist_nose_distance_2D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
      #  LWrist_nose_angle_2D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
      #  direction_2D.append(keypoint['keypoints_direction'])
  #      qom_2D.append(keypoint['keypoints_delta']['delta_total'])
      #  qom_angle_2D.append(keypoint['keypoints_fod']['angle_total'])