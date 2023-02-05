import json, sys
import math
from turtle import down
from datetime import timedelta

# Gather file path
participant = str(sys.argv[1])
song = str(sys.argv[2])
data_file_path = sys.argv[3]
frameRate = 30

# Opening JSON file
with open(data_file_path, 'r') as f:
  original_data = json.load(f)
  
# lists
pose_keypoints_2d = []
pose_keypoints_2d = []
face_keypoints_2d = []
hand_left_keypoints_2d = []
hand_right_keypoints_2d = []

data_out = []
keypoints_IDs = [[0,  "Nose"], [1,  "Neck"], [2,  "RShoulder"], [3,  "RElbow"], [4,  "RWrist"], [5,  "LShoulder"], [6,  "LElbow"], [7,  "LWrist"], [8,  "MidHip"], [9,  "RHip"],[10, "RKnee"], [11, "RAnkle"], [12, "LHip"], [13, "LKnee"], [14, "LAnkle"], [15, "REye"], [16, "LEye"], [17, "REar"], [18, "LEar"], [19, "LBigToe"], [20, "LSmallToe"], [21, "LHeel"], [22, "RBigToe"], [23, "RSmallToe"], [24, "RHeel"], [25, "Background"]]



# ------ first order difference by frame ------ #
def delta(x0, y0, x1, y1):
    delta = math.sqrt(pow((x1-x0),2)+pow((y1-y0),2))
    return float(delta)

# ------ moving average ------ #
def mavg(index, inArray, windowSize):
    
    indexWindow = 0
    movingAverage = 0

    for indexWindow in range(windowSize):     
        movingAverage = movingAverage + inArray[index-indexWindow]
    
    movingAverage /= windowSize

    return movingAverage

# ------ Directions ------ #
def direction(x0, y0, x1, y1):
    h = "nill"
    v = "nill"
    # direction horizontal
    if x1 < x0:
        h = "right"
    else:
        h = "left"
    # direction vertical axis
    if y1 < y0:
        v = "down"
    else:
        v = "up"
    return h + "_" + v

# Returns JSON object as a dictionary
for keypoint in original_data["data"]:
    pose_keypoints_2d.append(keypoint["pose_keypoints_2d"])
    face_keypoints_2d.append(keypoint["face_keypoints_2d"])
    hand_left_keypoints_2d.append(keypoint["hand_left_keypoints_2d"])
    hand_right_keypoints_2d.append(keypoint["hand_right_keypoints_2d"])    


# Creates an object that includes wrists and shouler data only

wristsShoulderRaw = []
for index in range(len(pose_keypoints_2d)):
    wristsShoulderRaw.append({
        "raw_r_wrist":pose_keypoints_2d[index][4],
        "raw_l_wrist":pose_keypoints_2d[index][7],
        "raw_r_shoulder":pose_keypoints_2d[index][2],
        "raw_l_shoulder":pose_keypoints_2d[index][5],
        })

pose_delta = []
previous = pose_keypoints_2d[0]


# calculates delta
for keypoints in pose_keypoints_2d:
    delta_keypoints_frame = []
    delta_total = 0
    angle_total = 0
    mav = []
    for index in range(len(keypoints)):
        pose_delta_dist = delta(previous[index][0], keypoints[index][0], previous[index][1], keypoints[index][0])
        angle_radians = math.atan2(keypoints[index][0]-previous[index][0], keypoints[index][1]-previous[index][0])
        angle_degrees = math.degrees(angle_radians)
        delta_total = delta_total + pose_delta_dist
        angle_total = angle_total + abs(angle_degrees)
        

        delta_keypoints_frame.append(
            {"keypoint_no":keypoints_IDs[index][0],
            "keypoint_name":keypoints_IDs[index][1], 
            "delta":pose_delta_dist, 
            "angle":angle_degrees,
            })

    pose_delta.append({
        "delta_total":delta_total, 
        "angle_total":angle_total, 
        "keypoints": delta_keypoints_frame
        })
    

    previous = keypoints


# ------ Distances ------ #
wrists_deltas = []
lwrist_nose_deltas = []
rwrist_nose_deltas = []

for keypoints in pose_keypoints_2d:
    wrist_0_x = keypoints[4][0] # right
    wrist_0_y = keypoints[4][1] # right
    wrist_1_x = keypoints[7][0] # left
    wrist_1_y = keypoints[7][1] # left
    nose_x = keypoints[0][0]
    nose_y = keypoints[0][1]    

    # wrists delta/angle
    wrists_delta = math.sqrt(pow((wrist_1_x-wrist_0_x),2)+pow((wrist_1_y-wrist_0_y),2))
    wrists_angle_radians = math.atan2(wrist_0_x-wrist_1_x, wrist_0_y-wrist_1_y)
    wrists_angle_degrees = math.degrees(wrists_angle_radians)
    wrists_deltas.append({"wrists_delta":wrists_delta, "wrists_angle":wrists_angle_degrees})

    # wrist 0 nose disance/angle
    rwrist_nose_delta = math.sqrt(pow((nose_x-wrist_0_x),2)+pow((nose_y-wrist_0_y),2))
    rwrist_nose_angle_radians = math.atan2(wrist_0_x-nose_x, wrist_0_y-nose_y)
    rwrist_nose_angle_degrees = math.degrees(rwrist_nose_angle_radians)
    rwrist_nose_deltas.append(
        {"keypoint_no":keypoints_IDs[4][0],
        "keypoint_name":keypoints_IDs[4][1], 
        "r_wrist_nose_delta":rwrist_nose_delta, 
        "r_wrist_nose_angle_degrees":rwrist_nose_angle_degrees
        })

    # wrist 0 nose disance/angle
    lwrist_nose_delta = math.sqrt(pow((nose_x-wrist_1_x),2)+pow((nose_y-wrist_1_y),2))
    lwrist_nose_angle_radians = math.atan2(wrist_1_x-nose_x, wrist_1_y-nose_y)
    lwrist_nose_angle_degrees = math.degrees(lwrist_nose_angle_radians)
    lwrist_nose_deltas.append({
        "keypoint_no":keypoints_IDs[7][0],
        "keypoint_name":keypoints_IDs[7][1],
        "l_wrist_nose_delta":lwrist_nose_delta, 
        "l_wrist_nose_delta":lwrist_nose_delta
        })

# ------ Directions ------ #

segments = []
previous_frame_no = 2 # in frames
angle_threshold = 45 # in degrees
segment_change_count = 0

for keypoints_index in range(0, len(pose_keypoints_2d)):
    directions_second = []
    directions_angle = []
    segment_data = []
    keypoints = pose_keypoints_2d[keypoints_index]

    if keypoints_index > previous_frame_no:
        previous_window = pose_keypoints_2d[keypoints_index-previous_frame_no] # takes 5th previous sample

        for index in range(0, len(keypoints)):

            # angle between of the keypoint displacement frame by frame
            previous_angle_radians = math.atan2(keypoints[index][0]-previous_window[index][0], keypoints[index][1]-previous_window[index][0])
            previous_angle_degrees = math.degrees(previous_angle_radians)
            
            angle_radians = math.atan2(keypoints[index][0]-previous[index][0], keypoints[index][1]-previous[index][0])
            angle_degrees = math.degrees(angle_radians)
            delta_angle = abs(previous_angle_degrees-angle_degrees)

            if delta_angle > angle_threshold:
                segment_change = 1
                segment_change_count = segment_change_count + 1
                #print(segment_change_count)
                # direction of displacement frame by frame on the horizontal and vertical axis
                direction_text = direction(previous_window[index][0], previous_window[index][1], keypoints[index][0], keypoints[index][1])
            else:
                direction_text = "none"
                segment_change = 0
            
            segment_data.append({
                "keypoint_no":keypoints_IDs[index][0],
                "keypoint_name":keypoints_IDs[index][1], 
                "change":segment_change, 
                "direction":direction_text, 
                "angle_delta":delta_angle, 
                "angle_degree":angle_degrees
                })

    previous = keypoints
    segments.append(segment_data)


# Hands data feature extraction
original_data_lenght = (len(original_data["data"]))


quantityOfMotion = []

# Creates files
if (original_data_lenght == len(pose_delta) == len(wrists_deltas) == len(lwrist_nose_deltas) == len(segments)): # checks that no data were lost
    for frame in range(original_data_lenght):
        keypoints_delta = pose_delta[frame]
        keypoints_wrists_delta = wrists_deltas[frame]
        keypoints_LWrist_nose_delta = lwrist_nose_deltas[frame]
        keypoints_RWrist_nose_delta = rwrist_nose_deltas[frame]
        keypoints_direction = segments[frame]
        raw = original_data["data"][frame]
        raw_wrists_shoulders = wristsShoulderRaw[frame]
        movingAverage = []
        frame_count = frame
        td = str(timedelta(seconds=(frame_count / frameRate)))
        
        quantityOfMotion.append(keypoints_delta['delta_total'])

        # moving averages
        mavgWindowSize = 10
        if frame<mavgWindowSize:
            deltaMavg = 0

        if frame > mavgWindowSize-1:
            deltaMavg = mavg(frame, quantityOfMotion, mavgWindowSize)
            

        data_out.append({
            "time":td,
            "frame":frame, 
            "time":td,
            "raw":raw,
            "keypoints_delta":keypoints_delta, 
            "keypoints_wrists_delta":keypoints_wrists_delta, 
            "keypoints_LWrist_nose_delta":keypoints_LWrist_nose_delta,
            "keypoints_RWrist_nose_delta":keypoints_RWrist_nose_delta, 
            "keypoints_direction":keypoints_direction, # segment_change, direction_text, delta_angle, angle_degrees
            "raw_wrists_shoulders": raw_wrists_shoulders,
            "delta_mavg": deltaMavg,
            })
     
    final_out = {
        
        "data":data_out, 
        "frameRate":frameRate,
        "participant":participant, 
        "song":song
        }
    
    filename = "./data/" + song + "_" + participant + "_features.json"
    with open(filename, 'w') as f:
        json.dump(final_out, f)

    print("Feature extraction SUCCESS")
else:
    print("ERROR: feature extraction failed. Data count does not match.")