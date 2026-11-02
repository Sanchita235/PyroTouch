# 🔥 PyroTouch — Hand-Controlled Fire Simulation

A real-time computer vision project that transforms hand movements into interactive fire particle effects.

PyroTouch uses **MediaPipe Hand Landmarker** to detect hands and track fingertips, while **OpenCV and NumPy** power the real-time visual simulation.

The goal is to explore how computer vision, hand tracking, and particle systems can combine to create interactive experiences.

## ✨ Features

- **Real-time hand detection:** Detects up to 7 hands simultaneously (configurable).
- **21-point hand landmarks:** Uses MediaPipe to identify key hand positions.
- **Multi-fingertip tracking:** Tracks all five fingertips on each detected hand.
- **Interactive particle generation:** Creates fire particles around detected fingertips.
- **Real-time webcam input:** Processes live camera frames.
- **Visual feedback:** Displays detected hands, fingertip positions, and particle counts.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam input and visual rendering |
| MediaPipe | Hand detection and landmark tracking |
| NumPy | Image and numerical operations |
| Random | Particle movement and variation |

## 📁 Project Structure

```text
PyroTouch/
│
├── models/
│   └── hand_landmarker.task
│
├── src/
│   ├── camera_test.py
│   ├── hand_tracking.py
│   ├── particle_system.py
│   └── pyrotouch.py
│
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sanchita235/PyroTouch.git
```

### 2. Navigate into the project

```bash
cd PyroTouch
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install opencv-python mediapipe numpy
```

### 6. Run PyroTouch

```bash
python src/pyrotouch.py
```

Make sure your webcam is connected and accessible.

Press **Q** to exit the simulation.

## 🧠 How It Works

The project follows a simple computer vision pipeline:

1. **Video Capture:** OpenCV captures live frames from the webcam.
2. **Preprocessing:** Frames are flipped, resized, and converted from BGR to RGB.
3. **Hand Detection:** MediaPipe identifies hands in the frame.
4. **Landmark Extraction:** The model provides 21 landmarks for each detected hand.
5. **Fingertip Tracking:** Five fingertip landmarks are extracted:
   - Thumb: 4
   - Index: 8
   - Middle: 12
   - Ring: 16
   - Pinky: 20
6. **Particle Generation:** Fire particles are generated at the detected fingertip coordinates.
7. **Rendering:** OpenCV draws and updates the particles on the webcam frame.

## 🔬 What I'm Learning

Building PyroTouch is helping me understand:

- Computer vision fundamentals
- Real-time object and landmark detection
- MediaPipe Tasks API
- Coordinate transformations
- Particle simulation
- Frame processing and rendering
- Integrating multiple Python libraries into one application

## 🚀 Future Improvements

- [ ] Gesture recognition
- [ ] Pinch-to-ignite interaction
- [ ] Open-palm particle explosion
- [ ] Closed-fist fire extinguishing
- [ ] More realistic fire physics
- [ ] Multiple particle effects
- [ ] Performance optimisation
- [ ] Interactive visual effects

## 👩‍💻 About This Project

PyroTouch is **Project 03** in my 30 Days, 30 AI/ML Projects series.

I'm building these projects to move beyond tutorial-based learning, understand how systems work internally, and develop practical AI/ML engineering skills.

**Built with Python, curiosity, and a lot of debugging.**

---

⭐ If you find this project interesting, consider starring the repository!
