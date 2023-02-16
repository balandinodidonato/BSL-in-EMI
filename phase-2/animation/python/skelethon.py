import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import json
import matplotlib.lines as lines

# Gather file path
data_file_path = sys.argv[1]
frameRate = 30
videoResolution = [1920, 1080]

# Opening JSON file
with open(data_file_path, 'r') as f:
  original_data = json.load(f)

keypoints = []

for keypoint in original_data["data"]:
    keypoints.append(keypoint["raw"]["pose_keypoints_2d"])

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create rain data
n_points = 13
joints = 25

points = np.zeros(n_points, dtype=[('position', float, (2,)),
                                      ('size',     float),
                                      ('color',    float, (4,))])

# Initialize the raindrops in random positions and with
# random growth rates.
points['position'] = [-1, -1]

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(points['position'][:, 0], points['position'][:, 1],
                  s=points['size'], lw=0.5, edgecolors=points['color'],
                  facecolors='none')
lineDraw = []
for lines in range(n_points):
  line, = ax.plot([], [], 'o-', lw=2)
  lineDraw.append(line)

def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_point = frame_number % n_points
    current_joint = frame_number % joints
    
    # filter joints
    if (current_joint <19):
      if (current_joint<9 or current_joint>14):
        # resscale pointer
        if(current_joint>9):
          current_point = (current_joint-14)+8

        x = keypoints[frame_number][current_joint][0]/videoResolution[0]
        y = 1 - keypoints[frame_number][current_joint][1]/videoResolution[1]

        if frame_number > 10: 
          px = keypoints[frame_number-10][current_joint][0]/videoResolution[0]
          py = 1 - keypoints[frame_number-10][current_joint][1]/videoResolution[1]
        else:
          px = x
          py = y

        thisx = [px, x]
        thisy = [py, y]
        #lineDraw[current_joint].set_data(thisx, thisy)   

        points['position'][current_point] = [x,y]
        points['size'][current_point] = 5
        points['color'][current_point] = (1, 0, 0, 1)
        # points['growth'][current_point] = np.random.uniform(50, 200)

        # Update the scatter collection, with the new colors, sizes and positions.
        scat.set_edgecolors(points['color'])
        scat.set_color(points['color'])
        scat.set_sizes(points['size'])
        scat.set_offsets(points['position'])

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()