import cv2
from util import get_limits
from PIL import Image
import numpy as np

# VIBGYOR colors in BGR
COLORS = {
    "Violet": [238, 130, 238],
    "Indigo": [75, 0, 130],
    "Blue": [0, 0, 255],
    "Green": [0, 255, 0],
    "Yellow": [0, 255, 255],
    "Orange": [0, 165, 255],
    "Red": [0, 0, 255]  # red overlaps with blue channel in BGR format
}

cap = cv2.VideoCapture(0)

roi_coords = None  # Region of Interest coordinates

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # If ROI selected, crop it for analysis
    if roi_coords is not None:
        x, y, w, h = roi_coords
        roi = frame[y:y + h, x:x + w]
        hsvImage = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        detected_color = None
        for name, bgr in COLORS.items():
            lower, upper = get_limits(bgr)
            mask = cv2.inRange(hsvImage, lower, upper)

            # Calculate percentage of mask pixels
            percentage = (cv2.countNonZero(mask) / (w * h)) * 100

            if percentage > 5:
                detected_color = f"{name} ({percentage:.1f}%)"
                break

        if detected_color:
            cv2.putText(frame, detected_color, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Draw ROI rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # On-screen instructions
    cv2.putText(frame, "Press 'r' to select ROI, 'q' to quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Detecting VIBGYOR if >50% in ROI",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("VIBGYOR Detector", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord("r"):
    # Pause frame to select ROI
        temp_frame = frame.copy()
        roi_coords = cv2.selectROI("Select ROI", temp_frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select ROI")
        if roi_coords == (0, 0, 0, 0):
            roi_coords = None  # Ignore invalid ROI


cap.release()
cv2.destroyAllWindows()
