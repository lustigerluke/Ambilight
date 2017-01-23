import time
import numpy as np
import cv2
from AmbilightCam import *
import config


def get_M(vs, cv2):
	image1 = vs.read()
	left = []
	right = []
	
	print("starting loop to find points")
	
	while (len(left) < 4) & (len(right) < 4):
		print("wait some tine before taking the next picture")
		time.sleep(1)
		image2 = vs.read()
		diffimage1 = cv2.absdiff(image2, image1)
		retval, thresholdimage1 = cv2.threshold(diffimage1,THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
		grayimage1 = cv2.cvtColor(thresholdimage1, cv2.COLOR_BGR2GRAY)
		
		# get points by calculating the corners
		left = get_lline(grayimage1)
		right = get_rline(grayimage1)		
		
		cv2.imshow("th_bw_image", grayimage1)
		
		image1 = image2
		print("another init loop needed")
	
	print("got left and right line")
	
	points= get_corners(left,right)
	
	
	#points = click_coordinates(vs, cv2) #get points by clicking the corners of the screen
	
	
	
	#TRANSFORM
	#four points from the original image
	pts1 = np.float32(points)
	#four points in the goal image
	pts2 = np.float32([[0,0],[config.HLED,0],[0,config.VLED],[config.HLED,config.VLED]])
	
	M = cv2.getPerspectiveTransform(pts1,pts2)
		
	return M



def get_points(vs, cv2):
	
	image1 = vs.read()
	left = []
	right = []
	
	print("starting loop to find points")
	
	while (len(left) < 4) & (len(right) < 4):
		print("wait some tine before taking the next picture")
		time.sleep(2.5)
		image2 = vs.read()
		diffimage1 = cv2.absdiff(image2, image1)
		retval, thresholdimage1 = cv2.threshold(diffimage1,THRESHOLD_SENSITIVITY,255,cv2.THRESH_BINARY)
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

	x1,y1 = left[0]
	x2,y2 = left[len(left)-1]
	#y = k * x + d
	k = float(x2-x1)/float(y2-y1)
	d = y1 - float((x2-x1)*x1)/float(y2-y1)
	
	print("symmetric data")
	print("k: " + str(k))
	print("d: " + str(d))
	#calculate left line
	
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
		
	coord_list = []
	print("1st coordinate")
	print(left[line1.index(min(line1))])
	coord_list.append(left[line1.index(min(line1))])
	x1,y1 = left[line1.index(min(line1))]
	
	print("3rd coordinate")
	print(left[0])
	coord_list.append(left[0])
	x3,y3 = left[0]

	print("4th coordinate")
	print(left[len(left)-1])
	coord_list.append(left[len(left)-1])
	x4,y4 = left[len(left)-1]
		
	print("2nd coordinate")
	print(right[line2.index(max(line2))])
	coord_list.append(right[line2.index(max(line2))])
	x2,y2 = right[line2.index(max(line2))]    

	left = []
	right = []

	#rotate x and y coordinates in coord_list
	i = 0
	while i < len(coord_list):
		coord_list[i].reverse()
		i = i + 1
	
	print()
	print("corner points")
	print(coord_list)
	points = np.float32(coord_list)
	
	return coord_list



