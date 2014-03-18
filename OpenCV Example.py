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
cv2.createTrackbar('H0','image',0,180,nothing)
cv2.createTrackbar('S0','image',0,255,nothing)
cv2.createTrackbar('V0','image',0,255,nothing)
cv2.createTrackbar('H1','image',0,180,nothing)
cv2.createTrackbar('S1','image',0,255,nothing)
cv2.createTrackbar('V1','image',0,255,nothing)
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

cv2.setTrackbarPos('H0','image',30)
cv2.setTrackbarPos('S0','image',20)
cv2.setTrackbarPos('V0','image',30)
cv2.setTrackbarPos('H1','image',100)
cv2.setTrackbarPos('S1','image',120)
cv2.setTrackbarPos('V1','image',60)
cv2.imshow('image',img)

while rval:

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
    invert=cv2.bitwise_not(frame,None)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(invert, cv2.COLOR_BGR2HSV)
    #hsv = cv2.dilate(hsv,None)
    #frame = cv2.GaussianBlur(frame,(5,5),0)
    #hsv=cv2.bitwise_not(hsv,None)

    # define range of blue color in HSV #red
    lower_blue = np.array([h0,s0,v0]) #72,96,141
    upper_blue = np.array([h1,s1,v1]) #102,255,255
    lower_blue = np.array([0,0,0]) 
    upper_blue = np.array([180,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #convert to gray
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)
    
    # Finding Shapes
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    '''ret,thresh = cv2.threshold(edges,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)
    if (len(contours)>0):
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        #print(cv2.contourArea(box))
        a=(box[0][0]+box[1][0]+box[2][0]+box[3][0])/4
        b=(box[0][1]+box[1][1]+box[2][1]+box[3][1])/4
        cv2.circle(frame,(a,b), 5, (0,0,255), -1)'''
    circles = cv2.HoughCircles(edges,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',edges)

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        cv2.destroyWindow("frame")
        cv2.destroyWindow("gray")
        cv2.destroyWindow("image")
        break

