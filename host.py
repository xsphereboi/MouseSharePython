import socket
import mouse
import threading
from ctypes import *
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #initiate tcp socket

s.bind(('0.0.0.0',5000))

s.listen(5)#listen for connection


clientSocket ,address = s.accept()
clientSocket.settimeout(0.5)
msg=clientSocket.recv(1024)#Looking for client's Display Size
clientwidth,clientheight = msg.decode('utf-8').split(':')

recent_axis=''
switch = False
def onClick(button):
    """Send MouseEvents to client except for mouseMovement.
    For some reason mousemovement event was creating a huge latency
    so i had to keep it on a while loop"""

    eventName = (type(button).__name__)
    if switch:
        if eventName =='MoveEvent':
            dict={'event':'Movement','x':button[0],'y':button[1]}
        elif eventName =='ButtonEvent':
            dict={'event':'ButtonEvent','button':button[1]}
        elif eventName == 'WheelEvent':
            dict={'event':'Wheel','delta':button[0]}
        dict = '\n'+str(dict)
        if eventName!='MoveEvent':
            clientSocket.send(bytes(dict,'utf-8'))


def keyBoardListener():
    pass

def clientListener():
    """Listen For Command From Client  in a seperate thread So That We can do corresponding action"""
    while True:
        try:
            data=clientSocket.recv(1024).decode('utf8')
            if 'UNBLOC' in data:
                mouse.move(1,1)
                #windll.user32.BlockInput(False)
            if 'BLOCK' in data:
                

                #windll.user32.BlockInput(True)
                #print('BLOCK COMMAND RECEIVED') 
        except Exception as e:
            print(e)
            pass

t1=threading.Thread(target=clientListener)
t1.start()
mouse.hook(onClick)


while 1:

    axis=mouse.get_position()
    if axis[0] <= 0:

        """SEND RESUME COMMAND TO CLIENT IF THE HOST's 
        x axis =0. Also Blocking Mouse Event on Host"""

        switch =True
        clientSocket.send(bytes('RESUME','utf-8'))

    if switch:
        dict='\n'+str({'event':'Movement','x':axis[0],'y':axis[1]})
        #dict={''}
        if dict!=recent_axis:   #

            """Skip if the axis are same as of previously sent axis .
            This Helps to Let Client Use Mouse When the host doesnt do anything with his mouse""" 

            clientSocket.send(bytes((dict),'utf-8'))
            recent_axis=dict
    pass
