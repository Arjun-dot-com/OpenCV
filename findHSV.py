import cv2 as cv
import numpy as np
from stackimages import stack

#ignore this function
def empty(a):
    pass


#function to create trackbars
def setupTrackbars():
    cv.namedWindow("TrackBars")
    cv.resizeWindow("TrackBars",640,240)
    cv.createTrackbar("Hue min","TrackBars",0,179,empty)
    cv.createTrackbar("Hue max","TrackBars",179,179,empty)
    cv.createTrackbar("Sat min","TrackBars",0,255,empty)
    cv.createTrackbar("Sat max","TrackBars",255,255,empty)
    cv.createTrackbar("Val min","TrackBars",0,255,empty)
    cv.createTrackbar("Val max","TrackBars",255,255,empty)

#function to get trackbar values
def getTrackbarValues():
    h_min=cv.getTrackbarPos("Hue min","TrackBars")
    h_max=cv.getTrackbarPos("Hue max","TrackBars")
    s_min=cv.getTrackbarPos("Sat min","TrackBars")
    s_max=cv.getTrackbarPos("Sat max","TrackBars")
    v_min=cv.getTrackbarPos("Val min","TrackBars")
    v_max=cv.getTrackbarPos("Val max","TrackBars")
    return h_min,s_min,v_min,h_max,s_max,v_max

cap = cv.VideoCapture(0)
cap.set(3,640)  # id for width is 3
cap.set(4,480)  # id for height is 4
cap.set(10,150) # id for brightness is 10

setupTrackbars()

while True:
    success,img=cap.read()
    if not success:
        break

    imgHSV=cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h_min,s_min,v_min,h_max,s_max,v_max=getTrackbarValues()

    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv.inRange(imgHSV,lower,upper)
    imgRes=cv.bitwise_and(img,img,mask=mask)

    imgFinal=stack(0.75, [[img,imgRes,mask]])
    cv.imshow("Stacked Result",imgFinal)

    if cv.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv.destroyAllWindows()
