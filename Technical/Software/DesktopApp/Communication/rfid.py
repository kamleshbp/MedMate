import socket
from global_variables import get_rfid
from utilities import get_physical_location,get_x,get_y
from MapGraphics.map_graphic import draw_point
from Communication.sync_backend_requests import set_robot_status
from tkinter import messagebox

def receive_robo_location(ui,ip,port,response):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip,port))
    except:
        messagebox.showerror("Error!","Location Sensor Not Activated")
        return
    print('connected with RFID')
    robo_start_location=response['robot']['location']
    robo_start_direction=response['robot']['direction']
    robo_mac_id=response['robot']['macId']
    prev_loc=robo_start_location
    while get_rfid():
        data=client.recv(20).decode()
        #print("Robo loc",data,get_physical_location(data))
        if data != prev_loc:
            robo_prev_x=get_x(prev_loc)
            robo_prev_y=get_y(prev_loc)
            draw_point(ui.mapview,robo_prev_x,robo_prev_y,'red',size=5)
            robo_x=get_x(data)
            robo_y=get_y(data)
            draw_point(ui.mapview,robo_x,robo_y,'blue',size=10)
            req_data={}
            req_data['direction']=robo_start_direction
            req_data['location']=data
            req_data['macId']=robo_mac_id
            req_data['status']="None"
            set_robot_status(req_data)
            prev_loc=data

    client.close()
