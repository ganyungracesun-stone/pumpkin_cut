# 🎃 Pumpkin Slice Game

A fun, interactive computer vision game built with **Python, OpenCV, and MediaPipe**. Use your hand movements in front of a webcam to slice flying pumpkins, avoid bats, and earn points!

## 🎮 Game Overview

Pumpkin Slice is a webcam-based game that uses real-time hand tracking to let players interact with objects on the screen—without a mouse or keyboard.

Move your hand in front of the camera and use your index-fingertip to slice pumpkins. Watch out for bats: hitting one will cost you points!

## ✨ Features

- **Real-time Hand Tracking:** Detects hand landmarks using MediaPipe.
- **Gesture-based Interaction:** Uses the index fingertip to interact with game objects.
- **Pumpkin Slicing:** Slice pumpkins to earn points.
- **Bat Obstacles:** Avoid flying bats to protect your score.
- **Sound Effects:** Audio feedback for slicing and other game events.
- **Interactive Gameplay:** Combines computer vision with a simple arcade-style experience.

## 🛠️ Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- Pygame
- Math and Random (Python standard libraries)

## 📁 Project Structure

```text
PumpkinSlice/
│
├── main.py
├── models/
│   └── hand_landmarker.task
├── sounds/
│   └── Halloween_music.mp3, cut_sound.mp3
└── README.md
```

## 🌿 Git Branches

This project has two development branches with different gameplay features:

| Branch | Description |
|---|---|
| `master` (`origin`) | Main version of the game, without bat obstacles. |
| `bat_fly` | Extended version featuring flying bats as obstacles. |

### Switching Between Versions

To run the main version without bats:

```bash
git checkout master
```

To try the version with flying bats:

```bash
git checkout bat_fly
```

The `bat_fly` branch introduces flying bat obstacles. Players must avoid hitting them to prevent losing points.


## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ganyungracesun-stone/pumpkin_cut
cd PumpkinSlice
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe pygame
```

### 3. Prepare the hand tracking model

Make sure the MediaPipe hand landmark model file is available at:

```text
/hand_landmarker.task
```

### 4. Run the game

```bash
python cut_pumpkin.py
```

Allow webcam access when prompted.

## 🕹️ How to Play

1. Start the game and position yourself in front of your webcam.
2. Show your hand to the camera.
3. Move your fingertips across the game screen to slice pumpkins.
4. Earn **10 points** for each pumpkin sliced.
5. Avoid bats, which deduct **5 points** when hit.
6. Try to achieve the highest score!

Press **Q** to quit the game.

## 🧠 How It Works

The game uses MediaPipe's hand landmark detection to identify 21 key points on the hand.

The index fingertip positions are used to detect collisions with pumpkins and bats. OpenCV handles the game graphics and display, while Pygame provides sound effects.

The game loop continuously:
- Captures webcam frames.
- Detects hand landmarks.
- Updates object positions.
- Checks collisions.
- Updates the score.
- Draws the game scene and displays it.

## 🔮 Future Improvements

- Add more game levels and difficulty settings.
- Introduce different objects with unique effects.
- Add a high-score leaderboard.
- Improve hand gesture recognition.
- Add more sound effects and visual animations.

## 👩‍💻 Author

Developed as a hands-on project exploring **Computer Vision and Human-Computer Interaction** using Python.

---

*Have fun slicing pumpkins!* 🎃
