import cv2
import mediapipe as mp
import random
import math
import time
from pathlib import Path
import numpy as np
from draw import draw_pumpkin, draw_bat
import pygame

# -----------------------------
# 1. Game settings
# -----------------------------
WIDTH = 1280
HEIGHT = 720

PUMPKIN_RADIUS = 55
SPAWN_INTERVAL = 1.0       # Seconds between pumpkins
FALL_SPEED = 220           # Pixels per second

BAT_RADIUS = 30
BAT_SPAWN_INTERVAL = 1.8
BAT_SCORE = -10
BAT_SPEED_MIN = 180
BAT_SPEED_MAX = 300

SLICE_SCORE = 10
MISS_SCORE = -5

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "hand_landmarker.task"
)

# -----------------------------
# 2. Pumpkin and bat data
# -----------------------------
pumpkins = []
explosions = []

score = 0
last_spawn_time = time.perf_counter()
previous_time = time.perf_counter()

# bat data
bats = []
last_bat_spawn_time = 0

# -----------------------------
# 3. MediaPipe setup
# -----------------------------
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)

# --------------------------------
# Sound setup
# ---------------------------------

SOUND_DIR = Path(__file__).resolve().parent

MUSIC_PATH = SOUND_DIR / "Halloween_music.mp3"
SLICE_PATH = SOUND_DIR / "cut_sound.mp3"
# Initialize sound system
pygame.mixer.init()

# Load sound effects
slice_sound = pygame.mixer.Sound(str(SLICE_PATH))
slice_sound.set_volume(0.5)

# Start background music and loop forever
pygame.mixer.music.load(str(MUSIC_PATH))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# -----------------------------
#  Main game
# -----------------------------
def main():
    global score, last_spawn_time, last_bat_spawn_time, previous_time

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}\n"
            "Download hand_landmarker.task into the models folder."
        )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check your camera settings."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    try:
        with HandLandmarker.create_from_options(options) as landmarker:
            while True:
                success, frame = camera.read()

                if not success:
                    print("Could not read from webcam.")
                    break

                # Mirror the webcam so movement feels natural
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (640, 480))

                # Do not display the webcam image.
                # Create a black game screen instead.
                frame_mask = np.full(
                    (HEIGHT, WIDTH, 3),
                    35,
                    dtype=np.uint8
                )

                now = time.perf_counter()
                dt = min(now - previous_time, 0.05)
                previous_time = now

                # Track the index fingertip
                rgb = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb
                )

                timestamp_ms = int(now * 1000)
                result = landmarker.detect_for_video(
                    mp_image, timestamp_ms
                )

                fingertip = None

                if result.hand_landmarks:
                    hand = result.hand_landmarks[0]
                    tip = hand[12]

                    finger_x = int(tip.x * WIDTH)
                    finger_y = int(tip.y * HEIGHT)
                    fingertip = (finger_x, finger_y)

                    # Draw a bright fingertip marker
                    cv2.circle(
                        frame_mask, fingertip, 12,
                        (255, 255, 0), -1
                    )
                    cv2.circle(
                        frame_mask, fingertip, 17,
                        (255, 255, 255), 2
                    )

                    connections = (
                        mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
                    )

                    # Draw the hand skeleton
                    for connection in connections:
                        start = hand[connection.start]
                        end = hand[connection.end]

                        x1 = int(start.x * WIDTH)
                        y1 = int(start.y * HEIGHT)
                        x2 = int(end.x * WIDTH)
                        y2 = int(end.y * HEIGHT)

                        cv2.line(
                            frame_mask,
                            (x1, y1),
                            (x2, y2),
                            (0, 200, 100),
                            3
                        )

                    # Draw all 21 landmarks
                    for landmark in hand:
                        x = int(landmark.x * WIDTH)
                        y = int(landmark.y * HEIGHT)

                        cv2.circle(
                            frame_mask,
                            (x, y),
                            5,
                            (0, 255, 180),
                            -1
                        )

                # Spawn pumpkins at random positions along the top
                if now - last_spawn_time >= SPAWN_INTERVAL:
                    pumpkins.append({
                        "x": random.randint(
                            PUMPKIN_RADIUS + 10,
                            WIDTH - PUMPKIN_RADIUS - 10
                        ),
                        "y": -PUMPKIN_RADIUS,
                        "radius": PUMPKIN_RADIUS,
                        "speed": FALL_SPEED
                    })
                    last_spawn_time = now

                # bats fly from the bottom
                if now - last_bat_spawn_time >= BAT_SPAWN_INTERVAL:
                    bats.append({
                        "x": random.randint(BAT_RADIUS, WIDTH - BAT_RADIUS),
                        "y": HEIGHT + BAT_RADIUS,
                        "radius": BAT_RADIUS,
                        "speed": random.uniform(
                            BAT_SPEED_MIN, BAT_SPEED_MAX
                        )
                    })

                    last_bat_spawn_time = now

                # Move pumpkins and check for slicing
                remaining_pumpkins = []

                for pumpkin in pumpkins:
                    pumpkin["y"] += pumpkin["speed"] * dt

                    px = pumpkin["x"]
                    py = pumpkin["y"]
                    radius = pumpkin["radius"]

                    # Is the fingertip inside the pumpkin?
                    sliced = False

                    if fingertip is not None:
                        fx, fy = fingertip
                        distance = math.hypot(
                            fx - px, fy - py
                        )
                        sliced = distance < radius + 10

                    if sliced:
                        score += SLICE_SCORE

                        # Play slice sound effect
                        slice_sound.play()

                        # Create a simple burst effect
                        explosions.append({
                            "x": px,
                            "y": py,
                            "start": now
                        })

                    elif py - radius > HEIGHT:
                        # Pumpkin reached the floor
                        score += MISS_SCORE

                    else:
                        remaining_pumpkins.append(pumpkin)

                pumpkins[:] = remaining_pumpkins

                # Move bats
                for bat in bats:
                    bat["y"] -= bat["speed"] * dt

                # Check collision
                for bat in bats[:]:
                    bx = bat["x"]
                    by = bat["y"]
                    radius = bat["radius"]

                    if fingertip is not None:
                        fx, fy = fingertip

                        hit = math.hypot(fx - bx, fy - by) < radius + 10
                    else:
                        hit = False

                    if hit:
                        score += BAT_SCORE
                        bats.remove(bat)

                # Remove bats out of screen
                bats[:] = [
                    bat for bat in bats
                    if bat["y"] + bat["radius"] > 0
                   ]

                # Draw remaining bats
                for bat in bats:
                    draw_bat(frame_mask, bat["x"], bat["y"], bat["radius"])

                # Draw the surviving pumpkins
                for pumpkin in pumpkins:
                    draw_pumpkin(
                        frame_mask,
                        pumpkin["x"],
                        pumpkin["y"],
                        pumpkin["radius"]
                    )

                # Draw brief explosion rings
                active_explosions = []

                for explosion in explosions:
                    age = now - explosion["start"]

                    if age < 0.25:
                        ring_radius = int(15 + age * 180)
                        cv2.circle(
                            frame_mask,
                            (
                                int(explosion["x"]),
                                int(explosion["y"])
                            ),
                            ring_radius,
                            (0, 220, 255),
                            4
                        )
                        active_explosions.append(explosion)

                explosions[:] = active_explosions

                # Score and instructions
                cv2.putText(
                    frame_mask,
                    f"Score: {score}",
                    (25, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (255, 255, 255), 3
                )

                cv2.putText(
                    frame_mask,
                    "Slice pumpkins with your index finger!",
                    (25, HEIGHT - 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2
                )

                cv2.putText(
                    frame_mask,
                    "Press Q to quit",
                    (WIDTH - 220, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2
                )

                cv2.imshow("Pumpkin Slice", frame_mask)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
