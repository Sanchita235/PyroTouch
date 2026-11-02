
import cv2
import numpy as np
import random
import math

WIDTH = 800
HEIGHT = 600

particles = []
mouse_x = WIDTH // 2
mouse_y = HEIGHT // 2


# Track mouse position
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y

    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y


# Particle class
class Particle:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        # Initial velocity
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -2)

        self.life = 100
        self.size = random.randint(4, 9)

    def update(self):

        self.x += self.vx
        self.y += self.vy

        # Random movement
        self.vx += random.uniform(-0.15, 0.15)

        # Upward acceleration
        self.vy -= 0.03

        self.life -= 2
        self.size *= 0.97

    def draw(self, frame):

        if self.life <= 0:
            return

        intensity = int(self.life * 2.55)

        color = (
            0,
            max(0, min(255, intensity // 3)),
            255
        )

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            max(1, int(self.size)),
            color,
            -1
        )


# Create window
cv2.namedWindow("PyroTouch - Particle Engine")

cv2.setMouseCallback(
    "PyroTouch - Particle Engine",
    mouse_callback
)

print("Particle engine started!")
print("Move your mouse to create fire.")
print("Press Q to exit.")

running = True

while running:

    frame = np.zeros(
        (HEIGHT, WIDTH, 3),
        dtype=np.uint8
    )

    # Spawn particles
    for _ in range(5):

        particles.append(
            Particle(mouse_x, mouse_y)
        )

    # Update particles
    for particle in particles[:]:

        particle.update()
        particle.draw(frame)

        if particle.life <= 0:
            particles.remove(particle)

    # Display particle count
    cv2.putText(
        frame,
        f"Particles: {len(particles)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "PyroTouch - Particle Engine",
        frame
    )

    if cv2.waitKey(16) & 0xFF == ord('q'):
        running = False

cv2.destroyAllWindows()

print("Particle engine stopped!")
