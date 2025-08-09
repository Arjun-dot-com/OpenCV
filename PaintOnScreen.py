import cv2 as cv
import numpy as np
from stackimages import stack

cap=cv.VideoCapture(0)
cap.set(3,640)  # id for width is 3
cap.set(4,480)  # id for height is 4
cap.set(10,150) # id for brightness is 10

#make the below nested lists if need more colors
myColours=[133,204,0,179,255,255] #first all mins then all max
myColourValues=[0,0,255] #BGR color code for the marker color
myPoints=[] # [x,y,Color_idx(if more than one color)]

def findColours(img, myColours, myColourValues):
    imgHSV=cv.cvtColor(img, cv.COLOR_BGR2HSV)
    newPoint=[]
    lower=np.array(myColours[:3])
    upper=np.array(myColours[3:6])
    mask=cv.inRange(imgHSV, lower, upper)
    x,y=getCountours(mask)
    if x!=0 and y!=0:
        newPoint=[x, y]
        cv.circle(imgResult, (x, y), 10, myColourValues, cv.FILLED)
    return newPoint


def getCountours(img):
    countours,hierarchy=cv.findContours(img, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in countours:
        area=cv.contourArea(cnt)
        if area>500:
            #cv.drawContours(imgResult,cnt, -1, (255,0,0),3)
            peri=cv.arcLength(cnt,True)
            approx=cv.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv.boundingRect(approx)
    return x+w//2,y

def colorOnCanvas(myPoints, myColourValues):
    for point in myPoints:
        cv.circle(imgResult, (point[0], point[1]), 8, myColourValues, cv.FILLED)

while True:
    success,img=cap.read()
    imgResult=img.copy()
    if not success:
        break
    
    newPoint=findColours(img, myColours, myColourValues)
    if len(newPoint)!=0:
        myPoints.append(newPoint)
    
    if len(myPoints)!=0:
        colorOnCanvas(myPoints, myColourValues)
    
    imgFinal1=cv.resize(imgResult, (640,480))
    imgFinal=cv.flip(imgFinal1,1)
    cv.imshow("Result",imgFinal)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv.destroyAllWindows()
