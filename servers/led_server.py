#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:17:41 2020

@author: david
"""

import RPi.GPIO as GPIO                                  
import time                                                
import socket                                              
import signal                                                        
import sys                                                          
                                                   
GPIO.setmode(GPIO.BCM)                                    
GPIO.setup(17, GPIO.OUT)
GPIO.setwarnings(False)                                    
                                                         
                                     
def signal_terminate_handler(signum, frame):
    """
            Manage the closure of a socket 
    """
   
    print("Received signal: {}. Your server is terminated ".format(signum))
    client.close()
    socket_sm.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_terminate_handler)
signal.signal(signal.SIGINT, signal_terminate_handler)
                                                   
host = '127.0.0.1' #adresse IP du serveur
port = 12820 #port d'acces au serveur de LED

GPIO.output(17, GPIO.LOW)
         
""" connexion accepted with the client """

print("Creation of the socket...\n")

socket_sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_sm.bind((host, port))        
socket_sm.listen(5)

print("Waiting a client...\n") 
client, adress = socket_sm.accept()  
print("Client found...\n")                   

""" communication avec le client """

choice = b""
                               
while choice != b"end":            
   
    choice = client.recv(255)

    choice = choice.decode()    

    if choice == "on":
        GPIO.output(17, GPIO.HIGH)
        print("On received...\n")   
        
    elif choice == "off":
        GPIO.output(17, GPIO.LOW)
        print("Off received...\n")   

    client.send(b"5 / 5")      

GPIO.cleanup()
socket_sm.close()

try:
    client.close()
except SyntaxError:
    print("client does not exist yet")
    
    
    
    
    