# Gesture Volume Control

Control your system volume using hand gestures in real-time — no keyboard, no mouse.

## Demo
- 🤏 Pinch (thumb + index finger) to set volume level
- 🤙 Fold pinky down to activate volume control
- 📊 Volume percentage displayed live on screen

## How It Works
Uses MediaPipe Hand Landmarker to detect hand landmarks in real-time.
Distance between thumb tip and index finger tip is mapped to system volume (0-100%).
Pinky-down gesture acts as activation toggle to prevent accidental volume changes.

## Tech Stack
- Python
- OpenCV
- MediaPipe Tasks API 
- pycaw (Windows Core Audio API)
- NumPy

## Setup

### Install dependencies
```pip install opencv-python mediapipe pycaw numpy```

### Run
python main.py

## Notes
- Windows only (pycaw is Windows specific)
- Built using latest MediaPipe Tasks API — not the legacy solutions API
- Landmark reference: thumb tip = 4, index tip = 8, pinky tip = 20
