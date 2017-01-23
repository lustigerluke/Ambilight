import socket
import time
import config

def send_UDP(MESSAGE,UDP_IP,UDP_PORT,lengthOnePackage):
	sock = socket.socket(socket.AF_INET, #Internet
	socket.SOCK_DGRAM) #UDP
	
	length_MESSAGE = len(MESSAGE)
	start = 0
	while length_MESSAGE > lengthOnePackage + start:
			MSG = MESSAGE[start:start+lengthOnePackage]
			sock.sendto(MSG,(UDP_IP,UDP_PORT))
			start = start + lengthOnePackage
			time.sleep(0.005) #give the message some time - TO BE REMOVED IF RECEIVE IS FAST ENOUGH
			
	if start + lengthOnePackage > length_MESSAGE:
			MSG = MESSAGE[start:length_MESSAGE]
			sock.sendto(MSG,(UDP_IP,UDP_PORT))
			time.sleep(0.005) #give the message some time - TO BE REMOVED IF RECEIVE IS FAST ENOUGH
			
	
