
import cv2
from pathlib import Path

# ---------------- SETTINGS ----------------
VIDEO = Path.home() / "Desktop" / "video.mp4"   # Change if needed
FPS = 10
WIDTH = 128
HEIGHT = 64
THRESHOLD = 128
# ------------------------------------------

cap = cv2.VideoCapture(str(VIDEO))

if not cap.isOpened():
    print("Couldn't open video!")
    quit()

src_fps = cap.get(cv2.CAP_PROP_FPS)
skip = max(1, round(src_fps / FPS))

frames = []
frame_num = 0

while True:
    ok, frame = cap.read()

    if not ok:
        break

    if frame_num % skip != 0:
        frame_num += 1
        continue

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, bw = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)

    packed = []

    # Pack into Adafruit_GFX drawBitmap() format
    for y in range(HEIGHT):
        for x in range(0, WIDTH, 8):
            b = 0

            for bit in range(8):
                if bw[y, x + bit] > 0:
                    b |= (0x80 >> bit)

            packed.append(b)

    frames.append(packed)
    frame_num += 1

cap.release()

with open("video.h", "w") as f:

    f.write("#pragma once\n\n")
    f.write("#include <Arduino.h>\n\n")
    f.write(f"#define FRAME_COUNT {len(frames)}\n\n")

    f.write("const uint8_t video[][1024] PROGMEM = {\n")

    for frame in frames:
        f.write("{")
        f.write(",".join(map(str, frame)))
        f.write("},\n")

    f.write("};\n")

print("Done!")
print(f"{len(frames)} frames")
