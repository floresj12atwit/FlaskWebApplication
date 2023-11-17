
'''
This class is a UDP server for just video transmission, audio is not implemented here this was used to test just video
This is not currently used in the website program
11/17/2023
'''

#This is the UDP server that the first user to enter a room is going to create 
#with the purpose of video streaming, this design may have to be changed since the goal is have 
#all users be able to manipulare the video 

import cv2, imutils, socket
import numpy as np
import time
import base64


video_path = 'WatchParty/website/Videos/SampleVideo1.mp4'    #this will be dynamically updated when we download yotube videos
#The plan is to launch a UDP server when a user enters a video
#And then all users will connect to it and share a video stream
def runVideoServer(local_video_path):
    BUFFER_SIZE= 65536
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

    print("I have arrived")
    
    #For Listening at we may need to import the user that's calling its IP
    host_name = socket.gethostname()
    host_ip = '127.0.0.1'  #This will need to be updated to reflect an actual IP  
    print(host_ip)

    port = 4444
    socket_address = (host_ip, port)  #this is the IP and address and port needed for address
    server_socket.bind(socket_address)
    print("Listening at", socket_address)

    #First step is to get the IP of the user that sets up this server 
    #Then to see how to get the video data into this piece of code 
        #this most likely entails some javascript to retrieve the video data 
        #and have it display on all other users screens
    vid = cv2.VideoCapture(video_path)
    FPS = vid.get(cv2.CAP_PROP_FPS)
    print(FPS)
    fps,st,frames_to_count,cnt = (0,0,20,0)

    while True:
        msg,client_addr =  server_socket.recvfrom(BUFFER_SIZE)
        print('GOT connection from ', client_addr)
        print(msg)
        WIDTH = 400
        global TS
        TS = (0.5/FPS)
        while(vid.isOpened()):
            _,frame = vid.read()
            
            frame = imutils.resize(frame, width= WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            message = base64.b64encode(buffer)       # base64 encoding and decoding is used to converty binary data into an american standard for informatione exchange text format and vice versa
            server_socket.sendto(message, client_addr)
            frame = cv2.putText(frame,'FPS:' +str(fps),(10,40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)
            
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1

            cv2.imshow('TRANSMIITING VIDEO', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF
            if key == ord('q'):
                server_socket.close()
                break
#runVideoServer(video_path) #uncomment this to run just the server and client together without the webapge