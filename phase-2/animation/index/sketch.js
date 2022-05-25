// Examples use USGS Earthquake API:
//   https://earthquake.usgs.gov/fdsnws/event/1/#methods
let earthquakes;
function preload() {
  // Get the most recent earthquake in the database
  let url = "Apparat_Goodbye_P1.json";
  data = loadJSON(url, "jsonp", dataLoaded, errorMessage);
}

function setup() {
  noLoop();
}

function draw() {
  background(200);
}

function errorMessage(){
  print("ERROR Data not loaded")
}

function dataLoaded(){
  print("Data Loaded")
}