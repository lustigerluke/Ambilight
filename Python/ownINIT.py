#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
from AmbilightCam import *
import config
from UDP import send_UDP #own UDO functions
import argparse
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from PiVideoStream import PiVideoStream
	
	
	
def get_M(vs, cv2):
	
	lightUpEdges(vs, cv2)
	
	points = click_coordinates(vs, cv2) #get points by clicking the corners of the screen
	
	#TRANSFORM
	#four points from the original image
	pts1 = np.float32(points)
	#four points in the goal image
	pts2 = np.float32([[0,0],[config.HLED,0],[0,config.VLED],[config.HLED,config.VLED]])
	
	M = cv2.getPerspectiveTransform(pts1,pts2)
	
	# cleanup
	# cv2.destroyAllWindows()
		
	return M

def lightUpEdges(vs, cv2):
	startLED = 0
	endLED = config.VLED
	
	#set all LEDS to red
	send_UDP("a 255 000 000")
	time.sleep(1.0)
	
	for i in range(4):
		j = startLED

		print("taking image")
		image1 = vs.read()
		
		#turn on all leds of an edge
		while j < endLED:
			MESSAGE = "A" + str("%03d" % (j,)) + "R000G000B255"
			send_UDP(MESSAGE)
			j = j + 1
			
		time.sleep(1.0)
		image2 = vs.read()
		diffimage1 = cv2.absdiff(image2, image1)
		grayimage1 = cv2.cvtColor(diffimage1, cv2.COLOR_BGR2GRAY)
		retval, thresholdimage1 = cv2.threshold(grayimage1,config.THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)

		cv2.imshow(str("%03d" % (i,)), thresholdimage1)
		
		
		startLED = endLED
		if i%2 == 0:
			print("HLED")
			endLED = startLED + config.HLED
		else:
			print("VLED")
			endLED = startLED + config.VLED
		
