import numpy as np
import cv2

def get_limits(color_bgr):
    c = np.uint8([[color_bgr]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    lowerLimit = np.array([hsvC[0][0][0] - 10, 100, 100], dtype=np.uint8)
    upperLimit = np.array([hsvC[0][0][0] + 10, 255, 255], dtype=np.uint8)
    return lowerLimit, upperLimit

# VIBGYOR BGR definitions
COLORS = {
    "Violet": [238, 130, 238],
    "Indigo": [75, 0, 130],
    "Blue":   [255, 0, 0],
    "Green":  [0, 255, 0],
    "Yellow": [0, 255, 255],
    "Orange": [0, 165, 255],
    "Red":    [0, 0, 255]
}
