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
from createMessage import *
import config


##PARAMETER ######################################################################################

# Display Settings
debug = True        # Set to False for no data display
window_on =  True    # Set to True displays opencv windows (GUI desktop reqd)


    
CAMERA_HFLIP = False
CAMERA_VFLIP = False
CAMERA_ROTATION=0
CAMERA_FRAMERATE = 60 #90


FRAME_COUNTER = 100

#initialize points
points = [] #list of clicked points

old_r = {}
old_g = {}
old_b = {}
old = [old_r, old_g, old_b]

stats_l = 0 
stats_o = 0
stats_r = 0 
stats_u = 0
stats = [stats_l, stats_o, stats_l, stats_u]

THRESHOLD = 50


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
	global stats
	global old
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
	#vs.camera.sharpness = 0
	#vs.camera.contrast = 0	
	#vs.camera.brightness = 50
	#vs.camera.saturation = 0
	#vs.camera.ISO = 0
	#vs.camera.video_stabilization = False
	#vs.camera.exposure_compensation = 0
	#vs.camera.exposure_mode = 'auto'
	#vs.camera.meter_mode = 'average'
	#vs.camera.awb_mode = 'auto'
	#vs.camera.image_effect = 'none'
	#vs.camera.color_effects = None
	#vs.camera.crop = (0.0, 0.0, 1.0, 1.0)
		
	frame_count = 0
	start_time = time.time()
	still_scanning = True
	
	#TO DO: find the fastest way to initialize the camera
	time.sleep(1.0) #time for camera to initialize


	M = get_M(vs,cv2) #get transformation matrix
	
	
	if window_on:
		print("press q to quit opencv display")
	else:
		print("press ctrl-c to quit")
	

	
	#initalize the mouse callback for the image
	#to do ... some scaling for the window or another callback or rule or something
	cv2.namedWindow("TVimage")
	cv2.setMouseCallback("TVimage", click_event) 
		
	#LOOP-------------------------------------------------------------------------------------------
	while still_scanning:
		
		image2 = vs.read()		
		
		if (click == True):
			print(x)
			print(y)
			print(image2.item(x,y,0))
			print(image2[0,0])
			#print("R: " + str(image2[x][y]) + ", G: " + str(image2[x][y][1]) + ", G: " + str(image2[x][y][2]))
			click = False
			
		#call function to generate fps output
		start_time, frame_count, stats = show_STATUS(start_time, frame_count,stats)
		
		#transform image with the generated transformation matrix M
		dst = cv2.warpPerspective(image2,M,(config.HLED,config.VLED))
		
		#find some way to get good RGB values and process the little image because it is faster to process small images ;)
		#dst = cv2.cvtColor(dst,   cv2.COLOR_HSV2RBG) #color transformation CV_HSV2BGR , cv2.COLOR_XYZ2BGR
		
		#create UDP Message
		MESSAGE, stats, old = create_Message(dst,stats,old)
		
		#send the MESSAGE
		send_UDP(MESSAGE)
	
	
		if window_on:
			dst = cv2.resize( dst,( config.CAMERA_WIDTH, config.CAMERA_HEIGHT ))
			cv2.imshow('TVimage', dst)
			
			# Close Window if q pressed while movement status window selected
			if cv2.waitKey(1) & 0xFF == ord('q'):
				#cv2.destroyAllWindows()
				print("End Motion Tracking")
				still_scanning = False
		
			if cv2.waitKey(1) & 0xFF == ord('i'):
				print("new init-process")
				cv2.destroyAllWindows()
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



