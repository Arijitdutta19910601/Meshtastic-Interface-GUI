#!/usr/bin/python3
from datetime import *
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
#root.geometry("658x395")

class RepeatedTimer(object): # Timer helper class
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.s = self.function(*self.args, **self.kwargs)
    if self.s == 1:
    	self.stop()

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False


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
  	size = sys.getsizeof(packet['decoded']['data']['payload'])
  	fromid = (packet['fromId'])
  	toId = (packet['toId'])
  	data = (packet['decoded']['data']['payload']).decode('utf-8')
  	rx_time = (packet['rxTime'])
  	rxSnr = (packet['rxSnr'])
  	
  except:
  	data = packet.(decode('utf-8'))
  
  data = str(data)
  
  try:
  	value = (packet['rxSnr'])
  except:
  	value = 0
  
  new_row = [data, size, fromid, toId, rx_time, rxSnr]
  
  #write message to csv file
  with open('new.csv', 'a') as appendobj:
  	append = csv.writer(appendobj)
  	append.writerow(new_row) 
  	
  #Write message to chat window
  LoadOtherEntry(txt, data, value)
  	
  input_dict = {'data': data, 'size': size, 'fromId': fromid, 'toId': toId, 'Time_stamp': rx_time}
  result = []
  for data, size in input_dict.items():
    result.append({'Size': size, 'Data': data})
  
  #playsound("/home/arijit/meshtasticGUI/notif.wav")

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
    interface.sendText(EntryText)

def true():
    timer(1)
    
def randchar(ran):
       	if ran == '':
       		return 1
       	LoadMyEntry(txt, ran)
       	txt.yview(END)    #Scroll to the bottom of chat windows
       	interface.sendText(ran)



def randchar2():
	file_pos=0
	with open('NewFile.txt', 'r') as f:
		for line in f:
			l = line.strip()
			if l is None:
				break
			LoadMyEntry(txt, l)
			txt.yview(END)
			interface.sendText(l)
			print(l)
			time.sleep(30)
			file_pos += len(line)
			f.seek(file_pos)
	f.close()
	file_pos=0		
	with open('NewFile.txt', 'r') as f:
		for line in f:
			l = line.strip()
			if l is None:
				break
			LoadMyEntry(txt, l)
			txt.yview(END)
			interface.sendText(l)
			print(l)
			time.sleep(60)
			file_pos += len(line)
			f.seek(file_pos)
	f.close()
	file_pos=0
	with open('NewFile.txt', 'r') as f:
		for line in f:
			l = line.strip()
			if l is None:
				break
			LoadMyEntry(txt, l)
			txt.yview(END)
			interface.sendText(l)
			print(l)
			time.sleep(90)
			file_pos += len(line)
			f.seek(file_pos)
	f.close()
	file_pos=0
	with open('NewFile.txt', 'r') as f:
		for line in f:
			l = line.strip()
			if l is None:
				break
			LoadMyEntry(txt, l)
			txt.yview(END)
			interface.sendText(l)
			print(l)
			time.sleep(120)
			file_pos += len(line)
			f.seek(file_pos)
	f.close()
	stop2()
	return 1

def timer(x):
    if x != 3:
        print("starting random messages...")
        '''file = open('myFile.txt', 'r')
        while True:
        	rando = file.readline()
        	ran = rando.strip()
        	print(ran)
        	#randchar2()
        	#randchar()'''
        #rt = RepeatedTimer(150, randchar2)
        time1 = threading.Timer(1, randchar2)
        time1.start()
        '''rt = RepeatedTimer(1, randchar, ran)
        	time.sleep(2)
        	if ran == '':
        		break
        file.close()
        stop2()
        
        file = open('myFile.txt', 'r')
        while True:
        	rando = file.readline()
        	ran = rando.strip()
        	print(ran)
        	if not ran:
        		break
        	randchar(ran)
        	#rt = RepeatedTimer(60, randchar(ran))
        file.close()
        stop2()
        file = open('myFile.txt', 'r')
        while True:
        	rando = file.readline()
        	ran = rando.strip()
        	print(ran)
        	if not ran:
        		break
        	randchar(ran)
        	#rt = RepeatedTimer(120, randchar(ran))
        file.close()
        stop2()
        file = open('myFile.txt', 'r')
        while True:
        	rando = file.readline()
        	ran = rando.strip()
        	print(ran)
        	if not ran:
        		break
        	randchar(ran)
        	rt = RepeatedTimer(180, randchar, ran)
        file.close()
        stop2()'''

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

#Bind a scrollbar to the  GUI App
scrollbar = Scrollbar(root, command=txt.yview)
txt['yscrollcommand'] = scrollbar.set
scrollbar.place(x = 1355,y = 7,height = 660)

#root.iconbitmap(r"@/home/arijit/Documents/M.Tech Final Year Project/code/41zvoDg7HlL.xbm")
txt.grid(row=0,column=0,columnspan = 5,ipadx=800, sticky = "NSEW") #line txt for increasing text area
#scrollbar = Scrollbar(txt, orient=VERTICAL)
#scrollbar.pack(fill=Y, side=RIGHT)
e = Entry(root,width = 145)
pub.subscribe(onConnection, "meshtastic.connection.established")
#start = Button(root,text = "START",command = subscribe).grid(row = 1,column = 2)
stop = Button(root,text = "STOP",command = stop).grid(row = 1,column = 2,ipadx=70, sticky="NSEW")
sent = Button(root,text = "SEND",command = send).grid(row = 1,column = 1,ipadx=70, sticky="NSEW")
e.bind("<Return>", DisableEntry)
e.bind("<KeyRelease-Return>", PressAction)
randomchar = Button(root,text = "RAND",command = true).grid(row = 1,column = 3,ipadx=70, sticky="NSEW")
exit = Button(root,text = "EXIT",command = exit).grid(row = 1,column = 4,ipadx=70, sticky="NSEW")
e.grid(row = 1,column = 0)
pub.subscribe(onReceive, "meshtastic.receive")# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.SerialInterface()
root.mainloop()
