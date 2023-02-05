from pickle import SHORT_BINSTRING
import sys
from matplotlib import pyplot as plt
from plot_P1 import *
from plot_P2 import *
from plot_P3 import *

plots = str(sys.argv[1])
participant_no = str(sys.argv[2])
song = str(sys.argv[3])

my_dpi = 100

# filling data lists with with data from json file
fill_lists_p1()
fill_lists_p2()
fill_lists_p3()

# Apparat - Goodbye
plt.figure(figsize=(2000/my_dpi, 720/my_dpi), dpi=my_dpi)

plt.title(plots)
plt.xlabel('Frames')
plt.ylabel('Pixels')



if song == 'A' or song == 'both':
    if plots == 'qom':
            plt.plot(frame_count_1A, qom_1A, label='1A -Overall QoM')
            plt.plot(frame_count_2A, qom_2A, label='2A -Overall QoM')
            plt.plot(frame_count_3A, qom_3A, label='3A -Overall QoM')

    elif plots == 'wrists':
        if participant_no == '1' or participant_no == '1_2' or participant_no == '1_3' or participant_no == '1_2_3':
            plt.plot(frame_count_1A, wrists_distance_1A, label='1A - Wrists distances')
            plt.plot(frame_count_1A, RWrist_nose_distance_1A, label='1A - R wrist-nose distance')
            plt.plot(frame_count_1A, LWrist_nose_distance_1A, label='1A - L wrist-nose distance')
        
        if participant_no == '2' or participant_no == '1_2' or participant_no == '2_3' or participant_no == '1_2_3':
            plt.plot(frame_count_2A, wrists_distance_2A, label='2A - Wrists distances')
            plt.plot(frame_count_2A, RWrist_nose_distance_2A, label='2A - R wrist-nose distance')
            plt.plot(frame_count_2A, LWrist_nose_distance_2A, label='2A - L wrist-nose distance')

        if participant_no == '3' or participant_no == '1_3' or participant_no == '2_3' or participant_no == '1_2_3':
            plt.plot(frame_count_2A, wrists_distance_2A, label='3A - Wrists distances')
            plt.plot(frame_count_2A, RWrist_nose_distance_2A, label='3A - R wrist-nose distance')
            plt.plot(frame_count_2A, LWrist_nose_distance_2A, label='3A - L wrist-nose distance')

    plt.legend()
    plt.savefig('./plot/'+plots+'_P'+participant_no+'A.png', bbox_inches='tight')


elif song == 'D' or song == 'both':
    # Daft Punk - Crecendools
    if plots == 'qom':
            plt.plot(frame_count_1D, qom_1D, label='1D -Overall QoM')
            plt.plot(frame_count_2D, qom_2D, label='2D -Overall QoM')
            plt.plot(frame_count_3D, qom_3D, label='3D -Overall QoM')

    elif plots == 'wrists':
        if participant_no == '1' or participant_no == '1_2' or participant_no == '1_3' or participant_no == '1_2_3':
            plt.plot(frame_count_1D, wrists_distance_1D, label='1D - Wrists distances')
            plt.plot(frame_count_1D, RWrist_nose_distance_1D, label='1D - R wrist-nose distance')
            plt.plot(frame_count_1D, LWrist_nose_distance_1D, label='1D - L wrist-nose distance')

        if participant_no == '2' or participant_no == '1_2' or participant_no == '2_3' or participant_no == '1_2_3':
            plt.plot(frame_count_2D, wrists_distance_2D, label='2D - Wrists distances')
            plt.plot(frame_count_2D, RWrist_nose_distance_2D, label='2D - R wrist-nose distance')
            plt.plot(frame_count_2D, LWrist_nose_distance_2D, label='2D - L wrist-nose distance')

        if participant_no == '3' or participant_no == '1_3' or participant_no == '2_3' or participant_no == '1_2_3':
            plt.plot(frame_count_2D, wrists_distance_2D, label='3D - Wrists distances')
            plt.plot(frame_count_2D, RWrist_nose_distance_2D, label='3D - R wrist-nose distance')
            plt.plot(frame_count_2D, LWrist_nose_distance_2D, label='3D - L wrist-nose distance')

    plt.legend()
    plt.savefig('./plot/'+plots+'_P'+participant_no+'D.png', bbox_inches='tight')

