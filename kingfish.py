#!/usr/bin/python

import cv2
import numpy as np

TRACKBAR_RED = [72,148,100,
                102,255,255]
TRACKBAR_BLU = [54,88,145,
                102,255,255]
TRACKBAR_YEL = [80,90,100,
                110,120,130]

class KingfishApp(object):
    def __init__(self):
        self.vc = cv2.VideoCapture(0)
        
        if self.vc.isOpened(): # try to get the first frame
            rval, img = self.vc.read()
        else:
            rval = False

        img = np.zeros((300,512,3), np.uint8)

        self.red_vals = self.show_trackbars("red")
        self.blu_vals = self.show_trackbars("blue")
        self.yel_vals = self.show_trackbars("yellow")
        
        while True:
            self.create_stream()
            self.update_trackbars()
            self.track_red()
            self.track_blue()
            self.track_yellow()
            self.show_frames()

            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                cv2.destroyWindow("frame")
                ## cv2.destroyWindow("gray")
                ## cv2.destroyWindow("image")
                break

    def create_stream(self):
        _, self.frame = self.vc.read()

    def track_red(self):
        #invert cause red is stupid
        invert=cv2.bitwise_not(self.frame,None)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(invert, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV #red
        lower_red = np.array([self.hr0,self.sr0,self.vr0])
        upper_red = np.array([self.hr1,self.sr1,self.vr1])
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(self.frame,self.frame,mask=mask)
        # Convert to grayscale
        red_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        red_gray = cv2.medianBlur(red_gray,5)
        # Find contours
        edges = cv2.Canny(red_gray,50,150,apertureSize = 3)
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
            cv2.circle(self.frame,(a,b), 5, (0,0,255), -1)


        self.red_gray = red_gray

    
    def track_blue(self):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV #red
        lower_blue = np.array([self.hb0,self.sb0,self.vb0])
        upper_blue = np.array([self.hb1,self.sb1,self.vb1])
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(self.frame,self.frame,mask=mask)
        # Convert to grayscale
        blue_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        blue_gray = cv2.medianBlur(blue_gray,5)
        # Find contours
        edges = cv2.Canny(blue_gray,50,150,apertureSize = 3)
        ret,thresh = cv2.threshold(edges,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        if (len(contours)>0):
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.frame,[box],0,(0,255,0),2)

        self.blue_gray = blue_gray

    def track_yellow(self):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV #red
        lower_yellow = np.array([self.hy0,self.sy0,self.vy0])
        upper_yellow = np.array([self.hy1,self.sy1,self.vy1])
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(self.frame,self.frame,mask=mask)
        # Convert to grayscale
        yellow_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        yellow_gray = cv2.medianBlur(yellow_gray,5)
        # Find contours
        edges = cv2.Canny(yellow_gray,50,150,apertureSize = 3)
        ret,thresh = cv2.threshold(edges,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        if (len(contours)>0):
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.frame,[box],0,(255,0,0),2)

        self.yellow_gray = yellow_gray

    def show_frames(self):
        frame = cv2.resize(self.frame, (0,0), fx=0.5, fy=0.5)
        red_gray = cv2.resize(self.red_gray, (0,0), fx=0.5, fy=0.5)
        blue_gray = cv2.resize(self.blue_gray, (0,0), fx=0.5, fy=0.5)
        yellow_gray = cv2.resize(self.yellow_gray, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('frame',frame)
        ## cv2.imshow('red_grayscale',red_gray)
        ## cv2.imshow('blue_grayscale',blue_gray)
        ## cv2.imshow('yellow_grayscale',yellow_gray)
        ## cv2.resizeWindow('frame',250,250)
        ## cv2.resizeWindow('red_grayscale', 250,250)
        ## cv2.resizeWindow('blue_grayscale', 250,250)
        ## cv2.resizeWindow('yellow_grayscale', 250,250)
        ## cv2.moveWindow('frame', 1040, 50)
        ## cv2.moveWindow('red_grayscale', 10, 50)
        ## cv2.moveWindow('blue_grayscale', 340, 50)
        ## cv2.moveWindow('yellow_grayscale', 680,50)

    def update_trackbars(self):
        self.hr0 = cv2.getTrackbarPos('HR0','red_image')
        self.sr0 = cv2.getTrackbarPos('SR0','red_image')
        self.vr0 = cv2.getTrackbarPos('VR0','red_image')
        self.hr1 = cv2.getTrackbarPos('HR1','red_image')
        self.sr1 = cv2.getTrackbarPos('SR1','red_image')
        self.vr1 = cv2.getTrackbarPos('VR1','red_image')

        self.hb0 = cv2.getTrackbarPos('HB0','blue_image')
        self.sb0 = cv2.getTrackbarPos('SB0','blue_image')
        self.vb0 = cv2.getTrackbarPos('VB0','blue_image')
        self.hb1 = cv2.getTrackbarPos('HB1','blue_image')
        self.sb1 = cv2.getTrackbarPos('SB1','blue_image')
        self.vb1 = cv2.getTrackbarPos('VB1','blue_image')

        self.hy0 = cv2.getTrackbarPos('HY0','yellow_image')
        self.sy0 = cv2.getTrackbarPos('SY0','yellow_image')
        self.vy0 = cv2.getTrackbarPos('VY0','yellow_image')
        self.hy1 = cv2.getTrackbarPos('HY1','yellow_image')
        self.sy1 = cv2.getTrackbarPos('SY1','yellow_image')
        self.vy1 = cv2.getTrackbarPos('VY1','yellow_image')

    def show_trackbars(self, color):
        def nothing(x):
            pass

        if color == "red":
            cv2.namedWindow('red_image')
            cv2.createTrackbar('HR0','red_image',0,180,nothing)
            cv2.createTrackbar('SR0','red_image',0,255,nothing)
            cv2.createTrackbar('VR0','red_image',0,255,nothing)
            cv2.createTrackbar('HR1','red_image',0,180,nothing)
            cv2.createTrackbar('SR1','red_image',0,255,nothing)
            cv2.createTrackbar('VR1','red_image',0,255,nothing)

            cv2.setTrackbarPos('HR0','red_image',TRACKBAR_RED[0])
            cv2.setTrackbarPos('SR0','red_image',TRACKBAR_RED[1])
            cv2.setTrackbarPos('VR0','red_image',TRACKBAR_RED[2])
            cv2.setTrackbarPos('HR1','red_image',TRACKBAR_RED[3])
            cv2.setTrackbarPos('SR1','red_image',TRACKBAR_RED[4])
            cv2.setTrackbarPos('VR1','red_image',TRACKBAR_RED[5])

            self.hr0 = cv2.getTrackbarPos('HR0','red_image')
            self.sr0 = cv2.getTrackbarPos('SR0','red_image')
            self.vr0 = cv2.getTrackbarPos('VR0','red_image')
            self.hr1 = cv2.getTrackbarPos('HR1','red_image')
            self.sr1 = cv2.getTrackbarPos('SR1','red_image')
            self.vr1 = cv2.getTrackbarPos('VR1','red_image')
         
        if color == "blue":
            cv2.namedWindow('blue_image')
            cv2.createTrackbar('HB0','blue_image',0,180,nothing)
            cv2.createTrackbar('SB0','blue_image',0,255,nothing)
            cv2.createTrackbar('VB0','blue_image',0,255,nothing)
            cv2.createTrackbar('HB1','blue_image',0,180,nothing)
            cv2.createTrackbar('SB1','blue_image',0,255,nothing)
            cv2.createTrackbar('VB1','blue_image',0,255,nothing)

            cv2.setTrackbarPos('HB0','blue_image',TRACKBAR_BLU[0])
            cv2.setTrackbarPos('SB0','blue_image',TRACKBAR_BLU[1])
            cv2.setTrackbarPos('VB0','blue_image',TRACKBAR_BLU[2])
            cv2.setTrackbarPos('HB1','blue_image',TRACKBAR_BLU[3])
            cv2.setTrackbarPos('SB1','blue_image',TRACKBAR_BLU[4])
            cv2.setTrackbarPos('VB1','blue_image',TRACKBAR_BLU[5])

            self.hb0 = cv2.getTrackbarPos('HB0','blue_image')
            self.sb0 = cv2.getTrackbarPos('SB0','blue_image')
            self.vb0 = cv2.getTrackbarPos('VB0','blue_image')
            self.hb1 = cv2.getTrackbarPos('HB1','blue_image')
            self.sb1 = cv2.getTrackbarPos('SB1','blue_image')
            self.vb1 = cv2.getTrackbarPos('VB1','blue_image')

        if color == "yellow":
            cv2.namedWindow('yellow_image')
            cv2.createTrackbar('HY0','yellow_image',0,180,nothing)
            cv2.createTrackbar('SY0','yellow_image',0,255,nothing)
            cv2.createTrackbar('VY0','yellow_image',0,255,nothing)
            cv2.createTrackbar('HY1','yellow_image',0,180,nothing)
            cv2.createTrackbar('SY1','yellow_image',0,255,nothing)
            cv2.createTrackbar('VY1','yellow_image',0,255,nothing)

            cv2.setTrackbarPos('HY0','yellow_image',TRACKBAR_YEL[0])
            cv2.setTrackbarPos('SY0','yellow_image',TRACKBAR_YEL[1])
            cv2.setTrackbarPos('VY0','yellow_image',TRACKBAR_YEL[2])
            cv2.setTrackbarPos('HY1','yellow_image',TRACKBAR_YEL[3])
            cv2.setTrackbarPos('SY1','yellow_image',TRACKBAR_YEL[4])
            cv2.setTrackbarPos('VY1','yellow_image',TRACKBAR_YEL[5])

            self.hy0 = cv2.getTrackbarPos('HY0','yellow_image')
            self.sy0 = cv2.getTrackbarPos('SY0','yellow_image')
            self.vy0 = cv2.getTrackbarPos('VY0','yellow_image')
            self.hy1 = cv2.getTrackbarPos('HY1','yellow_image')
            self.sy1 = cv2.getTrackbarPos('SY1','yellow_image')
            self.vy1 = cv2.getTrackbarPos('VY1','yellow_image')


if __name__ == '__main__':
    cur_app = KingfishApp()
