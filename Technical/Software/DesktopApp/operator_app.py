from UI.ui import Ui
from Cache.cache import get_cache_login_token,store_cache_login_token,get_cached_ts,store_cached_ts,store_cache_hKey,get_cache_hKey,store_map_data,get_map_data
from global_variables import get_notif_success,set_notif_success,get_mac_id,get_token_val,get_login_success,get_request_id,set_keyboard,set_ip_addr,set_token_val,get_hKey,set_hKey
from Medmate_background.pubsub_notif import notif_wait_loop
from Communication.ip_resolution import find_robot_ip_address
from Communication.robo_com import robo_communication
from Communication.sync_backend_requests import operator_ack,get_all_locations
from Communication.rfid import receive_robo_location
from Communication.lidar_communication import receive_obstacle_detection
from utilities import generate_header
from tkinter import messagebox
import sys,os
import threading

'''
--desktop app will be communicating to the server with sync requests
--desktop app will also be waiting for the notifications coming from the server
--desktop app will also be communicating to the robot.will be receiving the video and audio and some other
  data as well as sending some navigation data too.
'''

def onclosing(ui):
    if messagebox.askokcancel("Quit","Do you Want To Quit?"):
        ui.root.destroy()
        os._exit(0)
        print('should not come')

def main(ui):
    global login_success
    if not get_cache_login_token():
        ui.pre_login_screen()
        while not get_login_success():
            #login_success is from global_variables.py
            continue
        #check required if rememberMe is True or not(left)
        store_cache_login_token(get_token_val())
        store_cache_hKey(get_hKey())
    else:
        set_token_val(get_cache_login_token())
        set_hKey(get_cache_hKey())

    ui.clear_pre_login_screen()
    #login part Completes here.Token can be accessed via get_token_val()

    cached_ts=get_cached_ts()
    hKey=get_hKey()
    token=get_token_val()
    headers=generate_header(token)
    location_resp=get_all_locations(hKey,cached_ts,headers)
    if location_resp['msg'] == 'updated':
        location_arr=location_resp['location']
        store_map_data(location_arr)
        updated_ts=location_resp['cachedTs']
        updated_ts=updated_ts[:10]+"%20"+updated_ts[11:]
        store_cached_ts(updated_ts)

    location_arr=get_map_data()
    ui.post_login_pre_notif_screen(location_arr)
    while True:
        threading.Thread(target=notif_wait_loop,args=()).start()
        while not get_notif_success():
            #notif_success is from global_variables.py
            continue

        token=get_token_val()
        headers=generate_header(token)

        #Request_id will be set when the operator accepts the notification in the Medmate_background
        response=operator_ack(get_request_id(),headers)
        if not response['completed']:
            break
        set_notif_success(False)
        messagebox.showerror("Error!","Request Already Assigned to some other operator")

    ip_addr=find_robot_ip_address(response['robot']['macId'])
    set_ip_addr(ip_addr)
    #ip_addr='192.168.43.135'
    #set_ip_addr(ip_addr)

    ui.post_login_post_notif_screen(response)

    threading.Thread(target=robo_communication,args=(ui,ip_addr,8000)).start()
    robo_start_location=response['robot']['location']
    robo_start_direction=response['robot']['direction']
    threading.Thread(target=receive_robo_location,args=(ui,ip_addr,8001,response)).start()
    threading.Thread(target=receive_obstacle_detection,args=(ui,ip_addr,8002)).start()

if __name__=='__main__':
    ui=Ui()
    ui.root.protocol("WM_DELETE_WINDOW",lambda : onclosing(ui))
    t1=threading.Thread(target=main,args=[ui])
    t1.daemon=True
    t1.start()
    ui.run_ui()
