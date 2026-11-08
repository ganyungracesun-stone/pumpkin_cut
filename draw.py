import cv2
import numpy as np

# -----------------------------
# 4. Draw a pumpkin
# -----------------------------
def draw_pumpkin(frame, x, y, radius):
    x, y = int(x), int(y)

    # Orange pumpkin body
    cv2.circle(
        frame, (x, y), radius, (0, 140, 255), -1
    )

    # Pumpkin ridges
    cv2.ellipse(
        frame, (x, y), (radius // 2, radius),
        0, 0, 360, (0, 100, 210), 2
    )
    cv2.ellipse(
        frame, (x, y), (radius * 3 // 4, radius),
        0, 0, 360, (0, 100, 210), 2
    )

    # Green stem
    cv2.rectangle(
        frame,
        (x - 5, y - radius - 9),
        (x + 5, y - radius + 5),
        (30, 150, 30), -1
    )

    # Cute eyes and smile
    cv2.circle(
        frame, (x - 12, y - 5), 4, (0, 0, 0), -1
    )
    cv2.circle(
        frame, (x + 12, y - 5), 4, (0, 0, 0), -1
    )
    cv2.ellipse(
        frame, (x, y + 5), (12, 7),
        0, 0, 180, (0, 0, 0), 2
    )

#-----------------------------------
# draw bats
#-----------------------------------
def draw_bat(frame, x, y, radius):
    x, y, radius = int(x), int(y), int(radius)

    # Wings
    left_wing = np.array([
        [x, y],
        [x - radius, y - radius // 2],
        [x - radius, y + radius // 3],
        [x - radius // 3, y + radius // 2]
    ], dtype=np.int32)

    right_wing = np.array([
        [x, y],
        [x + radius, y - radius // 2],
        [x + radius, y + radius // 3],
        [x + radius // 3, y + radius // 2]
    ], dtype=np.int32)

    cv2.fillPoly(frame, [left_wing], (0, 0, 0))
    cv2.fillPoly(frame, [right_wing], (0, 0, 0))

    # Body and head
    cv2.ellipse(frame, (x, y), (radius // 4, radius // 2),
                0, 0, 360, (100, 40, 160), -1)  #purple
    cv2.circle(frame, (x, y - radius // 3),
               radius // 4, (180, 70, 220), -1) # bright purple

    # Red eyes
    cv2.circle(frame, (x - 4, y - radius // 3),
               2, (0, 0, 255), -1)
    cv2.circle(frame, (x + 4, y - radius // 3),
               2, (0, 0, 255), -1)