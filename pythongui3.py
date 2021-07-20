#!/usr/bin/python3
from datetime import *
import os
import sys
import tkinter
from tkinter import messagebox
import random
from tkinter import *
import meshtastic
from pubsub import pub
import threading
import pygame
import time
import csv
import datetime
import json
import base64

root = Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (width_value, height_value))

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


def LoadOtherEntry(txt, EntryText, value):
    if EntryText != '':
        txt.config(state=NORMAL)
        if txt.index('end') != None:
            if value == 0:
            	dev = "Device_1->"
            	color = "#FF8000"
            else:
            	dev = "Device_2->"
            	color = "#32CD32"
            LineNumber = float(txt.index('end'))-1.0 
            txt.insert(END, "\n" + dev + EntryText)
            txt.tag_add(dev, LineNumber, LineNumber+1.0)
            txt.tag_config(dev, foreground=color, font=("Arial", 14, "bold"))
            txt.config(state=DISABLED)
            txt.yview(END)
            

def onReceive(packet, interface): # called when a packet arrives
  print("Received: "+str(packet))
  try:
  	clock = time.time_ns()
  	size = sys.getsizeof(packet['decoded']['data']['payload'])
  	message = (packet['decoded']['data']['payload']).decode('utf-8')
  	fromid = (packet['fromId'])
  	toId = (packet['toId'])
  	Id = (packet['id'])
  	new_row = [message, size, fromid, toId, Id, clock]
  	with open('ts46.csv', 'a') as appendobj:
  		append = csv.writer(appendobj)
  		append.writerow(new_row)
  	
  except UnicodeDecodeError:
  	clock = time.time_ns()
  	size = sys.getsizeof(packet['decoded']['data']['payload'])
  	message = (packet['decoded']['data']['payload']).decode('utf-8', 'ignore')
  	fromid = (packet['fromId'])
  	toId = (packet['toId'])
  	Id = (packet['id'])
  	new_row = [message, size, fromid, toId, Id, clock]
  	with open('ts46.csv', 'a') as appendobj:
  		append = csv.writer(appendobj)
  		append.writerow(new_row)  	
  
  except KeyError:
  	try:
  		clock = time.time_ns()
  		size = 0
  		message = str(packet['decoded']['successId'])
  		Id = message
  		message = "success"
  		fromid = (packet['fromId'])
  		toId = (packet['toId'])
  		new1_row = [message, size, fromid, toId, Id, clock]
  		with open('ts46_s.csv', 'a') as appendobj:
  			append = csv.writer(appendobj)
  			append.writerow(new1_row)
  
  	except:
  		clock = time.time_ns()
  		size = 0
  		message = str(packet['decoded']['failId'])
  		Id = message
  		message = "failure"
  		fromid = (packet['fromId'])
  		toId = (packet['toId'])
  		new2_row = [message, size, fromid, toId, Id, clock]
  		with open('ts46_f.csv', 'a') as appendobj:
  			append = csv.writer(appendobj)
  			append.writerow(new2_row)
  except:
  	clock = time.time_ns()
  	size = 0
  	altitude = str(packet['decoded']['position']['altitude'])
  	latitudeI = str(packet['decoded']['position']['latitudeI'])
  	longitudeI = str(packet['decoded']['position']['longitudeI'])
  	Id = (packet['id'])
  	message = str(altitude+latitudeI+longitudeI)
  	fromid = (packet['fromId'])
  	toId = (packet['toId'])
  	new2_row = [message, size, fromid, toId, Id, clock]
  	with open('ts46_f.csv', 'a') as appendobj:
  		append = csv.writer(appendobj)
  		append.writerow(new2_row)
  try:
  	value = (packet['rxSnr'])
  except:
  	value = 0
  
  #Write message to chat window
  LoadOtherEntry(txt, message, value)
  	
  input_dict = {'data': message, 'size': size, 'fromId': fromid, 'toId': toId, 'Time_stamp': clock}
  result = []
  for message, size in input_dict.items():
    result.append({'Size': size, 'Data': message})
  
    #Scroll to the bottom of chat windows
  txt.yview(END)
  
  new = open('/home/arijit/meshtasticGUI/transmission_record.json', "a")
  new.write(json.dumps(result))
  new.close()


def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
   LoadConnectionInfo(txt,"\nStarting..")
   time.sleep(2)
   LoadConnectionInfo(txt,"Connection established Successfully\nStart Communicating..")

def stop2():
    LoadConnectionInfo(txt, "\n\nConnection is closing now..")
    timer(3)
    interface.close()
    LoadConnectionInfo(txt, "Disconnected now..")
        
def stop():
    LoadConnectionInfo(txt, "\n\nConnection is closing now..")
    timer(3)
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
    interface.sendText(EntryText, wantAck = True)

def true():
    timer(1)
    
def randchar():
	file_pos=0
	with open('file2.txt') as f:
	    while True:
		# Read from file 
	        c = f.read(223)
	        if not c:
	            break
	        LoadMyEntry(txt, c)
        	txt.yview(END)    
	        interface.sendText(c, wantAck = True)
	        time.sleep(30)
        	file_pos += len(c)
        	f.seek(file_pos)	        
	f.close()
	stop2()
	playsound("/home/arijit/meshtasticGUI/notif.wav")
	return 1

def timer(x):
    if x != 3:
        print("starting random messages...")
        time1 = threading.Timer(1, randchar)
        time1.start()

def exit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop2()
        root.destroy()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop2()
        root.destroy()

def PressAction(event):
	e.config(state=NORMAL)
	send()

def DisableEntry(event):
	e.config(state=DISABLED)

root.grid_columnconfigure(0, weight=8)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_rowconfigure(0, weight=8)
root.grid_rowconfigure(1, weight=0)
root.configure(background = "White")
root.title("MeshtasticGUI") #"tk" is replaced with "Meshtastic"
root.resizable(width=TRUE, height=TRUE)
img = tkinter.Image("photo", file="/home/arijit/meshtasticGUI/41zvoDg7HlL.png")
root.tk.call('wm','iconphoto',root._w, img)
txt = Text(root, width = 100, height = 100, background = "black", foreground = "#FFFFFF", font = ("Sans_Serif", 10))
root.protocol("WM_DELETE_WINDOW", on_closing)

#Bind a scrollbar to the GUI App
scrollbar = Scrollbar(root, command=txt.yview)
txt['yscrollcommand'] = scrollbar.set
scrollbar.place(x = 1355,y = 7,height = 660)
txt.grid(row=0,column=0,columnspan = 5,ipadx=800, sticky = "NSEW") #line txt for increasing text area
e = Entry(root,width = 145)
pub.subscribe(onConnection, "meshtastic.connection.established")
playsound("/home/arijit/meshtasticGUI/notif.wav")
stop = Button(root,text = "STOP",command = stop).grid(row = 1,column = 2,ipadx=70, sticky="NSEW")
sent = Button(root,text = "SEND",command = send).grid(row = 1,column = 1,ipadx=70, sticky="NSEW")
e.bind("<Return>", DisableEntry)
e.bind("<KeyRelease-Return>", PressAction)
randomchar = Button(root,text = "READ",command = true).grid(row = 1,column = 3,ipadx=70, sticky="NSEW")
exit = Button(root,text = "EXIT",command = exit).grid(row = 1,column = 4,ipadx=70, sticky="NSEW")
e.grid(row = 1,column = 0)
pub.subscribe(onReceive, "meshtastic.receive")# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.SerialInterface()
root.mainloop()
