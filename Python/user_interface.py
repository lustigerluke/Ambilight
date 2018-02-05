import time
import numpy as np
import cv2
from AmbilightCam import *
import config

	
#open window to get the screen corners by clicking them 
def click_coordinates(vs, cv2):
	
	
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_event)   #callback-function for mouse pointer
	
	#while loop to get TV coordinates
	print("press r to reset points, press c to continue")
	global points
	points = []
	
	while True:
		# display the image and wait for a keypress
		image2 = vs.read()
		image2= cv2.resize( image2,( config.dispW, config.dispH ))
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
	cv2.destroyWindow("image")

	return points


def click_event(event, x_click, y_click, flags, param):
	# grab references to the global variables

	global click
	global x,y
	global points
	
	x = x_click
	y = y_click
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates 
	if event == cv2.EVENT_LBUTTONDOWN :
			x = ((x * 10000) * config.CAMERA_WIDTH / config.dispW ) / 10000
			y = ((y * 10000) * config.CAMERA_HEIGHT / config.dispH ) / 10000
			refPt = [(x , y)]
			points.append(refPt)
			print(points)
			#print(len(points))

	if event == cv2.EVENT_RBUTTONDOWN :
		print("x: " + str(x) + ", y: " + str(y) + ";")
		#print("R: " + str(image2[x][y]) + ", G: " + str(image2[x][y][1]) + ", G: " + str(image2[x][y][2]))
		print()
		click = 1
