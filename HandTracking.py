import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.tipID=[4,8,12,16,20]
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,1,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findhands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB,)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLandmarks,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw=True):
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(Hand.landmark):
                height,width,chanels=img.shape
                xpos,ypos=int(lm.x*width),int(lm.y*height)
                self.lmList.append([id,xpos,ypos])
                if draw:
                    cv2.circle(img,(xpos,ypos),6,(255,255,0),cv2.FILLED)

        return self.lmList
    def fingersUp(self ):
        fingers=[]
        if self.lmList[self.tipID[0]][1] >= self.lmList[self.tipID[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if self.lmList[self.tipID[id]][2] < self.lmList[self.tipID[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        succes, img = cap.read()
        img = detector.findhands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.imshow("Image",img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()