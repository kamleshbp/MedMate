import time
import socket
import keyboard
from global_variables import get_keyboard,set_door_click,get_door_click,set_door,get_door,get_detected,set_key_changed,get_key_changed
from tkinter import messagebox


def send_command(ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip,port))
    except:
        messagebox.showerror("Error!","Keyboard Connection Cant be Made")
        return
    print('connected to Keyboard')


    while get_keyboard():
        data = ['F', 'F', 'F', 'F', 'F']
        try:
            if keyboard.is_pressed(' '):
                data[0]='T'
            else:
                if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    print("Detection flag ",get_detected())
                    if not get_detected() and get_key_changed():
                        data[1] = 'T'
                        print(data)
                if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                    data[2] = 'T'
                    print(data)
                    set_key_changed(True)
                if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    data[3] = 'T'
                    print(data)
                    set_key_changed(True)
                if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                    data[4] = 'T'
                    print(data)
                    set_key_changed(True)
            if 'T' in data or get_door_click():
                if get_door_click():
                    set_door_click(False)
                    if not get_door():
                        set_door(True)
                        print("Door Opened")
                        client.send("DROPN".encode())
                    else:
                        print("Door Closed")
                        set_door(False)
                        client.send("DRCLS".encode())
                else:
                    client.send("".join(data).encode())

            time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            print('Error')
            break

    client.close()

def door_control(ui):
    set_door_click(True)
    if not get_door():
        ui.door_config("Close The Door")
    else:
        ui.door_config("Open The Door")
