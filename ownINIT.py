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


def find_led_spotpoints1(vs, cv2):
	delay = 0.2 #this parameter could give some hint to the overall delay time. 
	
	find_led_spotpoints1(vs, cv2)
	
	#some blinking in the biginning to test RGB
	print("BEGIN: show corner LEDs to find Screen" )
	
	send_UDP("a000 000 000") #make everything black
	time.sleep(delay)
	bground_image = vs.read()
	
	#lower left corner
	send_UDP("A%03dR255G000B000" %( 2*(config.VLED + config.HLED)))
	send_UDP("A%03dR255G000B000" %( 0))
	send_UDP("A%03dR255G000B000" %( 1))
	time.sleep(delay)
	ll_image = vs.read()

	#upper left corner
	send_UDP("A%03dR255G000B000" %( config.VLED -1))
	send_UDP("A%03dR255G000B000" %( config.VLED))
	send_UDP("A%03dR255G000B000" %( config.VLED +1))
	time.sleep(delay)
	ul_image = vs.read()
	
	#upper right corner
	send_UDP("A%03dR255G000B000" %( config.VLED + config.HLED -1))
	send_UDP("A%03dR255G000B000" %( config.VLED + config.HLED))
	send_UDP("A%03dR255G000B000" %( config.VLED + config.HLED +1))
	time.sleep(delay)
	ur_image = vs.read()
	
	#lower right corner
	send_UDP("A%03dR255G000B000" %( 2 * config.VLED + config.HLED -1))
	send_UDP("A%03dR255G000B000" %( 2 * config.VLED + config.HLED))
	send_UDP("A%03dR255G000B000" %( 2 * config.VLED + config.HLED +1))
	time.sleep(delay)
	lr_image = vs.read()
	
	send_UDP("a000 000 000") #make everything black
	time.sleep(delay)
	bground_image = vs.read()
	
	#lower right corner blue
	send_UDP("A%03dR000G000B255" %( 2 * config.VLED + config.HLED -1))
	send_UDP("A%03dR000G000B255" %( 2 * config.VLED + config.HLED))
	send_UDP("A%03dR000G000B255" %( 2 * config.VLED + config.HLED +1))
	time.sleep(delay)
	lr_b_image = vs.read()

	send_UDP("a000 000 000") #make everything black
	time.sleep(delay)
	bground_image = vs.read()
	
	#lower right corner blue
	send_UDP("A%03dR000G255B000" %( 2 * config.VLED + config.HLED -1))
	send_UDP("A%03dR000G255B000" %( 2 * config.VLED + config.HLED))
	send_UDP("A%03dR000G255B000" %( 2 * config.VLED + config.HLED +1))
	time.sleep(delay)
	lr_g_image = vs.read()

	

	
	
	image = cv2.absdiff(ll_image,bground_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("1",image)
	
	image = cv2.absdiff(ul_image,ll_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("2",image)
	
	image = cv2.absdiff(ur_image,ul_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("3",image)
	
	image = cv2.absdiff(lr_image,ur_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("4",image)
	r_image =image
	
	
	image = cv2.absdiff(lr_b_image,r_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("4r",image)
	
	image = cv2.absdiff(lr_g_image,r_image)
	image[:,:,0] = 0
	image[:,:,1] = 0
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray) #find area
	cv2.circle(image, maxLoc, 5, (0,255 , 0), 2) #add a circle at the coordinates to the image
	cv2.imshow("4g",image)
	
		


	points = []
	
	
	
	return points


def find_led_spotpoints(vs, cv2):
	
	delay = 0.2 #this parameter could give some hint to the overall delay time. 
	
	corners = [0, config.VLED, config.VLED + config.HLED, 2 * config.VLED + config.HLED ]
	corner_count = len(corners)
	
	colors = ['R255G000B000','R000G255B000','R000G000B255']
	color_count = len(colors)
	
	print("new way to find corners")
	
	color = 0
	while color < color_count:
		
		corner = 0
		while corner < corner_count:
			
			send_UDP("a000 000 000") #make everything black
			time.sleep(delay)
			bground_image = vs.read()
			
			send_UDP(''.join(["A%03d"%( corners[corner] + 1) + colors[color] ])) # what about corners[corner] = 0?
			send_UDP(''.join(["A%03d"%( corners[corner]) + colors[color] ]))
			send_UDP(''.join(["A%03d"%( corners[corner] - 1) + colors[color] ]))
			time.sleep(delay)
			image = vs.read()
			
			print("processed corner # %03d " %(corner))
			print(''.join(["A%03d"%( corners[corner]) + colors[color] ]))
			
			image = cv2.absdiff(image,bground_image)
			cv2.imshow(''.join(["A%03d"%( corners[corner]) + colors[color] ]),image)
			
			corner = corner + 1
		
		color = color +1
		
	
	
	
def get_M(vs, cv2):

	left = []
	right = []
	
	print("starting loop to find points")
	
	#while (len(left) < 4) & (len(right) < 4):
		#print("wait some tine before taking the next picture")
		#time.sleep(0.2)
		#image1 = vs.read()
		#time.sleep(0.2)
		#image2 = vs.read()

		#diffimage1 = cv2.absdiff(image2, image1)
		#retval, thresholdimage1 = cv2.threshold(diffimage1,config.THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
		#grayimage1 = cv2.cvtColor(thresholdimage1, cv2.COLOR_BGR2GRAY)
		
		## get points by calculating the corners
		#left = get_lline(grayimage1)
		#right = get_rline(grayimage1)		
		
		#cv2.imshow("th_bw_image", grayimage1)
		

	
	##print("got left and right line")
	##points = get_corners(left,right)
	
	points = find_led_spotpoints(vs, cv2)
	
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



def get_points(vs, cv2):
	
	image1 = vs.read()
	left = []
	right = []
	
	print("starting loop to find points")
	
	while (len(left) < config.HLED) & (len(right) < config.HLED):
		print("wait some tine before taking the next picture")
		time.sleep(2.5)
		image2 = vs.read()
		diffimage1 = cv2.absdiff(image2, image1)
		retval, thresholdimage1 = cv2.threshold(diffimage1,config.THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
		grayimage1 = cv2.cvtColor(thresholdimage1, cv2.COLOR_BGR2GRAY)
		
		# get points by calculating the corners
		left = get_lline(grayimage1)
		right = get_rline(grayimage1)		
		
		cv2.imshow("th_bw_image", grayimage1)
		
		image1 = image2

	
	print("passed init. got left and right line")
	
	points= get_corners(left,right)
	return points
	

#find left points of screen
def get_lline(grayimage1):
	
    print("processing left line")
    
    i = 0 #index of left borders
    left = []
    line = 0
    while line < config.CAMERA_HEIGHT:
        colomn = 0
        while colomn < len(grayimage1[0,:]):
            if (grayimage1.item(line,colomn) != 0) & (colomn < config.CAMERA_WIDTH) & (line < config.CAMERA_HEIGHT):
                left.append([ line,colomn])
                #print(left[i])
                i = i + 1
                break
              
            colomn = colomn + 1 #Increment colomn
            
        line = line + 1 #Increment line
        i = 0
        
    return left


        
#find right points of screen
def get_rline(grayimage1):
	
	print("processing right line")

	j = 0 #index of right borders
	right = []
	line = 0
	while line < config.CAMERA_HEIGHT:
		colomn = config.CAMERA_WIDTH -1
		while colomn > 0:
			if (grayimage1.item(line,colomn) != 0) & (colomn > 0) & (line > 0):
				right.append([line,colomn])
				j = j + 1
				break
            
			colomn = colomn - 1 #decrement colomn to find right points

		line = line + 1 #Increment line
		j = 0
        
	return right

#algorithm to find the corner points due to the given points of left and right screen points
def get_corners(left,right):
	#not only subtract the symmetric line
	# first get the standard deviation to get an idea of orientation
	# TO DO 
	
	#symmetric line
	line1 = []
	line2 = []
	
	# get parameters for symmetric line
	x1,y1 = left[0]
	x2,y2 = left[len(left)-1]
	#y = k * x + d
	k = float(x2-x1)/float(y2-y1)
	d = y1 - float((x2-x1)*x1)/float(y2-y1)
	
	print("symmetric data")
	print("k: " + str(k))
	print("d: " + str(d))
	#calculate left line
	
	
	# calculate the triangles around the symmetric line
	i = 0
	while i < len(left):
		xline,yline = left[i]
		line1.append(yline - (k * float(xline) + d))
		i = i + 1
		
	#calculate right line
	i = 0
	while i < len(right):
		xline,yline = right[i]
		line2.append(yline - (k * float(xline) + d))
		i = i + 1
		
	# get coordinates in right order for prototype
	# TO DO: find algorithm to do this automaticaly
	coord_list = []
	coord_list.append(left[line1.index(min(line1))])
	coord_list.append(left[0])
	coord_list.append(left[len(left)-1])
	coord_list.append(right[line2.index(max(line2))])
	
	print("coordinates: " , coord_list)

	left = []
	right = []

	#rotate x and y coordinates in coord_list
	i = 0
	while i < len(coord_list):
		coord_list[i].reverse()
		i = i + 1
	
	points = np.float32(coord_list)
	return coord_list



