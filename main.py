import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
from utils import draw_landmarks, get_volume_controller

capture = cv2.VideoCapture(0)

base_options = python.BaseOptions('hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    min_hand_detection_confidence=0.5
)
hands = vision.HandLandmarker.create_from_options(options)
vol = get_volume_controller()

while True:
    isTrue, frame = capture.read()

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(mp.ImageFormat.SRGB, imgRGB)
    timestamp_ms = int(time.time() * 1000)
    results = hands.detect_for_video(mp_image, timestamp_ms)

    annotated_frame = draw_landmarks(imgRGB, results)
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    h, w, _ = frame.shape

    if results.hand_landmarks:
        for hand_landmark in results.hand_landmarks:
            x1, y1 = int(hand_landmark[8].x * w), int(hand_landmark[8].y * h)
            x2, y2 = int(hand_landmark[4].x * w), int(hand_landmark[4].y * h)

            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            volume = np.interp(distance, [20, 200], [0, 100])

            pinky_tip_y = int(hand_landmark[20].y * h)
            pinky_knuckle_y = int(hand_landmark[18].y * h)

            if pinky_tip_y > pinky_knuckle_y:
                vol.SetMasterVolumeLevelScalar(volume / 100, None)

            cv2.putText(annotated_frame, str(int(volume)), (10, h-30),
                       cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0), 2)

    cv2.imshow("Video", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()