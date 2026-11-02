import cv2
import numpy as np
import os
import sys

def read_image_unicode(path):
    with open(path, "rb") as fp:
        data = fp.read()
    return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

def write_image_unicode(path, img, quality=98):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    success, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if success:
        with open(path, "wb") as fp:
            fp.write(buf)
        return True
    return False

def get_sparkle_box_coords(h, w):
    s = w / 1376.0
    cx = w - 97.5 * s
    cy = h - 97.6 * s
    rad = 36.0 * s
    
    x0 = max(0, int(round(cx - rad)))
    y0 = max(0, int(round(cy - rad)))
    x1 = min(w, int(round(cx + rad)))
    y1 = min(h, int(round(cy + rad)))
    return (x0, y0, x1, y1), (cx, cy, s)

print("Coordinate helper ready.")
