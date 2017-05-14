#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
import cv2
from AmbilightCam import *
import config
		
def create_Message(dst, stats, old):
	
	THRESHOLD = 50
		
	
	adr = 0
	MESSAGE = ""
	
	while adr < config.VLED :
		#assume if red is set others are as well
		if (adr in old[0]):                
			if (abs((int(old[0][adr]) - int(dst[(config.VLED-adr)-1,0,2]))) < THRESHOLD) and (abs((int(old[2][adr]) - int(dst[(config.VLED-adr)-1,0,1]))) < THRESHOLD) and (abs((int(old[2][adr]) - int(dst[(config.VLED-adr)-1,0,0]))) < THRESHOLD):
				stats[0] = stats[0] + 1
			else:
				MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[(config.VLED-adr)-1,0,2])) + "G" + str("%03d" % (dst[(config.VLED-adr)-1,0,1])) + "B" + str("%03d" % (dst[(config.VLED-adr)-1,0,0]))    
		old[0][adr]= (dst[(config.VLED-adr)-1,0,2])
		old[2][adr]= (dst[(config.VLED-adr)-1,0,1])
		old[2][adr]= (dst[(config.VLED-adr)-1,0,0])
		adr = adr + 1;

	#18
	while adr < config.HLED + config.VLED:
		#assume if red is set others are as well
		if (adr in old[0]):                
			if (abs((int(old[0][adr]) - int(dst[0,adr-config.VLED,2]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[0,adr-config.VLED,1]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[0,adr-config.VLED,0]))) < THRESHOLD):
				stats[1] = stats[1] + 1
			else:
				MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[0,adr-config.VLED,2],)) + "G" + str("%03d" % (dst[0,adr-config.VLED,1],)) + "B" + str("%03d" % (dst[0,adr-config.VLED,0],))
		old[0][adr]= (dst[0,adr-config.VLED,2])
		old[2][adr]= (dst[0,adr-config.VLED,1])
		old[2][adr]= (dst[0,adr-config.VLED,0])
		adr = adr + 1;
	#48
	while adr < config.HLED + 2 * config.VLED:
		#assume if red is set others are as well
		if (adr in old[0]):                
			if (abs((int(old[0][adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,2]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,1]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[adr-config.VLED-config.HLED,config.HLED-1,0]))) < THRESHOLD):
				stats[2] = stats[2] + 1
			else:
				MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,2],)) + "G" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,1],)) + "B" + str("%03d" % (dst[adr-config.VLED-config.HLED,config.HLED-1,0],))
		old[0][adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,2])
		old[2][adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,1])
		old[2][adr]= (dst[adr-config.VLED-config.HLED,config.HLED-1,0])
		adr = adr + 1;

	#66
	while adr < 2 * config.HLED + 2 * config.VLED :
		xhelp = config.HLED - (adr - config.HLED - 2 * config.VLED ) - 1  #caöculate a help value

		#assume if red is set others are as well
		if (adr in old[0]):                
			if (abs((int(old[0][adr]) - int(dst[config.VLED-1,xhelp,2]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[config.VLED-1,xhelp,1]))) < THRESHOLD) and (abs((int(old[0][adr]) - int(dst[config.VLED-1,xhelp,0]))) < THRESHOLD):
				stats[3] = stats[3] + 1
			else:                    
				MESSAGE = MESSAGE + "A" + str("%03d" % (adr,)) + "R" + str("%03d" % (dst[config.VLED-1,xhelp,2],)) + "G" + str("%03d" % (dst[config.VLED-1,xhelp,1],)) + "B" + str("%03d" % (dst[config.VLED-1,xhelp,0],))
		old[0][adr]= (dst[config.VLED-1,xhelp,2])
		old[2][adr]= (dst[config.VLED-1,xhelp,1])
		old[2][adr]= (dst[config.VLED-1,xhelp,0])
		adr = adr + 1;
	
	return MESSAGE, stats, old
