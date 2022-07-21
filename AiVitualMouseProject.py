import cv2
import numpy as np
import HandTrackingMoudule as htm
import time
import autopy

#################################
wCam, hCam = 1280, 720
#################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
print(wScr,hScr)

while True:
    # 1. Find hand Landmarks
    _, img = cap.read()
    # img = cv2.flip(img, 1)  # 选择镜像
    img = detector.findHands(img)
    lmList = detector.findPostion(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print((x1,y1,x2,y2))

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:


            # 5. Convert Coordinates
            x3 = np.interp(x1,  (0,wCam),(0,wScr))
            y3 = np.interp(y1,  (0,hCam),(0,hScr))

            # 6. Smoothen Values
            # 7. Move Mouse
            autopy.mouse.move(wScr-x3, y3)
            cv2.circle(img,(x1,y1),15,(255,0,255), cv2.FILLED)
        # 8. Both Index and middle fingers are up : Clicking Mode
        # 9. FInd distance between fingers
        # 10. Click mouser if distance short


    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_PLAIN,
                3,(0,255,0),3)
    # 12. Dispaly
    cv2.imshow("Mouse",img)
    cv2.waitKey(1)
