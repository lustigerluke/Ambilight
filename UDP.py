import socket
import time
import config

def send_UDP(MESSAGE):
	sock = socket.socket(socket.AF_INET, #Internet
	socket.SOCK_DGRAM) #UDP
	
	length_MESSAGE = len(MESSAGE)
	start = 0
	while length_MESSAGE > config.lengthOnePackage + start:
			MSG = MESSAGE[start:start+config.lengthOnePackage]
			sock.sendto(MSG,(config.UDP_IP,config.UDP_PORT))
			start = start + config.lengthOnePackage
			time.sleep(0.005) #give the message some time - TO BE REMOVED IF RECEIVE IS FAST ENOUGH
			
	if start + config.lengthOnePackage > length_MESSAGE:
			MSG = MESSAGE[start:length_MESSAGE]
			sock.sendto(MSG,(config.UDP_IP,config.UDP_PORT))
			time.sleep(0.005) #give the message some time - TO BE REMOVED IF RECEIVE IS FAST ENOUGH
			
	
