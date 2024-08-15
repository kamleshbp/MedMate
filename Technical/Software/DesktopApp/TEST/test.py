'''
from tkinter import *
from PIL import ImageTk,Image
root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.place(relx=0.1,rely=0.1)
img = ImageTk.PhotoImage(Image.open("blank.png"))
canvas.create_image(100, 20, anchor=NW, image=img)
root.mainloop()
'''
'''
import time
import socket
import keyboard

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.43.73', 8000))
print('connected')

while True:
    data = ['F', 'F', 'F', 'F', 'F']
    try:
        if keyboard.is_pressed(' '):
            data[0] = 'T'
        else:
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                data[1] = 'T'
            if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                data[2] = 'T'
            if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                data[3] = 'T'
            if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                data[4] = 'T'
        print(data)
        client.send("".join(data).encode())
        time.sleep(0.1)
    except KeyboardInterrupt:
        break
    except Exception:
        print('Error')

client.close()
'''

'''
import socket
import threading
import pyaudio
import socket

class Server:
    def __init__(self):
        self.ip = '192.168.43.130'
        self.port=8888

        self.p = pyaudio.PyAudio()
        self.input_stream=self.p.open(format=pyaudio.paInt16,
                        input_device_index=0,
                        channels=2,
                        rate=44100,
                        input=True,
                        frames_per_buffer=4096
                        )
        #self.input_stream.stop_stream()
        self.output_stream=self.p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=4096
                        )
        #self.output_stream.stop_stream()

        while 1:
            try:

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind((self.ip, self.port))

                break
            except Exception as e:
                print(e)
                print("Couldn't bind to that port")


        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))

        #client=None
        while True:
            c, addr = self.s.accept()
            print("connected")
            #client = c
            break


        threading.Thread(target=self.receive_server_data,args=(c,)).start()
        #threading.Thread(target=self.send_server_data,args=(c,)).start()

        #self.send_server_data(c)




    def receive_server_data(self,c):
        self.output_stream.start_stream()
        while True:

            try:
                data = c.recv(4096)
                print(data)
                if not data:
                    break
                self.output_stream.write(data)
            except:
                print("hell1")
                break
        c.close()
        self.output_stream.stop_stream()

    #clear all socket resources



    def send_server_data(self,c):
        #self.input_stream.start_stream()
        while True:
            print("Ahiya aayu",c)
            data = self.input_stream.read(4096,exception_on_overflow=False)
            print("data",data)
            c.sendall(data)
                #print("hell2")
                #break
        c.close()
        self.input_stream.stop_stream()

server = Server()
'''

'''
import pyaudio
p=pyaudio.PyAudio()
print(p.get_device_count())
for ii in range(p.get_device_count()):
    print(p.get_device_info_by_index(ii).get('name'))
'''

'''
from tkinter import *
from PIL import ImageTk,Image
import requests






root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.place(relx=0.1,rely=0.1)
response = requests.get("http://192.168.43.73:8080/stream.mjpg")
print(response.content)
img = ImageTk.PhotoImage(Image.open(response.raw))
canvas.create_image(100, 20, anchor=NW, image=img)
root.mainloop()



import cv2
import urllib
import numpy as np
import threading

root=Tk()
photo=Label(root)
photo.pack()

def video():
    stream = urllib.request.urlopen("http://192.168.43.73:8080/video.mjpg")
    #stream = urllib.request.urlopen("http://localhost:8000/video_feed")
    bytes = ''.encode()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            tki = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)))
            photo.configure(image=tki)
            photo._backbuffer_ = tki
            #cv2.imshow('i', i)
            if cv2.waitKey(1) == 27:
                exit(0)

thread = threading.Thread(target=video)
thread.start()
root.mainloop()
'''
#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
#!/usr/bin/env python3
'''Animates distances and measurment quality'''
#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:
$ ./record_scans.py out.npy'''
#!/usr/bin/env python3
'''Animates distances and measurment quality'''

'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM3'
DMAX = 4000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()


    ax = plt.subplot(111, projection='polar')



    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)



    ax.set_rmax(DMAX)
    ax.grid(True)

    plt.show()

    iterator = lidar.iter_scans()

    print(iterator)


    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    run()
'''

#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar
import math
from tkinter import *
import threading
import time

PORT_NAME = 'COM3'

def sine(degree):
    return math.sin(math.radians(degree))

def cosine(degree):
    return math.cos(math.radians(degree))

def sense_object(start_angle,stop_angle,start_x,stop_x,start_y,stop_y,given_angle,given_distance):
    if given_angle>start_angle and given_angle<stop_angle:
        dist_y = given_distance * sine(given_angle)
        dist_x = given_distance * cosine(given_angle)
        if dist_y>start_y and dist_y<stop_y and dist_x>start_x and dist_x<stop_x:
            return True,dist_x,dist_y
    return False,-1,-1

def run(canvas,path,start_angle,stop_angle,start_x,stop_x,start_y,stop_y):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    start=time.time()
    while True:
        try:
            print('Recording measurments... Press Crl+C to stop.')
            for measurment in lidar.iter_measurments():
                given_angle=measurment[2]
                given_distance=measurment[3]
                flag,dist_x,dist_y = sense_object(start_angle,stop_angle,start_x,stop_x,start_y,stop_y,given_angle,given_distance)
                if flag:
                    #print(dist_x,dist_y,given_angle,given_distance)
                    print("*****Found*****")
                    draw_point(canvas,int(dist_x)//10,-int(dist_y)//10,'blue')
                else:
                    if time.time()-start > 2:
                        create_rectangle(canvas,start_x//10,-start_y//10,stop_x//10,-stop_y//10)
                        print("****Not Found****")
                        start=time.time()

        except:
            print('Stoping.')
            break
    lidar.stop()
    print("Lidar stopped")
    lidar.disconnect()
    outfile.close()
    print("Exiting process")
    sys.exit()

def draw_point(canvas,x,y,colour,size=5,text=''):
    x1, y1 = (220+x*2 - size), (240+y*2 - size)
    x2, y2 = (220+x*2 + size), (240+y*2 + size)
    canvas.create_oval(x1, y1, x2, y2, fill=colour)
    canvas.create_text(220+x*20,240+y*20,font=("Arial",20),text=text)

def create_line(canvas,x1,y1,x2,y2,width=2):
    x1,y1=(220+x1*2),(240+y1*2)
    x2,y2=(220+x2*2),(240+y2*2)
    canvas.create_line(x1,y1,x2,y2,width=width)

def create_rectangle(canvas,x1,y1,x2,y2,fill='white'):
    x1,y1=(220+x1*2),(240+y1*2)
    x2,y2=(220+x2*2),(240+y2*2)
    canvas.create_rectangle(x1,y1,x2,y2,fill=fill)

if __name__ == '__main__':
    root=Tk()
    root.geometry('450x500')
    canvas=Canvas(root, width = 450, height = 500)
    canvas.pack()
    draw_point(canvas,0,0,'red')
    start_angle=0
    stop_angle=180
    start_x=-700
    stop_x=700
    start_y=0
    stop_y=-700
    create_line(canvas,start_x//10,start_y//10,start_x//10,stop_y//10)
    create_line(canvas,stop_x//10,start_y//10,stop_x//10,stop_y//10)
    create_line(canvas,start_x//10,start_y//10,stop_x//10,start_y//10)
    create_line(canvas,start_x//10,stop_y//10,stop_x//10,stop_y//10)
    create_rectangle(canvas,start_x//10,start_y//10,stop_x//10,stop_y//10)
    t1=threading.Thread(target=run,args=[canvas,"abc.txt",start_angle,stop_angle,start_x,stop_x,start_y,-(stop_y)])
    t1.daemon=True
    t1.start()
    root.mainloop()
