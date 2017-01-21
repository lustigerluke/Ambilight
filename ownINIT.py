import time
import numpy as np
    
def get_lline(big_w, big_h, grayimage1):
    print("processing left line")
    i = 0 #index of left borders
    left = []
    line = 0
    while line < big_h:
        colomn = 0
        while colomn < len(grayimage1[0,:]):
            if (grayimage1.item(line,colomn) != 0) & (colomn < big_w) & (line < big_h):
                left.append([ line,colomn])
                #print(left[i])
                i = i + 1
                break
              
            colomn = colomn + 1 #Increment colomn
            
        line = line + 1 #Increment line
        i = 0
        
    return left


        
    #find right points
def get_rline(big_w, big_h, grayimage1):
	
	print("processing right line")

	j = 0 #index of right borders
	right = []
	line = 0
	while line < big_h:
		colomn = big_w -1
		while colomn > 0:
			if (grayimage1.item(line,colomn) != 0) & (colomn > 0) & (line > 0):
				right.append([line,colomn])
				j = j + 1
				break
            
			colomn = colomn - 1

		line = line + 1 #Increment line
		j = 0
        
	return right

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
