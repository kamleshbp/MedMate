import requests
from utilities import generate_header,get_sensor_id
from global_variables import get_token_val
from tkinter import messagebox

BASE_URL='http://medmate.pythonanywhere.com'

def operator_login(data):
    url=BASE_URL+'/operator_login'
    print("URL ",url)
    print("Data ",data)
    r=requests.post(url=url,data=data)
    #print(r.text)
    #print(r.status_code)
    print(r.json())
    return r.json()

def operator_ack(requestId,headers):
    url=BASE_URL+'/operator_ack/'+requestId
    r=requests.get(url=url,headers=headers)
    print(r.json())
    return r.json()

def set_request_status(requestId,status,headers):
    url=BASE_URL+'/set_request_status/'+requestId+"/"+status
    r=requests.get(url=url,headers=headers)
    print(r.json())
    return r.json()

def set_robot_status(data):
    url=BASE_URL+'/set_robot_status'
    r=requests.put(url=url,data=data)
    print(r.json())
    return r.json()

def get_all_locations(hKey,cachedTs,headers):
    url=BASE_URL+'/get_all_locations/'+hKey+'/'+cachedTs
    print(url)
    r=requests.get(url=url,headers=headers)
    print(r.json())
    return r.json()

def get_valid_locations(hKey,headers):
    url=BASE_URL+'/get_valid_locations/'+hKey
    r=requests.get(url=url,headers=headers)
    print(r.json())
    return r.json()


#UI Button Invoked Method
def send_order_request(ui,s_location,r_location,req_msg):
    url=BASE_URL+'/order'
    data={}
    data['slocation']=get_sensor_id(s_location)
    data['rlocation']=get_sensor_id(r_location)
    data['reqMsg']=req_msg
    token=get_token_val()
    headers=generate_header(token)
    r=requests.post(url=url,headers=headers,data=data)
    response=r.json()
    if 'error' in response:
        messagebox.showerror("Error","No Robots Available...try after some time")
    ui.create_req_window.destroy()
