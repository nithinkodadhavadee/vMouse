import cv2
import numpy as np
import handTrackingModule as htm
import time
import pyautogui

wScr, hScr = pyautogui.size()
wCam, hCam = 640, 480
cTime = pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 10
frameR = 150
pyautogui.FAILSAFE = False
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()

while True:
    # 1. Find hand Landmraks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw = False)
    
    # 2. Get the tip of the index and middle fingers
    if len(lmList):
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. Only Index Fingers: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, wCam - frameR), (0,wScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX)/smoothening
            clocY = plocY + (y3 - plocY)/smoothening
            # 7. Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1,y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            # 8. Both Index and Middle fingers are up: Click Mode
        if fingers[1] == 1 and fingers[2] == 1:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, wCam - frameR), (0,wScr))
            # 9. Find distance between Index and Middle Fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # 10. Click mouse if distance is short
            if length < 20: 
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(wScr - x3, y3)

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (244, 0, 244), 4)

    # 12. Display
    cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)