
import cv2
import mediapipe as mp
import numpy as np
import random
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# =====================================
# 1. CONFIGURATION
# =====================================

WIDTH = 800
HEIGHT = 600

MODEL_PATH = "models/hand_landmarker.task"

particles = []

# Five fingertip landmark IDs
FINGERTIPS = [4, 8, 12, 16, 20]


# =====================================
# 2. PARTICLE CLASS
# =====================================

class Particle:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        # Initial velocity
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -2)

        # Particle properties
        self.life = 100
        self.size = random.randint(4, 9)

    def update(self):

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Random movement
        self.vx += random.uniform(-0.15, 0.15)

        # Upward acceleration
        self.vy -= 0.03

        # Reduce lifetime and size
        self.life -= 2
        self.size *= 0.97

    def draw(self, frame):

        if self.life <= 0:
            return

        intensity = max(
            0,
            min(255, int(self.life * 2.55))
        )

        # BGR color format
        color = (
            0,
            intensity // 3,
            255
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            max(1, int(self.size)),
            color,
            -1
        )


# =====================================
# 3. MEDIAPIPE INITIALIZATION
# =====================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,

    # Detect up to ten hands
    num_hands=10,

    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

detector = vision.HandLandmarker.create_from_options(
    options
)


# =====================================
# 4. CAMERA INITIALIZATION
# =====================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    detector.close()

    raise RuntimeError(
        "Camera could not be opened"
    )

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

print("--------------------------------")
print("       PYROTOUCH ACTIVATED")
print("--------------------------------")
print("Hand detection: ON")
print("Fingertip emitters: 5 per hand")
print("Maximum hands: 10")
print("Press Q to exit.")
print("--------------------------------")


# =====================================
# 5. MAIN LOOP
# =====================================

try:

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Camera frame unavailable")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Resize frame
        frame = cv2.resize(
            frame,
            (WIDTH, HEIGHT)
        )

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp for VIDEO mode
        timestamp_ms = (
            time.perf_counter_ns() // 1_000_000
        )

        # Detect hands
        results = detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # =================================
        # 6. HAND AND FINGERTIP DETECTION
        # =================================

        if results.hand_landmarks:

            # Loop through every detected hand
            for hand_number, hand in enumerate(
                results.hand_landmarks
            ):

                # Extract all five fingertips
                for tip_id in FINGERTIPS:

                    tip = hand[tip_id]

                    # Convert normalized coordinates
                    # into screen pixel coordinates

                    x = int(tip.x * WIDTH)
                    y = int(tip.y * HEIGHT)

                    # Generate particles
                    for _ in range(3):

                        particles.append(
                            Particle(x, y)
                        )

                    # Highlight fingertip
                    cv2.circle(
                        frame,
                        (x, y),
                        8,
                        (255, 0, 255),
                        -1
                    )

                # Display detected hand number
                wrist = hand[0]

                wrist_x = int(wrist.x * WIDTH)
                wrist_y = int(wrist.y * HEIGHT)

                cv2.putText(
                    frame,
                    f"Hand {hand_number + 1}",
                    (wrist_x, wrist_y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        # =================================
        # 7. PARTICLE PHYSICS
        # =================================

        for particle in particles[:]:

            particle.update()

            particle.draw(frame)

            # Remove dead particles
            if particle.life <= 0:

                particles.remove(particle)

        # =================================
        # 8. DISPLAY INFORMATION
        # =================================

        detected_hands = len(
            results.hand_landmarks
        ) if results.hand_landmarks else 0

        cv2.putText(
            frame,
            f"Hands: {detected_hands}/2",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Particles: {len(particles)}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "PYROTOUCH - HAND CONTROLLED FIRE",
            (20, HEIGHT - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # =================================
        # 9. DISPLAY WINDOW
        # =================================

        cv2.imshow(
            "PyroTouch - Hand Controlled Fire",
            frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# =====================================
# 10. CLEANUP
# =====================================

finally:

    cap.release()

    detector.close()

    cv2.destroyAllWindows()

    print("--------------------------------")
    print("       PYROTOUCH STOPPED")
    print("--------------------------------")
