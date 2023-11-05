#This is the UDP server that the first user to enter a room is going to create 
#with the purpose of video streaming, this design may have to be changed since the goal is have 
#all users be able to manipulare the video 

import cv2, imutils, socket
import numpy as np
import time
import base64

BUFFER_SIZE= 65553

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)


#the first user to enter the room is going to create this UDP server so it acts as a client to the web server but also 
#server for the purposes of the video 
host_name = socket.gethostname()
host_ip = '10.0.0.36'
print(host_ip)

port = 4444
socket_address = (host_ip, port)  #this is the IP and address and port needed for address
server_socket.bind(socket_address)
print("Listening at", socket_address)

#First step is to get the IP of the user that sets up this server 
#Then to see how to get the video data into this piece of code 
    #this most likely entails some javascript to retrieve the video data 
    #and have it display on all other users screens
vid = cv2.VideoCapture("")
