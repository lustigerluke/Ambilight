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

from ownINIT import *
from UDP import send_UDP #own UDO functions
from user_interface import *
import config

##PARAMETER ######################################################################################

# Display Settings
debug = True        # Set to False for no data display
window_on =  True    # Set to True displays opencv windows (GUI desktop reqd)


    
CAMERA_HFLIP = False
CAMERA_VFLIP = False
CAMERA_ROTATION=0
CAMERA_FRAMERATE = 60 #90
THRESHOLD_SENSITIVITY = 100 #seems to be a good guess for most situations


FRAME_COUNTER = 100

#initialize points
points = [] #list of clicked points

# UDP settings
UDP_IP = "192.168.0.103"
UDP_PORT = 2390        
lengthOnePackage = 480 #<500

# LED settings
LED_COUNT = 97

#TO DO : rename the Function and add a parameter status.
#			#status is a list of 4 elements containing so called status_l status_o status_r status_u
#			#rewrite the code below ;)

def show_STATUS(start_time,frame_count,stats):
	if frame_count >= FRAME_COUNTER:
		duration = float(time.time() - start_time)
		FPS = float(frame_count / duration)
		print("Processing at %.2f fps last %i frames" %( FPS, frame_count))
		print("stats: %.0f , %.0f , %.0f , %.0f " %(stats[0],stats[1],stats[2],stats[3]))
		stats = [0,0,0,0]
		frame_count = 0
		start_time = time.time()
	else:
		frame_count += 1
	return start_time, frame_count, stats


	

        

                
def Ambilight():
	
	global x,y
	global click
	click = 0
	
	print("Initializing Camera ....")
	# Save images to an in-program stream
	# Setup video stream on a processor Thread for faster speed
	#vs = PiVideoStream().__init__(self, resolution=(config.CAMERA_WIDTH , config.CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False)
	vs = PiVideoStream(config.CAMERA_WIDTH, config.CAMERA_HEIGHT,CAMERA_FRAMERATE, 0 ,0, 0)
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
	
	#some blinking in the biginning to test RGB
	send_UDP("a255 000 000",UDP_IP,UDP_PORT,lengthOnePackage)
	time.sleep(0.2)
	send_UDP("a000 255 000",UDP_IP,UDP_PORT,lengthOnePackage)
	time.sleep(0.2)
	send_UDP("a255 000 255",UDP_IP,UDP_PORT,lengthOnePackage)
	

	M = get_M(vs,cv2) #get transformation matrix
	
	
	if window_on:
		print("press q to quit opencv display")
	else:
		print("press ctrl-c to quit")
	
	old_r = {}
	old_g = {}
	old_b = {}
	led_count = config.VLED*2+config.HLED*2
	
	stats_l = 0 
	stats_o = 0
	stats_r = 0
	stats_u = 0
	stats = [stats_l, stats_o, stats_l, stats_u]
	
	THRESHOLD = 50
	
	MSG_COUNT = 0
	
	DATA_COUNT = 0
	
	#initalize the mouse callback for the image
	#to do ... some scaling for the window or another callback or rule or something
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
		start_time, frame_count, stats = show_STATUS(start_time, frame_count,stats)
	
		dst = cv2.warpPerspective(image2,M,(config.HLED,config.VLED))
		#dst = cv2.cvtColor(dst,   cv2.COLOR_HSV2RBG) #color transformation CV_HSV2BGR , cv2.COLOR_XYZ2BGR
	
	
		adr = 0
		MESSAGE = ""
		
		
		while adr < config.VLED :
			#assume if red is set others are as well
			if (adr in old_r):                
				if (abs((int(old_r[adr]) - int(dst[(config.VLED-adr)-1,0,2]))) < THRESHOLD) and (abs((int(old_g[adr]) - int(dst[(config.VLED-adr)-1,0,1]))) < THRESHOLD) and (abs((int(old_b[adr]) - int(dst[(config.VLED-adr)-1,0,0]))) < THRESHOLD):
					stats[0] = stats[0] + 1
				else:
					MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[(config.VLED-adr)-1,0,2])) + "G" + str("%03d" % (dst[(config.VLED-adr)-1,0,1])) + "B" + str("%03d" % (dst[(config.VLED-adr)-1,0,0]))    
			old_r[adr]= (dst[(config.VLED-adr)-1,0,2])
			old_g[adr]= (dst[(config.VLED-adr)-1,0,1])
			old_b[adr]= (dst[(config.VLED-adr)-1,0,0])
			adr = adr + 1;
	
		#18
		while adr < config.HLED + config.VLED:
			#assume if red is set others are as well
			if (adr in old_r):                
				if (abs((int(old_r[adr]) - int(dst[0,adr-config.VLED,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[0,adr-config.VLED,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[0,adr-config.VLED,0]))) < THRESHOLD):
					stats[1] = stats[1] + 1
				else:
					MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[0,adr-config.VLED,2],)) + "G" + str("%03d" % (dst[0,adr-config.VLED,1],)) + "B" + str("%03d" % (dst[0,adr-config.VLED,0],))
			old_r[adr]= (dst[0,adr-config.VLED,2])
			old_g[adr]= (dst[0,adr-config.VLED,1])
			old_b[adr]= (dst[0,adr-config.VLED,0])
			adr = adr + 1;
		#48
		while adr < config.HLED + 2 * config.VLED:
			#assume if red is set others are as well
			if (adr in old_r):                
				if (abs((int(old_r[adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,0]))) < THRESHOLD):
					stats[2] = stats[2] + 1
				else:
					MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,2],)) + "G" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,1],)) + "B" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,0],))
			old_r[adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,2])
			old_g[adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,1])
			old_b[adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,0])
			adr = adr + 1;
	
		#66
		while adr < 2 * config.HLED + 2 * config.VLED :
			xhelp = config.HLED-(adr-config.HLED-2*config.VLED)-1 #caöculate a help value
	
			#assume if red is set others are as well
			if (adr in old_r):                
				if (abs((int(old_r[adr]) - int(dst[config.VLED-1,xhelp,2]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[config.VLED-1,xhelp,1]))) < THRESHOLD) and (abs((int(old_r[adr]) - int(dst[config.VLED-1,xhelp,0]))) < THRESHOLD):
					stats[3] = stats[3] + 1
				else:                    
					MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[config.VLED-1,xhelp,2],)) + "G" + str("%03d" % (dst[config.VLED-1,xhelp,1],)) + "B" + str("%03d" % (dst[config.VLED-1,xhelp,0],))
			old_r[adr]= (dst[config.VLED-1,xhelp,2])
			old_g[adr]= (dst[config.VLED-1,xhelp,1])
			old_b[adr]= (dst[config.VLED-1,xhelp,0])
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
			dst = cv2.resize( dst,( config.CAMERA_WIDTH, config.CAMERA_HEIGHT ))
			cv2.imshow('image', dst)
			
			# Close Window if q pressed while movement status window selected
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				print("End Motion Tracking")
				still_scanning = False
		
			if cv2.waitKey(1) & 0xFF == ord('i'):
				cv2.destroyAllWindows()
				print("End Motion Tracking")
				M = get_M(vs,cv2) #get new transformation Matrix
				

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



