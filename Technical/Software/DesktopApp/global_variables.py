login_success=False
notif_success=False
mac_id=''
token_val=''
request_id=-1
keyboard=False
audio=False
video=False
ip_addr=None
hKey=''
rfid=False
door=False
door_click=False
lidar=False
detected=False
key_changed=False

def set_key_changed(val):
    global key_changed
    key_changed=val

def get_key_changed():
    return key_changed

def get_detected():
    return detected

def set_detected(val):
    global detected
    detected=val

def get_lidar():
    return lidar

def set_lidar(val):
    global lidar
    lidar=val

def get_door_click():
    return door_click

def set_door_click(val):
    global door_click
    door_click=val

def get_door():
    return door

def set_door(val):
    global door
    door=val

def get_rfid():
    return rfid

def set_rfid(val):
    global rfid
    rfid=val


def get_video():
    return video

def set_video(val):
    global video
    video=val

def get_hKey():
    return hKey

def set_hKey(val):
    global hKey
    hKey=val

def set_ip_addr(val):
    global ip_addr
    ip_addr=val

def get_ip_addr():
    return ip_addr

def set_audio(val):
    global audio
    audio=val

def get_audio():
    return audio

def get_login_success():
    return login_success

def set_login_success(val):
    global login_success
    login_success=val


def get_token_val():
    return token_val

def set_token_val(val):
    global token_val
    token_val=val


def get_mac_id():
    return mac_id

def set_mac_id(val):
    global mac_id
    mac_id=val

def get_notif_success():
    return notif_success

def set_notif_success(val):
    global notif_success
    notif_success=val

def get_request_id():
    return str(request_id)

def set_request_id(val):
    global request_id
    request_id=val

def get_keyboard():
    return str(request_id)

def set_keyboard(val):
    global request_id
    request_id=val
