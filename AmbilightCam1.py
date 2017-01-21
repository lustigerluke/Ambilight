#!/usr/bin/env python
# -*- coding: utf-8 -*-


progname = "AmbilightCam.py"
ver = "version 0.95"

"""
motion-track ver 0.95 written by Claude Pageau pageauc@gmail.com
Raspberry (Pi) - python opencv2 motion tracking using picamera module

This is a raspberry pi python opencv2 motion tracking demonstration program.
It will detect motion in the field of view and use opencv to calculate the
largest contour and return its x,y coordinate.  I will be using this for
a simple RPI robotics project, but thought the code would be useful for 
other users as a starting point for a project.  I did quite a bit of 
searching on the internet, github, etc but could not find a similar
implementation that returns x,y coordinates of the most dominate moving 
object in the frame.  Some of this code is base on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Here is a my YouTube video demonstrating this demo program using a 
Raspberry Pi B2 https://youtu.be/09JS7twPBsQ

Requires a Raspberry Pi with a RPI camera module installed and configured
dependencies

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv python-picamera
sudo apt-get install libgl1-mesa-dri  

"""
print("%s %s using python2 and OpenCV2" % (progname, ver))
print("Loading Please Wait ....")
# import the necessary packages
import io
import time
#import argparse
import cv2
import socket
import numpy as np
import matplotlib.pyplot as plt

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from PiVideoStream import PiVideoStream

from ownINIT import get_lline
from ownINIT import get_rline
from ownINIT import get_corners
from UDP import send_UDP #own UDO functions

##PARAMETER ######################################################################################
HLED = 30	#number of horizontal LEDs
VLED = 18	#number of vertical LEDs

dispW = 720   #display width to calibrate coordinats
dispH = 480   #display height to calibrate coordinats
# Display Settings
debug = True        # Set to False for no data display
window_on =  True    # Set to True displays opencv windows (GUI desktop reqd)
SHOW_CIRCLE = True  # show a circle otherwise show bounding rectancle on window
CIRCLE_SIZE = 8     # diameter of circle to show motion location in window
LINE_THICKNESS = 1  # thickness of bounding line in pixels
WINDOW_BIGGER = 1   # Resize multiplier for Movement Status Window
                    # if gui_window_on=True then makes opencv window bigger
                    # Note if the window is larger than 1 then a reduced frame rate will occur            

# Camera Settings
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240  # 240
big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER)      
CAMERA_HFLIP = False
CAMERA_VFLIP = False
CAMERA_ROTATION=0
CAMERA_FRAMERATE = 60 #90


FRAME_COUNTER = 100

global x
global y
global click
click = False

#initialize points
refPt = []  #clicked point
points = [] #list of points

# UDP settings
UDP_IP = "192.168.0.103"
UDP_PORT = 2390        
lengthOnePackage = 480 #<500

# LED settings
LED_COUNT = 97


#-----------------------------------------------------------------------------------------------  
def show_FPS(start_time,frame_count):
    if debug:
        if frame_count >= FRAME_COUNTER:
            duration = float(time.time() - start_time)
            FPS = float(frame_count / duration)
            print("Processing at %.2f fps last %i frames" %( FPS, frame_count))
            frame_count = 0
            start_time = time.time()
        else:
            frame_count += 1
    return start_time, frame_count

#-----------------------------------------------------------------------------------------------  
def click_event(event, x_click, y_click, flags, param):
        # grab references to the global variables
        global refPt
        global points
        global click
        global x,y
        x = x_click
        y = y_click



        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates 
        if event == cv2.EVENT_LBUTTONDOWN :
                x = ((x * 10000) * CAMERA_WIDTH / dispW ) / 10000
                y = ((y * 10000) * CAMERA_HEIGHT / dispH ) / 10000
                refPt = [(x , y)]
                points.append(refPt)
                print(points)
                #print(len(points))

        if event == cv2.EVENT_RBUTTONDOWN :
            print("x: " + str(x) + ", y: " + str(y) + ";")
            #print("R: " + str(image2[x][y]) + ", G: " + str(image2[x][y][1]) + ", G: " + str(image2[x][y][2]))
            print()
            click = 1
        

                
def Ambilight():
    
    global points
    global x,y
    global click
    
    print("Initializing Camera ....")
    # Save images to an in-program stream
    # Setup video stream on a processor Thread for faster speed
    #vs = PiVideoStream().__init__(self, resolution=(CAMERA_WIDTH , CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False)
    vs = PiVideoStream(CAMERA_WIDTH, CAMERA_HEIGHT,CAMERA_FRAMERATE, 0 ,0, 0)
    vs.start()
    vs.camera.rotation = CAMERA_ROTATION
    vs.camera.hflip = CAMERA_HFLIP
    vs.camera.vflip = CAMERA_VFLIP
    time.sleep(1)    

        

    cx = 0
    cy = 0
    cw = 0
    ch = 0
    frame_count = 0
    start_time = time.time()
    still_scanning = True


    #INIT

    THRESHOLD_SENSITIVITY = 100 #seems to be a good guess for most situations
    #some blinking in the biginning to test RGB
    send_UDP("a255 000 000",UDP_IP,UDP_PORT,lengthOnePackage)
    print("red")
	
    sock = socket.socket(socket.AF_INET, #Internet
    socket.SOCK_DGRAM) #UDP
    MSG="a0 0 255"
    sock.sendto(MSG,(UDP_IP,UDP_PORT))
    time.sleep(1)

    #Get two images with a delay of 0.5s to find screen
    image1 = vs.read()
    time.sleep(2.5)     #wait some time fore message to be processed on receiving end
    global image2
    image2 = vs.read()
    diffimage1 = cv2.absdiff(image2, image1)    #Difference of the two images
    # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
    retval, thresholdimage1 = cv2.threshold(diffimage1,THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
    # Convert to gray scale, which is easier
    grayimage1 = cv2.cvtColor(thresholdimage1, cv2.COLOR_BGR2GRAY)
    cv2.imshow("th_bw_image", grayimage1)   #plot black/white result of thresholded image difference
    



    left = get_lline(big_w,big_h,grayimage1)

    right = get_rline(big_w,big_h,grayimage1)
    
    coord_list = get_corners(left,right)

    prev_time = time.time()
    time.sleep(0.01)
    print(time.time() - prev_time)

    

    

    #find algorithm to find corners


    #points = np.float32(left)
    # mow borders should contain the left border
    #left_border = cv2.fitLine(left,1, 0, 0.01, 0.01)


    points = []

        
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_event)   #callback-function for mouse pointer

        
    #while loop to get TV coordinates
    print("press r to reset points, press c to continue")
    while True:
        # display the image and wait for a keypress
        image2 = vs.read()
        image2= cv2.resize( image2,( dispW, dispH ))
        cv2.imshow("image", image2)
        
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset 
        if key == ord("r"):
            cv2.destroyAllWindows()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_event)   #callback-function for mouse pointer
            points = []
            print("points cleared")

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            cv2.destroyAllWindows()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_event)   #callback-function for mouse pointer
            break
            
    # close all open windows
    cv2.destroyWindow("coordinates_image")


    
    #TRANSFORM
    #four points from the original image
    pts1 = np.float32(points)
    #four points in the goal image
    pts2 = np.float32([[0,0],[HLED,0],[0,VLED],[HLED,VLED]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)

    if window_on:
        print("press q to quit opencv display")
    else:
        print("press ctrl-c to quit")

    old_r = {}
    old_g = {}
    old_b = {}
    led_count = VLED*2+HLED*2
    
    stats_l = 0 
    stats_o = 0
    stats_r = 0
    stats_u = 0

    THRESHOLD = 50

    MSG_COUNT = 0

    DATA_COUNT = 0

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_event) 
        
    #LOOP-------------------------------------------------------------------------------------------
    while still_scanning:

        #read image
        image2 = vs.read()
        cv2.imshow("image", image2)
        
        meanVec = cv2.mean(image2)
        
        if (click == True):
            print(x)
            print(y)
            print(image2.item(x,y,0))
            print(image2[0,0])
            #print("R: " + str(image2[x][y]) + ", G: " + str(image2[x][y][1]) + ", G: " + str(image2[x][y][2]))
            click = False
            
        #call function to generate fps output
        start_time, frame_count = show_FPS(start_time, frame_count)

        dst = cv2.warpPerspective(image2,M,(HLED,VLED))
        #dst = cv2.cvtColor(dst,   cv2.COLOR_HSV2RBG) #color transformation CV_HSV2BGR , cv2.COLOR_XYZ2BGR

        ##create a line vector with BGR values in it
        #      first row , last colomn  , last row flipped         , first colomn flipped

        MESSAGE2 = "a255 255 255"

        adr = 0
        MESSAGE = ""
        MSG1 = ""
        MSG2 = ""
        MSG3 = ""
        MSG4 = ""

        if (stats_l > 1000):
            print ("stats l " + str(stats_l))
            print(meanVec)
            stats_l = 0

        if (stats_o > 1000):
            print ("stats o " + str(stats_o))
            stats_o = 0
        if (stats_r > 1000):
            print ("stats r " + str(stats_r))
            stats_r = 0
        if (stats_u > 1000):
            print ("stats u " + str(stats_u))
            stats_u = 0

        

        while adr < VLED :
            #assume if red is set others are as well
            if (adr in old_r):                
                if (abs((int(old_r[adr]) - int(dst[(VLED-adr)-1,0,2]))) < THRESHOLD) and (abs((int(old_g[adr]) - int(dst[(VLED-adr)-1,0,1]))) < THRESHOLD) and (abs((int(old_b[adr]) - int(dst[(VLED-adr)-1,0,0]))) < THRESHOLD):
                    #print ("PASS")
                    stats_l = stats_l +1
                    #pass
                else:
                    MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[(VLED-adr)-1,0,2])) + "G" + str("%03d" % (dst[(VLED-adr)-1,0,1])) + "B" + str("%03d" % (dst[(VLED-adr)-1,0,0]))    
            old_r[adr]= (dst[(VLED-adr)-1,0,2])
            old_g[adr]= (dst[(VLED-adr)-1,0,1])
            old_b[adr]= (dst[(VLED-adr)-1,0,0])
            adr = adr + 1;

        #18
        while adr < HLED + VLED:
            #assume if red is set others are as well
            if (adr in old_r):                
                if (abs((int(old_r[adr]) - int(dst[0,adr-VLED,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[0,adr-VLED,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[0,adr-VLED,0]))) < THRESHOLD):
                    #print ("PASS")
                    stats_o = stats_o +1
                    #pass
                else:
                    MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[0,adr-VLED,2],)) + "G" + str("%03d" % (dst[0,adr-VLED,1],)) + "B" + str("%03d" % (dst[0,adr-VLED,0],))
            old_r[adr]= (dst[0,adr-VLED,2])
            old_g[adr]= (dst[0,adr-VLED,1])
            old_b[adr]= (dst[0,adr-VLED,0])
            adr = adr + 1;
        #48
        while adr < HLED + 2 * VLED:
            #assume if red is set others are as well
            if (adr in old_r):                
                if (abs((int(old_r[adr]) - int(dst[adr-VLED-HLED,HLED-1,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[adr-VLED-HLED,HLED-1,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[adr-VLED-HLED,HLED-1,0]))) < THRESHOLD):
                    #print ("PASS")
                    stats_r = stats_r +1
                    #pass
                else:
                    MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[adr-VLED-HLED,HLED-1,2],)) + "G" + str("%03d" % (dst[adr-VLED-HLED,HLED-1,1],)) + "B" + str("%03d" % (dst[adr-VLED-HLED,HLED-1,0],))
            old_r[adr]= (dst[adr-VLED-HLED,HLED-1,2])
            old_g[adr]= (dst[adr-VLED-HLED,HLED-1,1])
            old_b[adr]= (dst[adr-VLED-HLED,HLED-1,0])
            adr = adr + 1;

        #66
        while adr < 2 * HLED + 2 * VLED :
            xhelp = HLED-(adr-HLED-2*VLED)-1 #caöculate a help value

            #assume if red is set others are as well
            if (adr in old_r):                
                if (abs((int(old_r[adr]) - int(dst[VLED-1,xhelp,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[VLED-1,xhelp,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[VLED-1,xhelp,0]))) < THRESHOLD):
                
                    stats_u = stats_u +1
                    #pass
                else:                    
                    MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[VLED-1,xhelp,2],)) + "G" + str("%03d" % (dst[VLED-1,xhelp,1],)) + "B" + str("%03d" % (dst[VLED-1,xhelp,0],))
            old_r[adr]= (dst[VLED-1,xhelp,2])
            old_g[adr]= (dst[VLED-1,xhelp,1])
            old_b[adr]= (dst[VLED-1,xhelp,0])
            adr = adr + 1;
        


        
        
        length_MESSAGE = len(MESSAGE)

        DATA_COUNT = DATA_COUNT + len(MESSAGE)
        send_UDP(MESSAGE,UDP_IP,UDP_PORT,lengthOnePackage)

        #print every 100th msg len for debug
        MSG_COUNT = MSG_COUNT + 1
        if (MSG_COUNT > 100):
            print("message length " + str(length_MESSAGE))
            print ("sent: "+str(DATA_COUNT))
            MSG_COUNT = 0


 
        if window_on:
            dst = cv2.resize( dst,( big_w, big_h ))
            cv2.imshow('Movement Status  (Press q in Window to Quit)', dst)
            
            # Close Window if q pressed while movement status window selected
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print("End Motion Tracking")
                still_scanning = False

##MAIN ######################################################################################  
if __name__ == '__main__':
    try:
        Ambilight()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")                                



