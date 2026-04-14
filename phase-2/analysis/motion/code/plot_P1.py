import json

# data lists
wrists_distance_1A = []
RWrist_nose_distance_1A = []
RWrist_nose_angle_1A = []
LWrist_nose_distance_1A = []
LWrist_nose_angle_1A = []
direction_1A = []
qom_1A = []
qom_angle_1A = []
frame_count_1A = []
time_1A = []

wrists_distance_1D = []
RWrist_nose_distance_1D = []
RWrist_nose_angle_1D = []
LWrist_nose_distance_1D = []
LWrist_nose_angle_1D = []
direction_1D = []
qom_1D = []
qom_angle_1D = []
frame_count_1D = []
time_1D = []

def fill_lists_p1():

    with open('data/Apparat_Goodbye_P1_features.json', 'r') as f:
        original_data_1A = json.load(f)
    
    with open('data/DaftPunk_Crescendools_P1_features.json', 'r') as f:
        original_data_1D = json.load(f)

    for keypoint in original_data_1A['data']:
        frame_count_1A.append(keypoint['raw']['frame'])
        time_1A.append(keypoint['time'])
        wrists_distance_1A.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
        RWrist_nose_distance_1A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        RWrist_nose_angle_1A.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        LWrist_nose_distance_1A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        LWrist_nose_angle_1A.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        direction_1A.append(keypoint['keypoints_direction'])
        qom_1A.append(keypoint['keypoints_fod']['distance_total'])
        qom_angle_1A.append(keypoint['keypoints_fod']['angle_total'])

    for keypoint in original_data_1D['data']:
        frame_count_1D.append(keypoint['raw']['frame'])
        time_1D.append(keypoint['time'])
        wrists_distance_1D.append(keypoint['keypoints_wrists_distance_angle']['wrists_distance'])
        RWrist_nose_distance_1D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        RWrist_nose_angle_1D.append(keypoint['keypoints_RWrist_nose_distance_angle']['r_wrist_nose_distance'])
        LWrist_nose_distance_1D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        LWrist_nose_angle_1D.append(keypoint['keypoints_LWrist_nose_distance_angle']['l_wrist_nose_distance'])
        direction_1D.append(keypoint['keypoints_direction'])
        qom_1D.append(keypoint['keypoints_fod']['distance_total'])
        qom_angle_1D.append(keypoint['keypoints_fod']['angle_total'])