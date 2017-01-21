import time
import numpy as np
import cv2
from AmbilightCam import *

#find left points of screen
def get_lline(CAMERA_WIDTH, CAMERA_HEIGHT, grayimage1):
	
    print("processing left line")
    
    i = 0 #index of left borders
    left = []
    line = 0
    while line < CAMERA_HEIGHT:
        colomn = 0
        while colomn < len(grayimage1[0,:]):
            if (grayimage1.item(line,colomn) != 0) & (colomn < CAMERA_WIDTH) & (line < CAMERA_HEIGHT):
                left.append([ line,colomn])
                #print(left[i])
                i = i + 1
                break
              
            colomn = colomn + 1 #Increment colomn
            
        line = line + 1 #Increment line
        i = 0
        
    return left


        
#find right points of screen
def get_rline(CAMERA_WIDTH, CAMERA_HEIGHT, grayimage1):
	
	print("processing right line")

	j = 0 #index of right borders
	right = []
	line = 0
	while line < CAMERA_HEIGHT:
		colomn = CAMERA_WIDTH -1
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

#open window to get the screen corners by clicking them 
def click_coordinates(vs, cv2, dispW, dispH):

	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_event)   #callback-function for mouse pointer
	
	#while loop to get TV coordinates
	print("press r to reset points, press c to continue")
	global points
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
	print points
	return points

