import cv2
import os
import time
import HandTracking as htm

wCam,hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(detectionCon=0.8)
while True:
    succes,img=cap.read()
    img=detector.findhands(img)
    lmList=detector.findPosition(img,draw=False)
    print(lmList)
    if len(lmList)!=0:
        if lmList[8][2]<=lmList[6][2]:
            print("aratator")
    if len(lmList) != 0:
        if lmList[12][2] <= lmList[10][2]:
            print("interzis")
    cv2.imshow("Image",img)
    cv2.waitKey(1)