/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */
'use strict';

var audioid=[];
var videoid=[];
var videoname=[];
var constraints0,constraints1;
var stream1,stream2;
var recid;

function getdevice()
{
  navigator.mediaDevices.enumerateDevices()
  .then(function(devices) {
    devices.forEach(function(device) {
      if(device.kind=='videoinput' && device.label.substr(-11,1)=="(")
      {
        videoname.push(device.label.substr(-11,11));
        videoid.push(device.deviceId);
      }
      console.log(device.kind + ": " + device.label + " id = " + device.deviceId);
    });

    devices.forEach(function(device) {
      if(device.kind=='audioinput')
      {
        for(var i=0;i<videoname.length;i++)
        {
          if(videoname[i]==device.label.substr(-11,11))
          audioid[i]=device.deviceId;
        }
      }
      //console.log(device.kind + ": " + device.label + " id = " + device.deviceId);
    });
  })
  .catch(function(err) {
    console.log(err.name + ": " + err.message);
  });
}

function handleSuccess0(stream1) {  
  const videoTracks = stream1.getVideoTracks();
  console.log('Got stream with constraints:', constraints0);
  console.log(`Using video device: ${videoTracks[0].label}`); //憭鯱ebcam �虾�賭耨�㺿��
  window.stream = stream1; // make variable available to browser console
  $('#mycamera1')[0].srcObject = stream1;
}

function handleSuccess1(stream2) {  
  const videoTracks = stream2.getVideoTracks();
  console.log('Got stream with constraints:', constraints1);
  console.log(`Using video device: ${videoTracks[0].label}`); //憭鯱ebcam �虾�賭耨�㺿��
  window.stream = stream2; // make variable available to browser console
  $('#mycamera2')[0].srcObject = stream2;
}

function handleError(error) {
  if (error.name === 'ConstraintNotSatisfiedError') {
    const v = constraints.video;
    errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
  } else if (error.name === 'PermissionDeniedError') {
    errorMsg('Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

function errorMsg(msg, error) {
  const errorElement = document.querySelector('#errorMsg');
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== 'undefined') {
    console.error(error);
  }
}

async function init0(e) {
  var audioSource =audioid[0];
  var videoSource=videoid[0];
  //video: {deviceId: videoSource ? {exact: videoSource} : undefined}
  //video: {deviceId: videoSource ,width:1280,height:720}
  constraints0 = {
    audio: {deviceId: audioSource},
    video: {deviceId: videoSource ,width:1280,height:720}
  };

  try {
    stream1 = await navigator.mediaDevices.getUserMedia(constraints0);
    handleSuccess0(stream1);
    e.target.disabled = true;
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    handleError(e);
  }
}

async function init1(e) {
  var videoSource=videoid[1];
  constraints1 = {
    audio: false,
    video: {deviceId: videoSource ,width:1280,height:720}
  };

  try {
    stream2 = await navigator.mediaDevices.getUserMedia(constraints1);
    handleSuccess1(stream2);
    e.target.disabled = true;
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    handleError(e);
  }
}

let mediaRecorder;
let recordedBlobs;

function handleDataAvailable(event) {
  console.log('handleDataAvailable', event);
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}


/*function takeimg(camid)  {
  recid=camid;
  recordedBlobs = [];
  //'video/webm;codecs=vp9,opus' 'video/webm;codecs=vp8,opus' 'video/webm;codecs=h264,opus' 'video/mp4;codecs=h264,aac'
  const mimeType = 'image/png';
  const options = {mimeType};
  if(camid==0)
    window.stream=stream1;
  else if(camid==1)
    window.stream= $('#vtoc1')[0].captureStream(30);
  alert(recordedBlobs)
}*/



function startRecording(camid) {
  recid=camid;
  recordedBlobs = [];
  //'video/webm;codecs=vp9,opus' 'video/webm;codecs=vp8,opus' 'video/webm;codecs=h264,opus' 'video/mp4;codecs=h264,aac'
  const mimeType = 'video/webm;codecs=vp9,opus';
  const options = {mimeType};
  if(camid==0)
    window.stream=stream1;
  else if(camid==1)
    window.stream=stream2;
  else if(camid==2)
    window.stream= $('#vtoc1')[0].captureStream(30);

  if(camid!=2)
  {
    try {
      mediaRecorder = new MediaRecorder(window.stream, options);
    } catch (e) {
      console.error('Exception while creating MediaRecorder:', e);
      return;
    }
  }
  else
  {
    try {
      window.stream.addTrack(stream1.getAudioTracks()[0]);
      mediaRecorder = new MediaRecorder(window.stream, options);
    } catch (e) {
      console.error('Exception while creating MediaRecorder:', e);
      return;
    }
  }

  console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
 
  mediaRecorder.onstop = (event) => {
    console.log('Recorder stopped: ', event);
    console.log('Recorded Blobs: ', recordedBlobs);
  };
  mediaRecorder.ondataavailable = handleDataAvailable;
  mediaRecorder.start();
  console.log('MediaRecorder started', mediaRecorder);
}

function stopRecording() {
  mediaRecorder.stop();  
  stream1.getTracks().forEach(function(track) {
    track.stop();
  });
  stream2.getTracks().forEach(function(track) {
    track.stop();
  });
}

function playrecdata(){
  const mimeType = 'video/webm';
  const superBuffer = new Blob(recordedBlobs, {type: mimeType});
  if(recid==0)
  {
    $('#recplay1')[0].src = null;
    $('#recplay1')[0].srcObject = null;
    $('#recplay1')[0].src = window.URL.createObjectURL(superBuffer);
    $('#recplay1')[0].controls = true;
    $('#recplay1')[0].play();
  }
  else
  {
    $('#recplay2')[0].src = null;
    $('#recplay2')[0].srcObject = null;
    $('#recplay2')[0].src = window.URL.createObjectURL(superBuffer);
    $('#recplay2')[0].controls = true;
    $('#recplay2')[0].play();
  }
}

function downloadblob(){
  const blob = new Blob(recordedBlobs, {type: 'video/webm'});
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = 'recdata.png';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 100);
}

function uploadblob(camid) {
  var fd = new FormData();
  fd.append('fname', $("#picurl").val());
  // alert($("#str").val());
  const webmblob = new Blob(recordedBlobs, { type: 'image/png' });
  //fd.append('bdata', webmblob);

  fd.append('bdata',$('#bdata'));
  alert(webmblob);

  $('#inflist').append("<li style='color:red;'>轉檔中請稍後</li>");
  $.ajax({
    type: 'POST',
    url: './prg/upload.php',
    data: fd,
    processData: false,
    contentType: false
  }).done(function (data) {
    console.log(data);
    $('#inflist').append("<li style='color:green;'>轉檔成功</li>");
  });
}