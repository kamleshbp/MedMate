import socket
from global_variables import get_lidar,set_detected,set_key_changed
from tkinter import messagebox

def receive_obstacle_detection(ui,ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip,port))
    except:
        messagebox.showerror("Error!","Lidar Sensor Not Activated")
        return
    print('connected with Lidar')
    undetected_cnt=0
    while get_lidar():
        data=client.recv(12).decode()
        #print("Robo loc",data,get_physical_location(data))
        if data != "xxxxxxxxxxxx":
            #print(data)
            set_detected(True)
            set_key_changed(False)
            print("detected")
            undetected_cnt=0
        else:
            print("undetected")
            undetected_cnt+=1
            set_detected(False)
            if undetected_cnt==2:
                set_key_changed(True)
                undetected_cnt=0
    client.close()
