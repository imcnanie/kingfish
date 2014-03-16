import cv2
import numpy as np

cv2.namedWindow("frame")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, img = vc.read()
else:
    rval = False


def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H0','image',0,255,nothing)
cv2.createTrackbar('S0','image',0,255,nothing)
cv2.createTrackbar('V0','image',0,255,nothing)
cv2.createTrackbar('H1','image',0,255,nothing)
cv2.createTrackbar('S1','image',0,255,nothing)
cv2.createTrackbar('V1','image',0,255,nothing)
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while rval:
    
    cv2.imshow('image',img)

    # get current positions of four trackbars
    h0 = cv2.getTrackbarPos('H0','image')
    s0 = cv2.getTrackbarPos('S0','image')
    v0 = cv2.getTrackbarPos('V0','image')
    h1 = cv2.getTrackbarPos('H1','image')
    s1 = cv2.getTrackbarPos('S1','image')
    v1 = cv2.getTrackbarPos('V1','image')
    s = cv2.getTrackbarPos(switch,'image')

    #print res.dtype

    # Take each frame
    _, frame = vc.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = cv2.dilate(hsv,None)
    #frame = cv2.GaussianBlur(frame,(5,5),0)

    # # define range of blue color in HSV
    # lower_blue = np.array([50,80,80])
    # upper_blue = np.array([100,200,200])

    # define range of blue color in HSV
    lower_blue = np.array([h0,s0,v0])
    upper_blue = np.array([h1,s1,v1])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #convert to gray
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)
    
    # Finding Shapes
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    ret,thresh = cv2.threshold(edges,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)
    if (len(contours)>0):
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
    
    #minLineLength = 100
    #maxLineGap = 10
    #lines = cv2.HoughLinesP(gray,1,np.pi/180,100,minLineLength,maxLineGap)
    #if lines is not None:
    #    for x1,y1,x2,y2 in lines[0]:
    #        cv2.line(frame,(x1,y1),(x2,y2),(50,255,50),2)
        
    #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(gray, contours, -1, (100,100,100), 3)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',edges)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        cv2.destroyWindow("frame")
        cv2.destroyWindow("gray")
        break

