import mediapipe as mp
from mediapipe.tasks.python import vision
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mpHands = vision.HandLandmarksConnections
mpDrawing = vision.drawing_utils
mpDrawingStyles = vision.drawing_styles

def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def draw_landmarks(image_rgb, detection_results):
    hand_landmark_list = detection_results.hand_landmarks
    annotated_image = np.copy(image_rgb)
    for hand_landmark in hand_landmark_list:
        mpDrawing.draw_landmarks(
            annotated_image,
            hand_landmark,
            mpHands.HAND_CONNECTIONS,
            mpDrawingStyles.get_default_hand_landmarks_style(),
            mpDrawingStyles.get_default_hand_connections_style()
        )
    return annotated_image