import cv2
import numpy as np
import handTrackingModule as htm
import time
# import autopy

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cTime = pTime = 0
detector = htm.handDetector()

tipIds = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList):
        fingers = []

        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]: # This is just for the left hand. 
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range (1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (244, 0, 244), 4)


    cv2.imshow("Image", img)
    cv2.waitKey(1)