import cv2

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
