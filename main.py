import cv2
from util import get_limits
from PIL import Image

yellow = [0, 255, 255]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l,h = get_limits(yellow)

    mask = cv2.inRange(hsvImage, l, h) # like ip mask

    mask_ = Image.fromarray(mask)

    box = mask_.getbbox()
    
    if box is not None:

        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255,0), 5)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()