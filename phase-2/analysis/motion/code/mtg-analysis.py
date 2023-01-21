import musicalgestures
import sys

video_file_name = str(sys.argv[1])
source_audio = str(sys.argv[2])

source_video = musicalgestures.MgVideo(video_file_name)


# MOTIONGRAMS
motiongrams = source_video.motiongrams() # this renders only the motiongrams
motiongrams.show() # show both motiongrams
motiongrams[0].show() # show horizontal motiongram
motiongrams[1].show() # show vertical motiongram


# MOTION SSM
motionssm = source_video.ssm(features='motiongrams') # returns an MgList with the motion SSMs as MgImages
motionssm.show() # view both SSMs
motionssm[0].show() # view horizontal motiongram SSM
motionssm[1].show() # view vertical motiongram SSM
source_video.show(key='ssm') # view both SSMs
motionssm = source_video.ssm(features='motiongrams', cmap='viridis', norm=2)


# MOTION DATA
motion_video = source_video.motion() # process the video
motion_video.show() # view the result
source_video.show(key='motion') # another way to view the result, since the rendered motion video is now also referenced at the source `MgVideo`
motiondata = source_video.motiondata() # this renders only the motion data, returns the path to the rendered data file


# MOTION PLOTS
motionplots = source_video.motionplots() # this renders only the motion plots (returns an MgImage)
motionplots.show() # directly from variable
source_video.show(key='plot') # or from source MgVideo
motionplots = source_video.motionplots(audio_descriptors=True)


# VIDEOGRAMS
videograms = source_video.videograms() # returns an MgList with the videograms as MgImages
videograms.show() # view both videograms
videograms[0].show() # view horizontal videogram
videograms[1].show() # view vertical videogram
source_video.show(key='mgx') # from the source MgVideo view horizontal videogram
source_video.show(key='mgy') # from the source MgVideo view vertical videogram


# DIRECTOGRAMS
directograms = source_video.directograms() # returns an MgFigure with the directogram as figure
directograms.data['directogram'] # access directogram data
directograms.show() # view results view directograms


# WRAP AUDIO AND VISUAL BEATS
warp = source_video.warp_audiovisual_beats(source_audio) # returns an MgVideo with audio and visual beats warped
warp.show() # either like this
source_video.show(key='warp') # or like this (referenced from source MgVideo)
directogram = source_video.directograms() # Directogram separately
source_video.warp_audiovisual_beats(source_audio, data=directogram.data['directogram'])


# IMPACT
impact_envelopes = source_video.impacts(detection=False) # returns an MgFigure with the impact envelopes
impact_detection = source_video.impacts(detection=True, local_mean=0.1, local_maxima=0.15) # returns an MgFigure with the impact detection based on local mean and maxima
impact_envelopes.data['impact envelopes'] # access impacts envelope data
impact_envelopes.show() # view impact envelopes
impact_detection.show() # view impact envelopes with impact detection


# HISTORY
history = source_video.history(history_length=20) # returns an MgVideo with the history video
history.show() # view result either like this
source_video.show(key='history') # or like this (referenced from source MgVideo)


# MOTION HISTORY
motionhistory = source_video.motionvideo().history() # chaining motionvideo into history
motionhistory.show() # view result either like this
source_video.show(key='motionhistory') # or like this (referenced from source MgVideo)


## MOTION AVERAGE
motion_average = source_video.motionvideo().average() # motionvideo chained into an average image
motion_average.show() # view result


## AVERAGE
average = source_video.average() # average image (returns an MgImage)
average.show() # view result either like this
source_video.show(key='average') # or like this (referenced from source MgVideo)


# FLOW SPARSE
flow_sparse = source_video.flow.sparse() # sparse optical flow
flow_sparse.show() # view result either like this
source_video.show(key='sparse') # or like this (referenced from source MgVideo)


# FLOW DENSE
flow_dense = source_video.flow.dense() # dense optical flow
flow_dense.show() # view result either like this
source_video.show(key='dense') # or like this (referenced from source MgVideo)


# POSE
pose = source_video.pose(downsampling_factor=1, threshold=0.05, model='BODY_25', device='gpu', save_data=True) # We use the BODY_25 model. This is the fastest one on the GPU, the most accurate one, and the one with the highest number of keypoints (including foot keypoints!), highly recommended. It also uses the most amount of RAM/GPU memory. (Source: https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_05_faq.html)
flow_dense.show() # view result either like this
source_video.show(key='pose') # or like this (referenced from source MgVideo)