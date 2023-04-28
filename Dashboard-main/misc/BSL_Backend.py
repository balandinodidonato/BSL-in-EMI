#version 8
import json
import numpy as np
import glob
import os
import librosa
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader

body25Mappings={
	0:	"Nose",
	1:	"Neck",
	2:	"RShoulder",
	3:	"RElbow",
	4:	"RWrist",
	5:	"LShoulder",
	6:	"LElbow",
	7:	"LWrist",
	8:	"MidHip",
	9:	"RHip",
	10:	"RKnee",
	11:	"RAnkle",
	12:	"LHip",
	13:	"LKnee",
	14:	"LAnkle",
	15:	"REye",
	16:	"LEye",
	17:	"REar",
	18:	"LEar",
	19:	"LBigToe",
	20:	"LSmallToe",
	21:	"LHeel",
	22:	"RBigToe",
	23:	"RSmallToe",
	24:	"RHeel"
	}

faceMappings={
0: 'RChic_6',
1:'RChic_5',
2:'RChic_4',
3:'RChic_3',
4:'RChic_2',
5:'RChic_1',
6:'RChic_0',
7:'RMento',
8:'Mento',
9: 'LMento',
10: 'LChic_0',
11: 'LChic_1',
12: 'LChic_2',
13: 'LChic_3',
14: 'LChic_45',
15: 'LChic_5',
16: 'LChic_6',
17: 'REyelashes_4',
18: 'REyelashes_3',
19: 'REyelashes_2',
20: 'REyelashes_1',
21: 'REyelashes_0',
22: 'LEyelashes_0',
23: 'LEyelashes_1',
24: 'LEyelashes_2',
25: 'LEyelashes_3',
26: 'LEyelashes_4',
27: 'Nose_0',
28: 'UNose_1',
29: 'UNose_2',
30: 'UNose_3',
31: 'BNose_0',
32: 'BNose_1',
33: 'BNose_2',
34: 'BNose_3',
35: 'BNose_4',
36: 'REye_R',
37: 'REye_U_1',
38: 'REye_U_0',
39: 'REye_L',
40: 'REye_B_0',
41: 'REye_B_1',
42: 'LEye_R',
43: 'LEye_U_1',
44: 'LEye_U_0',
45: 'LEye_L',
46: 'LEye_B_0',
47: 'LEye_B_1',
48: 'OMouth_R',
49: 'OMouth_U_0',
50: 'OMouth_U_1',
51: 'OMouth_U_2',
52: 'OMouth_U_3',
53: 'OMouth_U_4',
54: 'OMouth_L',
55: 'OMouth_B_4',
56: 'OMouth_B_3',
57: 'OMouth_B_2',
58: 'OMouth_B_1',
59: 'OMouth_B_0',
60: 'IMouth_R',
61: 'IMouth_U_0',
62: 'IMouth_U_1',
63: 'IMouth_U_3',
64: 'IMouth_L',
65: 'IMouth_B_2',
66: 'IMouth_B_1',
67: 'IMouth_B_0',
68: 'REye',
69: 'LEye'
}

hand_mappings={
0: 'Palm',
1: 'Thumb_0',
2: 'Thumb_1',
3: 'Thumb_2',
4: 'Thumb_3',
5: 'Index_0',
6: 'Index_1',
7: 'Index_2',
8: 'Index_3',
9: 'Midle_0',
10: 'Middle_1',
11: 'Middle_2',
12: 'Middle_3',
13: 'Ring_0',
14: 'Ring_1',
15: 'Ring_2',
16: 'Ring_3',
17: 'Little_0',
18: 'Little_1',
19: 'Little_2',
20: 'Little_3'
}

#reads a json file and returns a dictionary tree that contains numpy arrays that hold the information from the video
#assume you put the output in a variable "videoData"
#videoData["insertGroup"]["insertBodyPart"] will be an array of shape (2,timesteps) that holds that body parts positions
#the groups are:
#body
#face
#hand_left
#hand_right
#to see the body part names for each group look at the top of this file

#for example if you want the y position of the Right Shoulder at frame 123 you would do:
#videoData=ConvertData(...)
#rightShoulder_Y_Position=videoData["body"]["RShoulder"][122][1]


#on top of those the object also includes frame times, which you can find in videoData["frame_time"][insertFrameHere]
#they are held as floats representing seconds
def ConvertData(inputFile,videoWidth=1920,videoHeight=1080,normalizeDimensions=False):
	#loead json
	f=open(inputFile,"r").read()
	data=json.loads(f)

	allData_body=[]
	allData_body_conf=[]
	for i in range(25):
		allData_body.append([])
		allData_body.append([])
		allData_body_conf.append([])
	allData_face=[]
	allData_face_conf=[]
	for i in range(70):
		allData_face.append([])
		allData_face.append([])
		allData_face_conf.append([])
	allData_hand_left=[]
	allData_hand_left_conf=[]
	for i in range(21):
		allData_hand_left.append([])
		allData_hand_left.append([])
		allData_hand_left_conf.append([])
	allData_hand_right=[]
	allData_hand_right_conf=[]
	for i in range(21):
		allData_hand_right.append([])
		allData_hand_right.append([])
		allData_hand_right_conf.append([])
	allData_frame_time=[]

	#load data
	for frameId in range(len(data["data"])):
		pose_keypoints_2d=data["data"][frameId]["raw"]["pose_keypoints_2d"]
		face_keypoints_2d=data["data"][frameId]["raw"]["face_keypoints_2d"]
		hand_left_keypoints_2d=data["data"][frameId]["raw"]["hand_left_keypoints_2d"]
		hand_right_pose_keypoints_2d=data["data"][frameId]["raw"]["hand_right_keypoints_2d"]

		#allData_frame_time.append(data["data"][frameId]["raw"]["time"])
		timeDataSplit=data["data"][frameId]["raw"]["time"].split(":")
		allData_frame_time.append((int(timeDataSplit[0])*3600)+(int(timeDataSplit[1])*60)+(float(timeDataSplit[2])))
		for i in range(25):
			allData_body[i*2].append(pose_keypoints_2d[i][0])
			allData_body[i*2+1].append(pose_keypoints_2d[i][1])
			allData_body_conf[i].append(pose_keypoints_2d[i][2])
		for i in range(70):
			allData_face[i*2].append(face_keypoints_2d[i][0])
			allData_face[i*2+1].append(face_keypoints_2d[i][1])
			allData_face_conf[i].append(face_keypoints_2d[i][2])
		for i in range(21):
			allData_hand_left[i*2].append(hand_left_keypoints_2d[i][0])
			allData_hand_left[i*2+1].append(hand_left_keypoints_2d[i][1])
			allData_hand_left_conf[i].append(hand_left_keypoints_2d[i][2])
		for i in range(21):
			allData_hand_right[i*2].append(hand_right_pose_keypoints_2d[i][0])
			allData_hand_right[i*2+1].append(hand_right_pose_keypoints_2d[i][1])
			allData_hand_right_conf[i].append(hand_right_pose_keypoints_2d[i][2])

	dict_body={}
	dict_face={}
	dict_hand_left={}
	dict_hand_right={}

	dict_body_conf={}
	dict_face_conf={}
	dict_hand_left_conf={}
	dict_hand_right_conf={}
	#combine x,y
	if (normalizeDimensions==False):
		videoWidth=1
	for i in range(25):
		partX=np.array(allData_body[i*2])/videoWidth
		partY=np.array(allData_body[i*2+1])/videoWidth
		partArray=np.stack([partX,partY],axis=0)
		dict_body[body25Mappings[i]]=partArray
		dict_body_conf[body25Mappings[i]]=allData_body_conf[i]

	for i in range(70):
		partX=np.array(allData_face[i*2])/videoWidth
		partY=np.array(allData_face[i*2+1])/videoWidth
		partArray=np.stack([partX,partY],axis=0)
		dict_face[faceMappings[i]]=partArray
		dict_face_conf[faceMappings[i]]=allData_face_conf[i]

	for i in range(21):
		partX=np.array(allData_hand_left[i*2])/videoWidth
		partY=np.array(allData_hand_left[i*2+1])/videoWidth
		partArray=np.stack([partX,partY],axis=0)
		dict_hand_left[hand_mappings[i]]=partArray
		dict_hand_left_conf[hand_mappings[i]]=allData_hand_left_conf[i]

	for i in range(21):
		partX=np.array(allData_hand_right[i*2])/videoWidth
		partY=np.array(allData_hand_right[i*2+1])/videoWidth
		partArray=np.stack([partX,partY],axis=0)
		dict_hand_right[hand_mappings[i]]=partArray
		dict_hand_right_conf[hand_mappings[i]]=allData_hand_right_conf[i]

	outputDict={}
	outputDict["body"]=dict_body
	outputDict["body_confidence"]=dict_body_conf
	outputDict["face"]=dict_face
	outputDict["face_confidence"]=dict_face_conf
	outputDict["hand_left"]=dict_hand_left
	outputDict["hand_left_confidence"]=dict_hand_left_conf
	outputDict["hand_right"]=dict_hand_right
	outputDict["hand_right_confidence"]=dict_hand_right_conf
	outputDict["frame_time"]=allData_frame_time
	return outputDict

#given an array of positions, returns a new array containing the deltas (offset from one frame to the next)
def getDeltaFromPositions(inputArray):
	outputArray=inputArray+0

	arrayLength=outputArray.shape[1]

	for i in range(arrayLength-1):
		outputArray[:,arrayLength-1-i]=outputArray[:,arrayLength-1-i]-outputArray[:,arrayLength-2-i]

	outputArray[:,0]=0
	return outputArray

#Computes the exponential Moving Average on an array of shape [numberOfFeatures,lengthOfTimeSteps] along axis 1
#(so in practise just give it the position arrays for example and it will calculate the ema over the time dimension)
#the parameter beta needs to be between 0 and 1. 1 just returns the input array as it is. When beta is close to one the moving average is very strict
#(it only includes the latest values). When beta is close to 0 the average is very loose (it includes many values).
def exponentialMovingAverage(inputArray,beta=0.9):
	outputArray=inputArray+0

	arrayLength=outputArray.shape[1]

	for i in range(1,arrayLength):
		outputArray[:,i]=outputArray[:,i]*beta+outputArray[:,i-1]*(1-beta)

	return outputArray

#given an array of shape [lengthOfTimeSteps,2] (positions for example) creates a heatmap
#rows and columns specify the number of zones, the default values are decent for 1080p video.
#inputRangeX and inputRangeY specify the range of the input coordinates.
#if normalizeOutput=True the heatmap will contain values 0-1 (1 being the most active zone). Otherwise it will contain the number of points that fall in each zone.
def generateHeatmap(inputArray,rows=18,columns=32,inputRangeX=1920,inputRangeY=1080,normalizeOutput=True,gamma=0.5):
	heatmap=np.zeros((columns,rows))

	arrayLength=inputArray.shape[0]

	for i in range(0,arrayLength):
		coordx=round((inputArray[i,0]/inputRangeX)*(columns-1))
		coordy=round((inputArray[i,1]/inputRangeY)*(rows-1))
		heatmap[coordx,coordy]+=1

	if(normalizeOutput==True):
		heatmap/=heatmap.max()
		if(gamma is not None):
			heatmap=heatmap**gamma
			heatmap/=heatmap.max()
	return heatmap

#takes as input a numpy array "inputArr" of shape (2,n) containing 2d vectors and returns an array of shape (n) containing their lengths:
def calculate_vector_lengths(inputArr):
    return np.sqrt(np.sum(np.square(inputArr), axis=0))

#takes as input three arrays of shape (2,n) contain 2d positions, and returns the angle between points1-pivotPoints and points2-pivotPoints.
#for example points1 might be wrist, points2 shoulder, and pivotPoints elbow (because thats the body part that connects them)
#Returns the angle in degrees by default or radians if ReturnDegrees=False
#output ranges between 0-180 (assuming in degrees) and does not take into account whether the smallest angle between the two is clockwise or counterclockwise. Is you care about that see the function "calculate_signed_angle" bellow
def calculate_angle(points1, points2, pivotPoints,ReturnDegrees=True):
	vec1 = points1 - pivotPoints
	vec2 = points2 - pivotPoints
	dot_product = np.sum(vec1 * vec2, axis=0)
	norm_product = np.linalg.norm(vec1, axis=0) * np.linalg.norm(vec2, axis=0)
	cosine_angles = dot_product / norm_product

	angle_in_radians = np.arccos(cosine_angles)
	if(ReturnDegrees):
		return np.degrees(angle_in_radians)
	else:
		return angle_in_radians

#takes as input three arrays of shape (n,2) contain 2d positions, and returns the angle between points1-pivotPoints and points2-pivotPoints.
#for example points1 might be wrist, points2 shoulder, and pivotPoints elbow (because thats the body part that connects them)
#Returns the angle in degrees by default or radians if ReturnDegrees=False
#output ranges between -180 and 180 (assuming in degrees). (sign of the angle indicates whether or not the shortest angle from one to the other is clockwise or counterclockwise)
def calculate_signed_angle(points1, points2, pivotPoints,ReturnDegrees=True):
	vec1 = points1 - pivotPoints
	vec2 = points2 - pivotPoints
	dot_product = np.sum(vec1 * vec2, axis=1)
	norm_product = np.linalg.norm(vec1, axis=1) * np.linalg.norm(vec2, axis=1)
	cosine_angles = dot_product / norm_product
	angle_in_radians = np.arccos(cosine_angles)
	cross_product = np.cross(vec1, vec2)
	cross_product_sign = np.sign(cross_product)

	if(ReturnDegrees):
		return np.degrees(angle_in_radians) * cross_product_sign
	else:
		return angle_in_radians * cross_product_sign

#given an array "inputArr" of shape (numberOfFeatures,n) and a winfow size "winSize", returns an array of shape (numberOfFeatures,n) containing the moving average (calculated independantly for every feature). The start and end of the array automatically make the window smaller to take into account boundaries.
def moving_average(inputArr, winSize=5):
	numOfFeatures,n = inputArr.shape
	outputArr = np.zeros_like(inputArr)
	halfWinSize1 = winSize // 2
	if(winSize%2==1):
		halfWinSize2 = (winSize // 2) +1
	else:
		halfWinSize2 = winSize // 2
	for i in range(numOfFeatures):
		for j in range(n):
			start = max(0, j - halfWinSize1)
			end = min(n, j + halfWinSize2)
			outputArr[i,j] = np.mean(inputArr[i,start:end])
	return outputArr

#given a numpy array of shape (width,height) will return a pillow image of with the given dimensions. The color at each pixel will be a mix of color 1 and 2 depending on the input array. (wherever the input array is 1, the output array will be color2). The resulting image will be bilinearly upscale to your given resolution. The colors are either 3-item tuples containing RGB or 4-item tuples containing RGBA (transparency)
def create_image_from_grayscale_array(inputArr, outputWidth, outputHeight, color1=(0, 0, 0, 255), color2=(255, 0, 0, 255)):
	assert inputArr.ndim == 2, "Input array must be 2-dimensional"
	assert isinstance(outputWidth, int) and isinstance(outputHeight, int), "Output dimensions must be integers"

	# Determine the size of the input array
	numOfColmn, numOfRows = inputArr.shape

	# Compute a linear interpolation between the two colors based on the input array
	numChannels = len(color1)
	assert numChannels == len(color2), "Color1 and color2 must have the same number of channels"
	colorArr = np.zeros((numOfColmn, numOfRows, numChannels), dtype=np.uint8)
	for i in range(numChannels):
		colorArr[..., i] = (1 - inputArr) * color1[i] + inputArr * color2[i]

	# Create an image from the color array
	inputImage = Image.fromarray(colorArr)

	# Scale the image to the output dimensions using bilinear interpolation
	outputImage = inputImage.resize((outputWidth, outputHeight), resample=Image.BILINEAR)

	return outputImage



#Loads an audio file
#returns (audioData,sampling_rate)
def LoadAudio(pathToAudio):
	y, sr = librosa.load(pathToAudio)
	return y,sr

#Returns a spectrogram of the song in decibels, and a list of the frequencies in the spectrogram
def GenSpectrogram(audioData,sampling_rate,n_fft = 2048,hop_length = 512):
	spec = np.abs(librosa.core.stft(audioData, n_fft=n_fft, hop_length=hop_length))
	specDB=librosa.amplitude_to_db(spec,ref=np.max)
	frequencies = librosa.core.fft_frequencies(sr=sampling_rate,n_fft=n_fft)
	return specDB,frequencies

#Given a frequency index, and a list of times, returns a frequency band from a spectrogram
def GetFrequencyBandAtTimes(spectrogram,targetFrequency,frame_time,hop_length=512):
	indexes=librosa.time_to_frames(frame_time)
	return spectrogram[targetFrequency,indexes]

#Gets the index of the frequency in "frequencyList" that is closest to "targetFrequency"
def GetClosestFrequencyIndex(targetFrequency,frequencyList):
	bestIndex=0
	bestDist=1000000000
	for i in range(len(frequencyList)):
		if(abs(frequencyList[i]-targetFrequency)<bestDist):
			bestDist=abs(frequencyList[i]-targetFrequency)
			bestIndex=i
	return bestIndex




#Tries to figure out what frequencies are best to look at when trying to predict interpeters movements
def SearchBestFrequencies(potentialFrequencies,data,spectrogram,frequencyList,numberOfRuns=2):
	currentFrequencies=potentialFrequencies

	joinAngle=np.expand_dims(calculate_angle(data["body"]["LShoulder"],data["body"]["LWrist"],data["body"]["LElbow"],ReturnDegrees=True),axis=0)
	joinAngle[np.isnan(joinAngle)]=0	#remove NaN
	joinAngleDelta=getDeltaFromPositions(joinAngle)


	removedFrequencies=[]

	while(len(currentFrequencies)>1):
		highestScore=-1000
		bestIndex=0
		for indexToRemove in range(len(currentFrequencies)):


			capturedFrequencies=[]
			for i in range(len(currentFrequencies)):
				if(i==indexToRemove):
					continue
				frequencyIndex=GetClosestFrequencyIndex(currentFrequencies[i],frequencyList)
				frequencyBand=GetFrequencyBandAtTimes(spectrogram=spectrogram,targetFrequency=frequencyIndex,frame_time=data["frame_time"])
				capturedFrequencies.append(frequencyBand)
			capturedFrequencies=np.stack(capturedFrequencies,axis=0)

			capturedFrequencies=getDeltaFromPositions(capturedFrequencies)
			mov_avg=exponentialMovingAverage(capturedFrequencies)
			capturedFrequencies=np.concatenate((capturedFrequencies,mov_avg))
			capturedFrequencies=np.swapaxes(capturedFrequencies,0,1)

			currentScore=0
			for runId in range(numberOfRuns):
				clf = make_pipeline(StandardScaler(), svm.SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1))
				reg=clf.fit(capturedFrequencies,joinAngleDelta[0])
				currentScore+=reg.score(capturedFrequencies,joinAngleDelta[0])
			currentScore/=numberOfRuns
			if(currentScore>highestScore):
				bestIndex=indexToRemove
				highestScore=currentScore
		print(f"Removing {currentFrequencies[bestIndex]}...")
		removedFrequencies.append(currentFrequencies[bestIndex])
		currentFrequencies.pop(bestIndex)
	removedFrequencies.append(currentFrequencies[0])
	removedFrequencies.reverse()
	print("Best Frequencies")
	for i in range(len(removedFrequencies)):
		print(f"{i}:\t{removedFrequencies[i]}")


# takes the processed video data and converts it into a format appropriate for animation
def getAnimation(videoData):

    bodyAnimation = []
    for x in body25Mappings.values():
        i = 0
        flip = videoData["body"][x]
        flipped = np.transpose(flip)
        for y in (flipped):
            z = np.append(y, i)
            z[1] = 1080 - z[1]
            i = i + 1
            bodyAnimation.append(z)

    faceAnimation = []
    for x in faceMappings.values():
        i = 0
        flip = videoData["face"][x]
        flipped = np.transpose(flip)
        for y in (flipped):
            z = np.append(y, i)
            z[1] = 1080 - z[1]
            i = i + 1
            faceAnimation.append(z)

    handLeftAnimation = []
    for x in hand_mappings.values():
        i = 0
        flip = videoData["hand_left"][x]
        flipped = np.transpose(flip)
        for y in (flipped):
            z = np.append(y, i)
            z[1] = 1080 - z[1]
            i = i + 1
            handLeftAnimation.append(z)

    handRightAnimation = []
    for x in hand_mappings.values():
        i = 0
        flip = videoData["hand_right"][x]
        flipped = np.transpose(flip)
        for y in (flipped):
            z = np.append(y, i)
            z[1] = 1080 - z[1]
            i = i + 1
            handRightAnimation.append(z)

    outputDict = {}
    outputDict["body"] = bodyAnimation
    outputDict["face"] = faceAnimation
    outputDict["hand_left"] = handLeftAnimation
    outputDict["hand_right"] = handRightAnimation

    return outputDict









#===========================================Neural networks Start=======
#Note:
#Because of the limited data, neural networks were effectivly unusable. As more data becomes available this code
#Will serve as a reference to how you would train a model.


#Example network. When more data is available, increase width and depth
class Predictor_v1(nn.Module):
	def __init__(self,num_of_inputs,num_of_outputs):
		super().__init__()


		self.dense1=torch.nn.Linear(num_of_inputs,10)
		self.bn1=nn.BatchNorm1d(10)
		self.dense2=torch.nn.Linear(10,5)
		self.bn2=nn.BatchNorm1d(5)
		self.dense3=torch.nn.Linear(5,num_of_outputs)
		#self.activation=torch.nn.SiLU()
		self.activation=torch.nn.Sigmoid()

	def forward(self,x):

		x=self.dense1(x)
		x=self.bn1(x)
		x=self.activation(x)
		x=self.dense2(x)
		x=self.bn2(x)
		x=self.activation(x)
		x=self.dense3(x)

		return x

#Dataset class
class customDataset(torch.utils.data.Dataset):
	def __init__(self, dataX,dataY):
		self.dataX = dataX
		self.dataY = dataY

	def __len__(self):
		return self.dataX.shape[1]

	def __getitem__(self, index):
		a=self.dataX[:,index]
		b=self.dataY[:,index]
		return torch.Tensor(a),torch.Tensor(b)

#Trains a neural network on some given data
def trainModel(model,optimizer,dataLoader,device,epochs=300):
	for t in range(epochs):
		print(f"epoch {t}")
		counter=0
		totalLossTrain=0
		totalLossTest=0
		for batch, (x,y) in enumerate(dataLoader):
			currentBatchSize=int(x.size(0)/2)
			x=x.to(device)
			xTrain=x[:currentBatchSize]
			xTest=x[currentBatchSize:]

			y=y.to(device)
			yTrain=y[:currentBatchSize]
			yTest=y[currentBatchSize:]
			prediction=model.forward(xTrain)


			loss=torch.mean(abs(prediction-yTrain))


			# Backpropagation
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			#To calculate test loss
			with torch.no_grad():
				loss_test=torch.mean(abs(model.forward(xTest)-yTest))
			totalLossTrain+=loss.item()
			totalLossTest+=loss_test.item()

			counter+=1
		print(f"train loss: {totalLossTrain/counter}")
		print(f"test loss: {totalLossTest/counter}")


#Example function for what training on more data might look like
#Point it to a folder with data like:
#mycoolSong.json
#mycoolSong.mp3
#here_isanother_song.json
#here_isanother_song.mp3
def TrainMultiple(pathToData):
	#select some joint angles to predict
	anglesToPredict=[("LShoulder","LElbow","LWrist"),("RShoulder","RElbow","RWrist")]
	#select some body part movements to predict
	bodyPartsToPredict=["Neck"]
	#select some frequencies as input (in hz)
	#The closest available frequencies in the fft will be used.
	targetFrequencies=[10,30,80,120,200,300,400,500,600]


	files= [f for f in os.listdir(pathToData) if os.path.isfile(os.path.join(pathToData,f))]
	DataFiles=[]
	for i in range(len(files)):
		if(files[i].endswith(".json")):
			if(os.path.isfile(pathToData+files[i][:-5]+".mp3")):
				DataFiles.append((files[i],pathToData+files[i][:-5]+".mp3"))

	print(f"Loaded {len(DataFiles)} files")
	for i in range(len(DataFiles)):
		print(f"Found data pair: {DataFiles[i]}")

	capturedMovements_all=[]
	capturedFrequencies_all=[]
	#Load the data from the differnt files
	for i in range(len(DataFiles)):
		#Load the video data
		data=ConvertData(DataFiles[i][0],"",videoWidth=1920,videoHeight=1080)

		#Load the audio data
		audioData, sampling_rate = LoadAudio(DataFiles[i][1])
		spectrogram,frequencyList=GenSpectrogram(audioData,sampling_rate)


		#Capture movements
		capturedMovements=[]
		#angles
		for ii in range(len(anglesToPredict)):
			joinAngle=np.expand_dims(calculate_angle(
				data["body"][anglesToPredict[ii][0]],
				data["body"][anglesToPredict[ii][2]],
				data["body"][anglesToPredict[ii][1]],
				ReturnDegrees=True),axis=0)
			joinAngle[np.isnan(joinAngle)]=0	#remove NaN
			joinAngleDelta=getDeltaFromPositions(joinAngle)
			capturedMovements.append(joinAngleDelta)
		#offsets
		for ii in range(len(bodyPartsToPredict)):
			capturedMovements.append(getDeltaFromPositions(data["body"][bodyPartsToPredict[ii]]))
		capturedMovements=np.concatenate(capturedMovements,axis=0)
		capturedMovements_all.append(capturedMovements)

		#Capture frequencies
		capturedFrequencies=[]
		for ii in range(len(targetFrequencies)):
			frequencyIndex=GetClosestFrequencyIndex(targetFrequencies[ii],frequencyList)
			frequencyBand=GetFrequencyBandAtTimes(spectrogram=spectrogram,targetFrequency=frequencyIndex,frame_time=data["frame_time"])
			capturedFrequencies.append(frequencyBand)
		capturedFrequencies=np.stack(capturedFrequencies,axis=0)

		#from each frequency include its current delta and the exponential Moving Average of its delta
		capturedFrequencies=getDeltaFromPositions(capturedFrequencies)
		mov_avg=exponentialMovingAverage(capturedFrequencies)
		capturedFrequencies=np.concatenate((capturedFrequencies,mov_avg))
		capturedFrequencies_all.append(capturedFrequencies)

	#Combine all data from different files
	capturedMovements_all=np.concatenate(capturedMovements_all,axis=1)
	capturedFrequencies_all=np.concatenate(capturedFrequencies_all,axis=1)

	inputFeatures=capturedFrequencies_all.shape[0]
	outputFeatures=capturedMovements_all.shape[0]

	print(f"Found {inputFeatures} input features")
	print(f"Found {outputFeatures} output features")

	#Select gpu if available
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	#Create model and optimizer
	model=Predictor_v1(inputFeatures,outputFeatures).to(device)
	optimizer=torch.optim.Adam(model.parameters())
	#Create dataset
	dataset=customDataset(capturedFrequencies_all,capturedMovements_all)
	dataloader=DataLoader(dataset,batch_size=64,num_workers=4,pin_memory=True)
	#Begin training
	print("Starting training on: "+str(device))
	trainModel(model,optimizer,dataloader,device,epochs=3000)

	#Note this doesnt save the model, since in practise you will have to adapt it to your future code. See this as future reference:
	#https://pytorch.org/tutorials/beginner/saving_loading_models.html
#===========================================Neural networks End=======




