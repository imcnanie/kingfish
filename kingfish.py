#!/usr/bin/python
## TODO ##
#autosave hues

import cv2
import numpy as np

TRACKBAR_RED = [72,148,100,
                102,255,255]
TRACKBAR_BLU = [54,88,145,
                102,255,255]
TRACKBAR_YEL = [80,90,100,
                110,120,130]

mode=0
visibleYellow=0

class KingfishApp(object):
    def __init__(self):
        self.mode = 0

        self.cv_init()
        self.cv_show_trackbars()
        
        while True:
            self.cv_create_stream()
            self.cv_update_trackbars()
            self.cv_track(invert=True)
            self.cv_show_frames()

            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                cv2.destroyWindow("frame")
                cv2.destroyWindow("track_image")
                self.vc.release
                break

    def cv_init(self):
        self.vc = cv2.VideoCapture(0)
        
        if self.vc.isOpened(): # try to get the first frame
            rval, img = self.vc.read()
        else:
            rval = False

        img = np.zeros((300,512,3), np.uint8)

    def cv_create_stream(self):
        _, self.frame = self.vc.read()

    def cv_track(self,invert=False):
        if invert:
            # Invert for Red
            invert=cv2.bitwise_not(self.frame,None)
            # Convert BGR to HSV
            hsv = cv2.cvtColor(invert, cv2.COLOR_BGR2HSV)
        else:
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV #red
        lower = np.array([self.h0,self.s0,self.v0])
        upper = np.array([self.h1,self.s1,self.v1])
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower, upper)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(self.frame,self.frame,mask=mask)
        # Convert to grayscale
        gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        self.gray = cv2.medianBlur(gray,5)
        # Find contours
        edges = cv2.Canny(self.gray,50,150,apertureSize = 3)
        ret,thresh = cv2.threshold(edges,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        if (len(contours)>0):
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.frame,[box],0,(0,0,255),2)
            # AREA OF RECTANGLE + CENTER
            #print(cv2.contourArea(box))
            a=(box[0][0]+box[1][0]+box[2][0]+box[3][0])/4
            b=(box[0][1]+box[1][1]+box[2][1]+box[3][1])/4
            cv2.circle(self.gray,(a,b), 5, (0,0,255), -1)

            '''
            if (a<200 and cv2.contourArea(box)>10000 and visibleYellow==0):
                mode+=1
                visibleYellow=1  
            if (cv2.contourArea(box)<3000 and visibleYellow==1):
                visibleYellow=0
        if (len(contours)<0):
            visibleYellow=0
        print(str(mode)+" "+str(visibleYellow))'''

    def cv_show_frames(self):
        frame = cv2.resize(self.frame, (0,0), fx=0.5, fy=0.5)
        gray = cv2.resize(self.gray, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('frame',frame)
        cv2.imshow('grayscale',gray)

    def cv_update_trackbars(self):
        self.h0 = cv2.getTrackbarPos('H0','track_image')
        self.s0 = cv2.getTrackbarPos('S0','track_image')
        self.v0 = cv2.getTrackbarPos('V0','track_image')
        self.h1 = cv2.getTrackbarPos('H1','track_image')
        self.s1 = cv2.getTrackbarPos('S1','track_image')
        self.v1 = cv2.getTrackbarPos('V1','track_image')

    def cv_show_trackbars(self):
        def nothing(x):
            pass

        cv2.namedWindow('track_image')
        cv2.createTrackbar('H0','track_image',0,180,nothing)
        cv2.createTrackbar('S0','track_image',0,255,nothing)
        cv2.createTrackbar('V0','track_image',0,255,nothing)
        cv2.createTrackbar('H1','track_image',0,180,nothing)
        cv2.createTrackbar('S1','track_image',0,255,nothing)
        cv2.createTrackbar('V1','track_image',0,255,nothing)
        
        cv2.setTrackbarPos('H0','track_image',TRACKBAR_RED[0])
        cv2.setTrackbarPos('S0','track_image',TRACKBAR_RED[1])
        cv2.setTrackbarPos('V0','track_image',TRACKBAR_RED[2])
        cv2.setTrackbarPos('H1','track_image',TRACKBAR_RED[3])
        cv2.setTrackbarPos('S1','track_image',TRACKBAR_RED[4])
        cv2.setTrackbarPos('V1','track_image',TRACKBAR_RED[5])
        
        self.h0 = cv2.getTrackbarPos('H0','track_image')
        self.s0 = cv2.getTrackbarPos('S0','track_image')
        self.v0 = cv2.getTrackbarPos('V0','track_image')
        self.h1 = cv2.getTrackbarPos('H1','track_image')
        self.s1 = cv2.getTrackbarPos('S1','track_image')
        self.v1 = cv2.getTrackbarPos('V1','track_image')
         
if __name__ == '__main__':
    cur_app = KingfishApp()
