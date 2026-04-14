
const scaleSize = 1
let frame_i = 0;
let mySound;
let dataPath = "../analysis/motion/data/Apparat_Goodbye_P1_features.json";
let title = "P1 Apparat - Goodbye";
let soundPath = "../media/audio/Apparat_Goodbye.mp3"
let animationWidth;
let animationHeight;
let skelethonDrawing = []
let faceDrawing = []
let leftHandDrawing = []
let rightHandDrawing = []
let trail = false
let trailLength
let playbackrate = 1;

function preload(){
  mySound = loadSound(soundPath);
  data_in = loadJSON(dataPath, dataLoaded, errorMessage);
}

function setup() {
  animationWidth = int(1920*scaleSize)
  animationHeight = int(1280*scaleSize)

  let featuresHeight = 150;
  createCanvas(animationWidth, animationHeight+featuresHeight)
  background(0);
  frameRate(data_in.frameRate)
  frame_i = 0; 

  skelethonBuffer = createGraphics(width/2, height/2);

  prepareKeypoints()
  trailLength = trailLenght(data_in.frameRate, 0.5) // sets the trail lengths in seconds

}

function draw() {
  fill(0);
  noStroke();
  rect(0, 0, animationWidth, animationHeight);

  fill(200)
  
  /*
  if (frame_i>trailLength) {
    trail = true
  }
  */

  
  if(frame_i < data_in.data.length){

    // sincs audio playback rate to visualisation
    if (frame_i<1) mySound.play()
    playbackrate = getFrameRate()/data_in.frameRate
    if (playbackrate < 100) mySound.rate(playbackrate)
  
    textSize(40*scaleSize)
    text(title +  "        FPS: " + str(int(getFrameRate()))  + "        Time: " + str(data_in.data[frame_i].time), 10, 20, width, 200)

    drawFullSkelethon();
    drawFod(frame_i);
  }
  frame_i++;

  if(playbackrate == 0) {
    playbackrate = 1
  }
  else {
    
    
  }
}


/* _.-^-._.-^-._.-^-._.-^-._.-^-._.-^-._.-^-._.-^-._.-^-._.-^-._ */

function drawFullSkelethon(){

  if(trail){
    for (let index_trail = 0; index_trail < trailLength; index_trail++) {
      for (let key_i = 0; key_i < skelethonDrawing[frame_i].length; key_i++) {
        skelethonDrawing[frame_i-index_trail][key_i].show(1/index_trail)
      }
    }
    /*
    for (let index_trail = 0; index_trail < trailLength; index_trail++) {
      for (let key_i = 0; key_i < leftHandDrawing[frame_i].length; key_i++) {
        leftHandDrawing[frame_i-index_trail][key_i].show(1/index_trail)
      }
    }

    for (let index_trail = 0; index_trail < trailLength; index_trail++) {
      for (let key_i = 0; key_i < rightHandDrawing[frame_i].length; key_i++) {
        rightHandDrawing[frame_i-index_trail][key_i].show(1/index_trail)
      }
    }
    
    for (let index_trail = 0; index_trail < trailLength; index_trail++) {
      for (let key_i = 0; key_i < faceDrawing[frame_i].length; key_i++) {
        faceDrawing[frame_i-index_trail][key_i].show(1/index_trail)
      }
    }
    */
  }

  for (let key_i = 0; key_i < skelethonDrawing[frame_i].length; key_i++) {
    skelethonDrawing[frame_i][key_i].show(1)
  }

  for (let key_i = 0; key_i < faceDrawing[frame_i].length; key_i++) {
    faceDrawing[frame_i][key_i].show(1)
  }

  for (let key_i = 0; key_i < leftHandDrawing[frame_i].length; key_i++) {
    leftHandDrawing[frame_i][key_i].show(1)
  }

  for (let key_i = 0; key_i < rightHandDrawing[frame_i].length; key_i++) {
    rightHandDrawing[frame_i][key_i].show(1)
  }
}


function prepareKeypoints() {
  for (let frame_i = 0; frame_i < data_in.data.length; frame_i++) {
    body_keypoints = data_in.data[frame_i].raw.pose_keypoints_2d
    handLeft_keypoints = data_in.data[frame_i].raw.hand_left_keypoints_2d
    handRight_keypoints = data_in.data[frame_i].raw.hand_right_keypoints_2d
    face_keypoints = data_in.data[frame_i].raw.face_keypoints_2d

    prepareBody(body_keypoints, true, true)
    prepareFace(face_keypoints, true, true)
    prepareHand(handLeft_keypoints, true, true, leftHandDrawing)
    prepareHand(handRight_keypoints, true, true, rightHandDrawing)
  }
}

function prepareBody(keypoints, lines, ellipses){
  let bodyPoints = []
  
  bodyPoints.push(new drawSkelethon(keypoints[0], keypoints[1], 1, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[1], keypoints[2], 2, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[2], keypoints[3], 3, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[3], keypoints[4], 4, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[1], keypoints[5], 5, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[5], keypoints[6], 6, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[6], keypoints[7], 7, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[1], keypoints[8], 8, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[8], keypoints[9], 9, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[9], keypoints[10], 10, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[10], keypoints[11], 11, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[8], keypoints[12], 12, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[12], keypoints[13], 13, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[13], keypoints[14], 14, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[0], keypoints[15], 15, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[0], keypoints[16], 16, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[15], keypoints[17], 16, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[16], keypoints[18], 18, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[14], keypoints[19], 19, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[19], keypoints[20], 20, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[14], keypoints[21], 21, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[11], keypoints[22], 22, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[22], keypoints[23], 23, 1, lines, ellipses))
  bodyPoints.push(new drawSkelethon(keypoints[11], keypoints[24], 19, 1, lines, ellipses))

  skelethonDrawing.push(bodyPoints)
}

function prepareHand(keypoints, lines, ellipses, handDrawing){
  let handArray = []
  
  handArray.push(new drawSkelethon(keypoints[0], keypoints[1], 0, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[1], keypoints[2], 0, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[2], keypoints[3], 0, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[3], keypoints[4], 0, 1, lines, ellipses))
  
  handArray.push(new drawSkelethon(keypoints[0], keypoints[5], 4, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[5], keypoints[6], 4, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[6], keypoints[7], 4, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[7], keypoints[8], 4, 1, lines, ellipses))

  handArray.push(new drawSkelethon(keypoints[0], keypoints[9], 7, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[9], keypoints[10], 7, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[10], keypoints[11], 7, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[11], keypoints[12], 7, 1, lines, ellipses))

  handArray.push(new drawSkelethon(keypoints[0], keypoints[13], 14, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[13], keypoints[14], 14, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[14], keypoints[15], 14, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[15], keypoints[16], 14, 1, lines, ellipses))

  handArray.push(new drawSkelethon(keypoints[0], keypoints[17], 17, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[17], keypoints[18], 16, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[18], keypoints[19], 18, 1, lines, ellipses))
  handArray.push(new drawSkelethon(keypoints[19], keypoints[20], 18, 1, lines, ellipses))

  handDrawing.push(handArray)
}

function prepareFace(keypoints, lines, ellipses){
  let facePoints = []

  for (let index = 0; index < 16; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))
  
  for (let index = 17; index < 21; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 22; index < 26; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 27; index < 30; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 31; index < 35; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 36; index < 41; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 42; index < 47; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 48; index < 60; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  for (let index = 60; index < 67; index++)
    facePoints.push(new drawSkelethon(keypoints[index], keypoints[index+1], 25, 1, lines, ellipses))

  facePoints.push(new drawSkelethon(keypoints[68], keypoints[68], 25, 1, lines, ellipses))
  facePoints.push(new drawSkelethon(keypoints[69], keypoints[69], 25, 1, lines, ellipses))

  faceDrawing.push(facePoints)
}


function errorMessage(){
  print("ERROR Data not loaded")
}

function dataLoaded(){
  print("Data Loaded")
}


function setColor(j, alpha){
  let p5jsColor = color(255, 255, 255, 255);

  let alphaBody = int(255*alpha);
  let alphaFace = int(100*alpha);

  switch (j) {
    case 0: // nose
      p5jsColor = color(245, 66, 132, alphaBody);
      break;
    case 1:// neck
      p5jsColor = color(255, 0, 0, alphaBody);
      break;
    case 2:// r_shoulder
      p5jsColor = color(247, 95, 0, alphaBody);
      break;
    case 3:// r_elbow
      p5jsColor = color(247, 193, 0, alphaBody);
      break;
    case 4://r_wrist
      p5jsColor = color(247, 247, 0, alphaBody);
      break;
    case 5:// l_shoulder
      p5jsColor = color(181, 247, 0, alphaBody);
      break;
    case 6:// l_elbow
      p5jsColor = color(103, 247, 0, alphaBody);
    case 7:// l_wrist
      p5jsColor = color(0, 255, 0, alphaBody);
      break;
    case 8:// mid_hip
      p5jsColor = color(247, 45, 0, alphaBody);
      break;
    case 9:// r_hip
      p5jsColor = color(178, 102, 255, alphaBody);
      break;
    case 10:// r_knee
      p5jsColor = color(51, 255, 51, alphaBody);;
      break;
    case 11:// r_ankle
      p5jsColor = color(255, 255, 255, alphaBody);
      break;
    case 12:// l_hip
      p5jsColor = color(102, 178, 255, alphaBody);
      break;
    case 13:// l_knee
      p5jsColor = color(51, 153, 255, alphaBody);
      break;
    case 14:// l_ankle
      p5jsColor = color(51, 51, 255, alphaBody);
      break;
    case 15:// r_eye
      p5jsColor = color(255, 0, 127, alphaBody);
      break;
    case 16:// l_eye
      p5jsColor = color(178, 102, 255, alphaBody);
      break;
    case 17:// r_ear
      p5jsColor = color(255, 0, 255, alphaBody);
      break;
    case 18:// l_ear
      p5jsColor = color(102, 0, 204, alphaBody);
      break;
    case 19:// l_big_toe
      p5jsColor = color(0, 0, 255, alphaBody);
      break;
    case 20:// l_small_toe
      p5jsColor = color(0, 0, 255, alphaBody);
      break;
    case 21:// l_heel
      p5jsColor = color(51, 51, 255, alphaBody);
      break;
    case 22:// r_big_toe
      p5jsColor = color(0, 255, 255, alphaBody);
      break;
    case 23:// r_small_toe
      p5jsColor = color(0, 255, 255, alphaBody);
      break;
    case 24:// r_heel
      p5jsColor = color(0, 255, 255, alphaBody);
      break;
    case 25:
      p5jsColor = color(255, 255, 255, alphaFace);
      break;
    default:
        p5jsColor = color(255, 255, 255, alphaBody);
  }
  return p5jsColor
}

class drawSkelethon {
  constructor(k0, k1, col, alpha, lines, ellipses){
    this.k0 = k0;
    this.k1 = k1;
    this.lines = lines;
    this.ellipses = ellipses;
    this.col = col
    this.alpha = alpha
  }
  show(alpha){

    this.alpha = alpha

    if(this.k0[0]>0 && this.k0[1]>0 && this.k1[0]>0 && this.k1[1]>0){
      stroke(setColor(this.col, this.alpha))
      strokeWeight(10*scaleSize)
      fill(setColor(this.col, this.alpha))

      if (this.lines) {
        line(this.k0[0]*scaleSize, this.k0[1]*scaleSize, this.k1[0]*scaleSize, this.k1[1]*scaleSize)
      }
      if (this.ellipses) {
        ellipse(this.k0[0]*scaleSize, this.k0[1]*scaleSize, 10*scaleSize, 10*scaleSize)
        ellipse(this.k1[0]*scaleSize, this.k1[1]*scaleSize, 10*scaleSize, 10*scaleSize)
      }
    }
  }
}

function drawFod(index){

  let marker = width/data_in.data.length
  let lineIndex = index*marker
  strokeWeight(1);

  let fodMax = 0;
  let color_k = 25
  let previousFod = height;

  for (let index_k = 0; index_k < data_in.data[index].keypoints_fod.keypoints.length; index_k++) {
    let fod = data_in.data[index].keypoints_fod.keypoints[index_k].distance*0.02

    stroke(setColor(index_k, 0.2))

    line(lineIndex, previousFod, lineIndex, previousFod-fod)
    previousFod = previousFod-fod;
  }
  
  
}

function trailLenght(frameRate, seconds){
  return frameRate*seconds
}