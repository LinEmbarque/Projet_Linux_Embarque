# coding: utf-8

import socket
import signal
import sys
import numpy as np
import cv2

def signal_terminate_handler(signum, frame):
    """
    Signal handler
    
    
    """
    
    print("Received signal: {}. Closing connexion ".format(signum))

    camera_connexion.close()
    sys.exit(0)
    
signal.signal(signal.SIGTERM, signal_terminate_handler)
signal.signal(signal.SIGINT, signal_terminate_handler)



host = input("IP adress of the rpi3 card:") #Server IP Address

port = 12810 #port 
image_nb = 0




"""connexion with the camera of the rpi3 """
camera_connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    camera_connexion.connect((host, port))
except socket.error:
    print("Failed to connect")
    sys.exit(0)
        
print("Connexion established with camera on port{}".format(port))

size_request=0
message = b""
received_message=b""

while message != b"q":
    message = input("Write t to take a picture and q to stop:")
   
    if (message!="t" and message!="q"):
        print("You have to input t or q")


    elif (message == "t"):
        try:
            message = message.encode()
            camera_connexion.send(message)
            size_message=camera_connexion.recv(40000)
            size_message=int.from_bytes(size_message, byteorder='big')
            
           
            while size_request<size_message:
                received_tmp = camera_connexion.recv(40960)
                size_request+=len(received_tmp)
                received_message=b"".join([received_message,received_tmp])
            
            size_request=0
            
            if (received_message):
                print('Image ' + str(image_nb) + ' received')
                nparr = np.fromstring(received_message, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imwrite('image' + str(image_nb) + '.jpg',img_np)
                image_nb +=1
            received_message=b""
            
            
        except socket.error:
            print("Error in the received message")
                
    elif (message == "q"):
        try:
            message = message.encode()
            camera_connexion.send(message)
            received_message = camera_connexion.recv(1024)
           
        except socket.error:
            print("Error in the received message")

print("Closing connexion")

camera_connexion.close()
