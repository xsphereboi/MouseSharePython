import socket
import mouse
import wx
import pyautogui
#from pynput.mouse import Button,Controller

app=wx.App(False)
width,height = wx.GetDisplaySize()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('IP',5000))
s.send(bytes(f'{width}:{height}','utf-8'))
#control = Controller()
class Musa:
    def __init__(self):
        pass

    def click(self,event):
        try:
            if event['event'] =='ButtonEvent':
                #axis=mouse.get_position()
                pyautogui.click(button=event['button'],clicks=1)
                #if event['button']=='Left':
                    #control.press(Button.Left)
        except Exception:
            pass
    
    def scroll(self,event):
        pyautogui.scroll(event['delta'])

def oas(osa):
    pass
musa=Musa()
def controller(event):
    eventName = eval(event)
    #print(eventName)
    if eventName['event'] == 'Movement':
        mouse.move(eventName['x'],eventName['y'])
    elif eventName['event'] == 'Wheel':
        musa.scroll(eventName)
    elif eventName['event'] == 'ButtonEvent':
        musa.click(eventName)
        #musa.click(eventName)
#cursor=Musa()
isSwitched =False
while True:
    axis= mouse.get_position()
    data=s.recv(1024).decode('utf-8')
    #print(data)
    if 'RESUME' in data:
        isSwitched=False
        s.send(bytes('BLOCK','utf-8'))
    if axis[0] ==1365:
        mouse.move(width-20,axis[1])
        s.send(bytes('UNBLOC','utf-8'))
        isSwitched=True
        
    if not isSwitched:

        #print(eval(data))
        all_data= data.split('\n')[-1]
        try:
            controller(all_data)
        except Exception:
            pass
    # controller(all_data)
    #print(all_data)
        #cursor.moveCursor(all_data)
    #serverSocket.send(bytes('Send me more','utf-8'))
