from .keyboard import send_command
import threading
from .sound import audio_connect
from global_variables import get_audio,set_audio,get_ip_addr,get_video,set_video
from .video import video_connect,video_connect1,ip_video_connect

audio_port=8888
video_port=8080
video_port1=8081

def audio_loop(ui):
    '''
    Here the actual communication part with the robot for
    retrieving the audio data will be written.and it will be shown in the UI
    app
    '''
    #ui.lock_audio_button()
    t1=None
    if not get_audio():
        ui.audio("Switch OFF Audio")
        set_audio(True)
        if (t1==None or not t1.isAlive()):
            ip=get_ip_addr()
            t1=threading.Thread(target=audio_connect,args=[ip,audio_port,ui])
            t1.start()
    else:
    	ui.audio("Switch ON Audio")
    	set_audio(False)
    	#inform raspberry to stop audio stream

    	#set global variable

def video_loop(ui):
    '''
    Here the actual communication part with the robot for
    retrieving the video data will be written.and it will be shown in the UI
    app
    '''
    t2=None
    t3=None
    if not get_video():
        ui.video("Switch OFF Video")
        set_video(True)
        if (t2==None or not t2.isAlive()):
            ip=get_ip_addr()
            #t2=threading.Thread(target=video_connect,args=[ip,video_port,ui])
            #t2.start()
            #t3=threading.Thread(target=video_connect1,args=[ip,video_port1,ui])
            t3=threading.Thread(target=ip_video_connect,args=["192.168.43.120",8554,ui])
            t3.start()
    else:
    	ui.video("Switch ON Video")
    	set_video(False)




def robo_communication(ui,ip,port):
    '''
    Thread that will perform the communication with robot using sockets.
    '''
    send_command(ip,port)
