import cv2
import numpy as np
import handTrackingModule as htm
import time
import math
from pynput.keyboard import Key,Controller
# import autopy

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cTime = pTime = 0
detector = htm.handDetector()

keyboard = Controller()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    # print(lmList)
    if len(lmList):
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        # range 15 to 150

        length = math.hypot(x2-x1, y2-y1)

        vChange = int(np.interp(length, [15, 150], [0, 19]))


        if vChange<10:
            # Decrease the Volume
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
            print(vChange, length, vChange, "DOWN")
            cv2.putText(img, "Volume Down", (10, 170), cv2.FONT_HERSHEY_PLAIN, 3, (244, 0, 244), 4)
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            
        else:
            # Increase the volume
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            print(vChange, length, vChange, "UP")
            cv2.putText(img, "Volume Up", (10, 170), cv2.FONT_HERSHEY_PLAIN, 3, (244, 0, 244), 4)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (244, 0, 244), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


