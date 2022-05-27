
const scaleSize = 0.3
var frame_i = 0;
let mySound;
let dataPath = "../analysis/motion/data/Apparat_Goodbye_P1_features.json";
let title = "P1 Apparat - Goodbye";
let soundPath = "../media/audio/Apparat_Goodbye.mp3"
var animationWidth;
var animationHeight;

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
  print(data_in.frameRate)

  frameRate(data_in.frameRate)
  frame_i = 0; 
}

function draw() {
  //background(0);
  fill(0);
  noStroke();
  rect(0, 0, animationWidth, animationHeight);

  fill(200)
  text(title + "  " + str(data_in.data[frame_i].raw.time), 10, 20, width, 200)

  if(frame_i < data_in.data.length){

    
    
    if(frame_i==0) mySound.play()

    body_keypoints = data_in.data[frame_i].raw.pose_keypoints_2d
    handLeft_keypoints = data_in.data[frame_i].raw.hand_left_keypoints_2d
    handRight_keypoints = data_in.data[frame_i].raw.hand_right_keypoints_2d
    face_keypoints = data_in.data[frame_i].raw.face_keypoints_2d
    
    

    drawBody(body_keypoints, true, true)
    drawHand(handLeft_keypoints, true, true)
    drawHand(handRight_keypoints, true, true)
    drawFace(face_keypoints, true, true)

    drawFod(frame_i);
  }
  frame_i++;
}

function drawBody(keypoints, lines, ellipses){

  drawSkelethon(keypoints[0], keypoints[1], 1, lines, ellipses)
  drawSkelethon(keypoints[1], keypoints[2], 2, lines, ellipses)
  drawSkelethon(keypoints[2], keypoints[3], 3, lines, ellipses)
  drawSkelethon(keypoints[3], keypoints[4], 4, lines, ellipses)
  drawSkelethon(keypoints[1], keypoints[5], 5, lines, ellipses)
  drawSkelethon(keypoints[5], keypoints[6], 6, lines, ellipses)
  drawSkelethon(keypoints[6], keypoints[7], 7, lines, ellipses)
  drawSkelethon(keypoints[1], keypoints[8], 8, lines, ellipses)
  drawSkelethon(keypoints[8], keypoints[9], 9, lines, ellipses)
  drawSkelethon(keypoints[9], keypoints[10], 10, lines, ellipses)
  drawSkelethon(keypoints[10], keypoints[11], 11, lines, ellipses)
  drawSkelethon(keypoints[8], keypoints[12], 12, lines, ellipses)
  drawSkelethon(keypoints[12], keypoints[13], 13, lines, ellipses)
  drawSkelethon(keypoints[13], keypoints[14], 14, lines, ellipses)
  drawSkelethon(keypoints[0], keypoints[15], 15, lines, ellipses)
  drawSkelethon(keypoints[0], keypoints[16], 16, lines, ellipses)
  drawSkelethon(keypoints[15], keypoints[17], 16, lines, ellipses)
  drawSkelethon(keypoints[16], keypoints[18], 18, lines, ellipses)
  drawSkelethon(keypoints[14], keypoints[19], 19, lines, ellipses)
  drawSkelethon(keypoints[19], keypoints[20], 20, lines, ellipses)
  drawSkelethon(keypoints[14], keypoints[21], 21, lines, ellipses)
  drawSkelethon(keypoints[11], keypoints[22], 22, lines, ellipses)
  drawSkelethon(keypoints[22], keypoints[23], 23, lines, ellipses)
  drawSkelethon(keypoints[11], keypoints[24], 19, lines, ellipses)
}

function drawHand(keypoints, lines, ellipses){

  drawSkelethon(keypoints[0], keypoints[1], 0, lines, ellipses)
  drawSkelethon(keypoints[1], keypoints[2], 0, lines, ellipses)
  drawSkelethon(keypoints[2], keypoints[3], 0, lines, ellipses)
  drawSkelethon(keypoints[3], keypoints[4], 0, lines, ellipses)
  
  drawSkelethon(keypoints[0], keypoints[5], 4, lines, ellipses)
  drawSkelethon(keypoints[5], keypoints[6], 4, lines, ellipses)
  drawSkelethon(keypoints[6], keypoints[7], 4, lines, ellipses)
  drawSkelethon(keypoints[7], keypoints[8], 4, lines, ellipses)

  drawSkelethon(keypoints[0], keypoints[9], 7, lines, ellipses)
  drawSkelethon(keypoints[9], keypoints[10], 7, lines, ellipses)
  drawSkelethon(keypoints[10], keypoints[11], 7, lines, ellipses)
  drawSkelethon(keypoints[11], keypoints[12], 7, lines, ellipses)

  drawSkelethon(keypoints[0], keypoints[13], 14, lines, ellipses)
  drawSkelethon(keypoints[13], keypoints[14], 14, lines, ellipses)
  drawSkelethon(keypoints[14], keypoints[15], 14, lines, ellipses)
  drawSkelethon(keypoints[15], keypoints[16], 14, lines, ellipses)

  drawSkelethon(keypoints[0], keypoints[17], 17, lines, ellipses)
  drawSkelethon(keypoints[17], keypoints[18], 16, lines, ellipses)
  drawSkelethon(keypoints[18], keypoints[19], 18, lines, ellipses)
  drawSkelethon(keypoints[19], keypoints[20], 18, lines, ellipses)
}

function drawFace(keypoints, lines, ellipses){
  for (let index = 0; index < 16; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)
  
  for (let index = 17; index < 21; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 22; index < 26; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 27; index < 30; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 31; index < 35; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 36; index < 41; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 42; index < 47; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 48; index < 60; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  for (let index = 60; index < 67; index++)
    drawSkelethon(keypoints[index], keypoints[index+1], 25, lines, ellipses)

  drawSkelethon(keypoints[68], keypoints[68], 25, lines, ellipses)
  drawSkelethon(keypoints[69], keypoints[69], 25, lines, ellipses)
}


function errorMessage(){
  print("ERROR Data not loaded")
}

function dataLoaded(){
  print("Data Loaded")
}


function setColor(j){
  let p5jsColor = color(255, 255, 255);
  switch (j) {
    case 0: // nose
      p5jsColor = color(245, 66, 132);
      break;
    case 1:// neck
      p5jsColor = color(255, 0, 0);
      break;
    case 2:// r_shoulder
      p5jsColor = color(247, 95, 0);
      break;
    case 3:// r_elbow
      p5jsColor = color(247, 193, 0);
      break;
    case 4://r_wrist
      p5jsColor = color(247, 247, 0);
      break;
    case 5:// l_shoulder
      p5jsColor = color(181, 247, 0);
      break;
    case 6:// l_elbow
      p5jsColor = color(103, 247, 0);
    case 7:// l_wrist
      p5jsColor = color(0, 255, 0);
      break;
    case 8:// mid_hip
      p5jsColor = color(247, 45, 0);
      break;
    case 9:// r_hip
      p5jsColor = color(178, 102, 255);
      break;
    case 10:// r_knee
      p5jsColor = color(51, 255, 51);;
      break;
    case 11:// r_ankle
      p5jsColor = color(255, 255, 255);
      break;
    case 12:// l_hip
      p5jsColor = color(102, 178, 255);
      break;
    case 13:// l_knee
      p5jsColor = color(51, 153, 255);
      break;
    case 14:// l_ankle
      p5jsColor = color(51, 51, 255);
      break;
    case 15:// r_eye
      p5jsColor = color(255, 0, 127);
      break;
    case 16:// l_eye
      p5jsColor = color(178, 102, 255);
      break;
    case 17:// r_ear
      p5jsColor = color(255, 0, 255);
      break;
    case 18:// l_ear
      p5jsColor = color(102, 0, 204);
      break;
    case 19:// l_big_toe
      p5jsColor = color(0, 0, 255);
      break;
    case 20:// l_small_toe
      p5jsColor = color(0, 0, 255);
      break;
    case 21:// l_heel
      p5jsColor = color(51, 51, 255);
      break;
    case 22:// r_big_toe
      p5jsColor = color(0, 255, 255);
      break;
    case 23:// r_small_toe
      p5jsColor = color(0, 255, 255);
      break;
    case 24:// r_heel
      p5jsColor = color(0, 255, 255);
      break;
    case 25:
      p5jsColor = color(255, 255, 255, 100);
      break;
    default:
        p5jsColor = color(255, 255, 255);
  }
  return p5jsColor
}

function drawSkelethon(k0, k1, col, lines, ellipses) {

  if(k0[0]>0 && k0[1]>0 && k1[0]>0 && k1[1]>0){

    stroke(setColor(col))
    strokeWeight(4)
    fill(setColor(col))

    if (lines) {
      line( k0[0]*scaleSize, k0[1]*scaleSize, k1[0]*scaleSize, k1[1]*scaleSize )
    }
    if (ellipses) {
      ellipse(k0[0]*scaleSize, k0[1]*scaleSize, 4, 4)
      ellipse(k1[0]*scaleSize, k1[1]*scaleSize, 4, 4)
    }
  }
}



function drawFod(index){
  fod = data_in.data[index].keypoints_fod.distance_total / 100
  let marker = width/data_in.data.length
  let lineIndex = index*marker
  strokeWeight(1);
  stroke(255)
  line(lineIndex, height, lineIndex, height-fod)
}