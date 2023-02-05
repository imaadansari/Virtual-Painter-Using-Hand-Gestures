import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
from datetime import datetime

##############
brushThickness=15
eraserThickness=50
##############

folderPath='Header'
myList=os.listdir(folderPath)
print(myList)

overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header=overlayList[0]
drawColor=(255,0,255)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector=htm.handDetector(detentionCon=1)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    # 1. Import Image
    success,img=cap.read()
    img=cv2.flip(img,1)

    # 2. Find Hand Landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList)

        #tip of the index and middle fingers
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        # 3. Check which fingers are up
        fingers=detector.fingersUp()
        #print(fingers)
        
        # 4. If Selection Mode - Two Fingers are up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print('Selection Mode')
            #Checking for the click
            if y1<125:
                if 220<x1<340:
                    header=overlayList[0]
                    drawColor=(255,0,255)
                elif 520<x1<640:
                    header=overlayList[1]
                    drawColor=(255,100,100)
                elif 820<x1<940:
                    header=overlayList[2]
                    drawColor=(0,255,0)
                elif 1120<x1<1240:
                    header=overlayList[3]
                    drawColor=(0,0,0)
                elif 20<x1<140:
                    imgCanvas=np.zeros((720,1280,3),np.uint8)

            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        # 5. If Drawing Mode - Index Finger is  up 
        if fingers[1] and fingers[2] == False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print('Drawing Mode')
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    h,w,c=header.shape
    img[0:h, 0:w]=header
    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    #cv2.imshow("Canvas",imgCanvas)
    key=cv2.waitKey(1)
    if int(key)==ord('s'):
        imgName='canvas_'+str(datetime.today().strftime('%Y_%m_%d_%H_%M_%S'))+'.jpg'
        cv2.imwrite(f'saved_canvas/{imgName}',imgCanvas)
        print('image saved')