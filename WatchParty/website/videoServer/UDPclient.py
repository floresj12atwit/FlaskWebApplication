'''
This class is a UDP client for just video transmission, audio is not implemented here this was used to test just video

This is not currently used in the website program
11/17/23
'''



import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE= 65536

     
def runClient():  #IP will most likely need to be passed in
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '127.0.0.1' # This will need to be dynamically updated somehow use the IP made in the server
    print(host_ip)
    port = 4444
    message = b'TAKE THIS! :D'

    #client_socket.sendto(message, (host_ip, port))
    fps,st,frames_to_count,cnt = (0,0,20,0)

    try:
        client_socket.sendto(b'TAKE THIS! :D', (host_ip, port))

        
        while True:
            packet,_ = client_socket.recvfrom(BUFF_SIZE)

            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data, dtype=np.uint8)        #fromstring is deprecated use frombuffer
            frame = cv2.imdecode(npdata,1)
            frame = cv2.putText(frame,'FPS:' +str(fps),(10,40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                    client_socket.close()
                    break
            if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count/(time.time()-st))
                        st=time.time()
                        cnt=0
                    except:
                        pass
            cnt+=1
    
    except ConnectionResetError:
        print("Connection was forcibly closed by the remote host.")
    finally:
        client_socket.close()

#runClient() #uncomment this line to run the client alone with the UDPserver

