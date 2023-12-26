import { takepicture, clearphoto } from './webcam.js';

let width = 320;
let height = 0;

let streaming = false;

let video = null;
let canvas = null;
let photo = null;
let startbutton = null;

(function() {
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  photo = document.getElementById('photo');
  startbutton = document.getElementById('startbutton');

  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(function(stream) {
    video.srcObject = stream;
    video.play();
  })
  .catch(function(err) {
    console.log("An error occurred: " + err);
  });

  video.addEventListener('canplay', function(ev){
    if (!streaming) {
      height = video.videoHeight / (video.videoWidth/width);
    
      // Firefox currently has a bug where the height can't be read from
      // the video, so we will make assumptions if this happens.
    
      if (isNaN(height)) {
        height = width / (4/3);
      }
    
      video.setAttribute('width', width);
      video.setAttribute('height', height);
      canvas.setAttribute('width', width);
      canvas.setAttribute('height', height);
      streaming = true;
    }
  }, false);

  startbutton.addEventListener('click', async function(ev){
    let imageData = await takepicture(video, width, height);

    const formData = new FormData();
    formData.append('image', imageData, 'image.png');
    
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      console.log('Image uploaded:', data);
    }
    catch(error)
    {
      console.error('Error uploading image:', error);
    }
    ev.preventDefault();
  }, false);
  
  clearphoto();
})();


