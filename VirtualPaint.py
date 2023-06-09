import cv2
import mediapipe as mp
import time
import os
import numpy as np
import HandTracking as htm
import math
path = "Header"
headerList = os.listdir(path)
overlayList = []
for imagePath in headerList:
    img = cv2.imread(f"{path}/{imagePath}")
    overlayList.append(img)
print(len(overlayList))

header = overlayList[0]
footer = overlayList[7]
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.5)
eraserThikness = 50
brushThikness = 15
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
drawColor=(0,0,0)
selectmode=0
selectmode2=0
R=0
G=0
B=0
while True:
    succes, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findhands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        # print(lmList)


    #     varf deget index 8
        deget1x, deget1y = lmList[8][1:]
        deget2x, deget2y = lmList[12][1:]


        fingers = detector.fingersUp()
        # print(fingers)

        if fingers[1] and fingers[2] and fingers[3] == 0 and fingers[4] == 0 :
            print("selection mode")
            xp, yp = 0, 0
        #     check for click
            if deget1x < 200:
                # draw color
                if deget1y < 170:
                    selectmode=0
                    header = overlayList[8]
                    selectmode2 = 0
                if deget1y < 360  and  deget1y >= 170:
                    header = overlayList[2]
                    selectmode = 1
                # brush size
                if deget1y < 542 and deget1y >= 360:
                    header = overlayList[3]
                    selectmode = 2
                    selectmode2 = 0

                # eraser
                if deget1y<720 and deget1y >= 542:
                    header = overlayList[4]
                    drawColor = (0, 0, 0)
                    selectmode = 3
                    selectmode2 = 0





        ##################### brush thincknes 5-50
        if selectmode == 2 and fingers[2] == False:
            x11,y12=lmList[4][1],lmList[4][2]
            x21,y22=lmList[8][1],lmList[8][2]

            cx,cy=(x11+x21)//2,(y12+y22)//2
            cv2.circle(img,(x11,y12),15,(255,255,0),cv2.FILLED)
            cv2.circle(img,(x21,y22),15,(255,255,0),cv2.FILLED)
            cv2.line(img,(x11,y12),(x21,y22),(255,255,0),3)


            length=math.hypot(x21-x11,y22-y12)

            brushThikness=int(np.interp(length,[30,250],[5,100]))
            print(brushThikness)

        ####################


        if selectmode == 1 and fingers[2] == False:
            if deget1x < 1280 and deget1x > 1080:
                # draw color
                if deget1y < 85:
                    selectmode2 = 1
                    footer = overlayList[1]

                if deget1y < 160 and deget1y >= 85:
                    drawColor = (255, 150, 0)
                    selectmode2 = 2
                    footer = overlayList[6]

                # brush size
                if deget1y < 250 and deget1y >= 160:
                    footer = overlayList[5]
                    selectmode2 = 3

        ##################### red range
        if selectmode2 == 1 and fingers[2] == False:
            x11, y12 = lmList[4][1], lmList[4][2]
            x21, y22 = lmList[8][1], lmList[8][2]

            cx, cy = (x11 + x21) // 2, (y12 + y22) // 2
            cv2.circle(img, (x11, y12), 15, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x21, y22), 15, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x11, y12), (x21, y22), (255, 255, 0), 3)

            length = math.hypot(x21 - x11, y22 - y12)

            R = int(np.interp(length, [30, 250], [0, 255]))
        ####################

        ##################### green range
        if selectmode2 == 2 and fingers[2] == False:
            x11, y12 = lmList[4][1], lmList[4][2]
            x21, y22 = lmList[8][1], lmList[8][2]

            cx, cy = (x11 + x21) // 2, (y12 + y22) // 2
            cv2.circle(img, (x11, y12), 15, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x21, y22), 15, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x11, y12), (x21, y22), (255, 255, 0), 3)

            length = math.hypot(x21 - x11, y22 - y12)

            G = int(np.interp(length, [30, 250], [0, 255]))
        ####################

        ##################### green range
        if selectmode2 == 3 and fingers[2] == False:
            x11, y12 = lmList[4][1], lmList[4][2]
            x21, y22 = lmList[8][1], lmList[8][2]

            cx, cy = (x11 + x21) // 2, (y12 + y22) // 2
            cv2.circle(img, (x11, y12), 15, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x21, y22), 15, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x11, y12), (x21, y22), (255, 255, 0), 3)

            length = math.hypot(x21 - x11, y22 - y12)

            B = int(np.interp(length, [30, 250], [0, 255]))
        ####################
        if selectmode != 3:
            drawColor=(R,G,B)



        ############################
        if fingers[1] and fingers[2] == False and selectmode != 2 and selectmode != 1:
            cv2.circle(img, (deget1x, deget1y), brushThikness, drawColor, cv2.FILLED)
            print("Draw mode")
            if xp ==0 and yp == 0:
                xp, yp = deget1x, deget1y
            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (deget1x, deget1y), drawColor, brushThikness)
                cv2.line(imgCanvas, (xp, yp), (deget1x, deget1y), drawColor, brushThikness)
            else:
                cv2.line(img, (xp, yp), (deget1x, deget1y), drawColor, brushThikness)
                cv2.line(imgCanvas, (xp, yp), (deget1x, deget1y), drawColor, brushThikness)

        xp, yp = deget1x, deget1y



    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255, cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    img[0:720,0:200] = header
    if selectmode == 1:
        img[0:250, 1080:1280] = footer
    cv2.imshow("Image", img)
    print(selectmode2)




    cv2.waitKey(1)
