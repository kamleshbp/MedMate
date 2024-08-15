import cv2
import urllib
import numpy as np
from PIL import ImageTk,Image
from global_variables import get_video,set_video
from tkinter import messagebox

def video_connect(ip,port,ui):
    try:
        stream = urllib.request.urlopen("http://"+ip+":"+str(port)+"/stream.mjpg")
    except:
        messagebox.showerror("Error!","Line Camera Not Activated")
        return
    bytes = ''.encode()
    while get_video():
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            tki = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)))
            ui.video_panel.configure(image=tki)
            ui.video_panel._backbuffer_ = tki
    image=ImageTk.PhotoImage(Image.open("blank.png"))
    ui.video_panel.configure(image=image)
    ui.video_panel.image=image

def video_connect1(ip,port,ui):
    try:
        stream = urllib.request.urlopen("http://"+ip+":"+str(port)+"/stream.mjpg")
    except:
        messagebox.showerror("Error!","Main Camera Not Activated")
        return
    bytes = ''.encode()
    while get_video():
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            tki = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)))
            ui.video_panel1.configure(image=tki)
            ui.video_panel1._backbuffer_ = tki
    image=ImageTk.PhotoImage(Image.open("blank.png"))
    ui.video_panel1.configure(image=image)
    ui.video_panel1.image=image

def ip_video_connect(ip,port,ui):
    try:
        cap=cv2.VideoCapture("rtsp://admin:123456@"+ip+":"+str(port)+"/profile0")
        while get_video():
            _, frame = cap.read()
            #frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            ui.video_panel1.imgtk = imgtk
            ui.video_panel1.configure(image=imgtk)
            ui.video_panel1._backbuffer_ = imgtk
        image=ImageTk.PhotoImage(Image.open("blank.png"))
        ui.video_panel1.configure(image=image)
        ui.video_panel1.image=image
    except:
        messagebox.showerror("Error!","Issues in Main Camera...Couldnt Connect")
