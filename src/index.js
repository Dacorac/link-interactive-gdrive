import { takepicture, clearphoto } from './webcam.js';

let width = 320;
let height = 0;
let streaming = false;
let video = null;
let canvas = null;
let photo = null;
let startbutton = null;

function initialize() {
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  photo = document.getElementById('photo');
  startbutton = document.getElementById('startbutton');

  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function (stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function (err) {
      console.log("An error occurred: " + err);
    });

  video.addEventListener('canplay', function (ev) {
    if (!streaming) {
      height = video.videoHeight / (video.videoWidth / width);

      if (isNaN(height)) {
        height = width / (4 / 3);
      }

      video.setAttribute('width', width);
      video.setAttribute('height', height);
      canvas.setAttribute('width', width);
      canvas.setAttribute('height', height);
      streaming = true;
    }
  }, false);

  startbutton.addEventListener('click', startStreaming, false);

  clearphoto();
}

function startStreaming() {
  takepicture(video, width, height)
    .then(function (imageData) {
      const formData = new FormData();
      formData.append('image', imageData, 'image.png');

      fetch('/upload', {
        method: 'POST',
        body: formData
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          console.log('Image uploaded:', data);
        })
        .catch(function (error) {
          console.error('Error uploading image:', error);
        });
    })
    .catch(function (error) {
      console.error('Error taking picture:', error);
    });
}

initialize();