
import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Model location
MODEL_PATH = "models/hand_landmarker.task"

# Hand connections: 21 landmarks
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

# Initialize hand landmarker
base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Create detector
detector = vision.HandLandmarker.create_from_options(options)

# Start webcam
cap = cv2.VideoCapture(0)

print("PyroTouch hand tracking started!")
print("Press Q to exit.")

try:
    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Camera frame unavailable")
            break

        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Video timestamp in milliseconds
        timestamp_ms = time.perf_counter_ns() // 1_000_000

        # Detect hand
        results = detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        height, width, _ = frame.shape

        if results.hand_landmarks:

            for hand in results.hand_landmarks:

                points = []

                # Convert normalized coordinates to pixels
                for landmark in hand:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    points.append((x, y))

                # Draw connections
                for start, end in HAND_CONNECTIONS:
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (0, 255, 0),
                        2
                    )

                # Draw all 21 landmarks
                for x, y in points:
                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 0, 255),
                        -1
                    )

                # Index fingertip = landmark 8
                index_x, index_y = points[8]

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    12,
                    (255, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "INDEX FINGER",
                    (index_x + 15, index_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 255),
                    2
                )

                print(
                    f"Index fingertip: X={index_x}, Y={index_y}"
                )

        cv2.imshow("PyroTouch - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    detector.close()
    cv2.destroyAllWindows()

print("Hand tracking stopped!")
