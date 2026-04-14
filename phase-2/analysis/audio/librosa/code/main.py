import librosa

# 1. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load('audio/hIrskyj-douglas/music.mp3')

# 2. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Prints the tempo of the audio in beats per minutes
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# 3. Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)