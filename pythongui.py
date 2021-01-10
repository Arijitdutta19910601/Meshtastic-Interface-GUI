from datetime import *
import tkinter
from tkinter import *
import meshtastic
from pubsub import pub
import threading
import pygame
import time
import datetime
import json
import base64

root = Tk()
txt = Text(root, bg = "black", foreground = "#FFFFFF", font = ("Sans_Serif", 10))

def playsound(soundfile):
    """Play sound through default mixer channel in blocking manner.
       This will load the whole sound into memory before playback
    """    
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        clock.tick(1000)    


def LoadConnectionInfo(txt, EntryText):
    if EntryText != '':
        txt.config(state=NORMAL)
        if txt.index('end') != None:
            now = datetime.datetime.now()
            txt.insert(END, EntryText+'\n')
            LineNumber = float(txt.index('end'))-1.0            
            txt.tag_add(EntryText, LineNumber, LineNumber+1.0)
            txt.tag_config(EntryText, foreground="#FFFFFF", font = ("Sans_Serif", 10))
            txt.config(state=DISABLED)
            txt.yview(END)


def LoadMyEntry(txt, EntryText):
    if EntryText != '':
        txt.config(state=NORMAL)
        if txt.index('end') != None:
            current_time = datetime.datetime.now().time()
            LineNumber = float(txt.index('end'))-1.0
            txt.insert(END, "\nDevice_1-> " + EntryText + "\t\t" + str(current_time))
            txt.tag_add("Device_1->", LineNumber, LineNumber+1.0)
            txt.tag_config("Device_1->", foreground="#FF8000", font=("Arial", 14, "bold"))
            txt.config(state=DISABLED)
            txt.yview(END)

def LoadOtherEntry(txt, EntryText):
    if EntryText != '':
        txt.config(state=NORMAL)
        if txt.index('end') != None:
            LineNumber = float(txt.index('end'))-1.0
            current_time = datetime.datetime.now().time()
            txt.insert(END, "\nDevice_2-> " + EntryText + "\t\t" + str(current_time))
            txt.tag_add("Device_2->", LineNumber, LineNumber+1.0)
            txt.tag_config("Device_2->", foreground="#04B404", font=("Arial", 14, "bold"))
            txt.config(state=DISABLED)
            txt.yview(END)


def onReceive(packet, interface): # called when a packet arrives
  """print(f"Received: {packet}")"""
  try:
  	packet = (packet['decoded']['data']['payload']).decode('utf-8')
  except:
  	packet = packet['decoded']['position']
  
  data = str(packet)

  #Write message to chat window
  LoadOtherEntry(txt, data)
  playsound("notif.wav")

  #Scroll to the bottom of chat windows
  txt.yview(END)

  """data = json.dumps(packet, indent = 2).encode('utf-8')
  data = data.encode('ascii')
  base64_bytes = base64.b64encode(data)
  packet = base64_bytes.decode('ascii')
  packet = base64.b64encode(packet)
  data = json.dumps(packet, indent = 2)"""
  
  new = open('new.txt', "a")
  new.write(data)
  new.close()


def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
   LoadConnectionInfo(txt,"\nStarting..")
   time.sleep(2)
   LoadConnectionInfo(txt,"Connection established Successfully\nStart Communicating..")

def stop():   
    LoadConnectionInfo(txt, "\n\nConnection is closing now..")
    interface.close()
    time.sleep(2)
    LoadConnectionInfo(txt, "Disconnected now..")


def send():
    
    EntryText = e.get()

    #Erase previous message in Entry Box
    e.delete('0',END)

    # Loading the message on the chat window
    LoadMyEntry(txt, EntryText)

    #Scroll to the bottom of chat windows
    txt.yview(END)
           
    #Send my mesage to all others
    interface.sendText(EntryText)


def exit():
    root.destroy()

def PressAction(event):
	e.config(state=NORMAL)
	send()

def DisableEntry(event):
	e.config(state=DISABLED)

root.configure(background = "White")
root.title("Meshtastic") #"tk" is replaced with "Meshtastic"
img = tkinter.Image("photo", file="/home/arijit/Documents/M.Tech Final Year Project/code/41zvoDg7HlL.png")
root.tk.call('wm','iconphoto',root._w, img)
#root.iconbitmap(r"@/home/arijit/Documents/M.Tech Final Year Project/code/41zvoDg7HlL.xbm")
txt.grid(row=0,column=0,columnspan = 5) #line txt for increasing text area
e = Entry(root,width = 70)
start = Button(root,text = "START",command = pub.subscribe(onConnection, "meshtastic.connection.established")).grid(row = 1,column = 2)
stop = Button(root,text = "STOP",command = stop).grid(row = 1,column = 3)
sent = Button(root,text = "SEND",command = send).grid(row = 1,column = 1)
e.bind("<Return>", DisableEntry)
e.bind("<KeyRelease-Return>", PressAction)
exit = Button(root,text = "EXIT",command = exit).grid(row = 1,column = 4)
e.grid(row = 1,column = 0)
pub.subscribe(onReceive, "meshtastic.receive")# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.SerialInterface()
root.mainloop()