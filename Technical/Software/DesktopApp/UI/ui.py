from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from MapGraphics.map_graphic import draw_map,draw_point
from global_variables import set_login_success,set_token_val,set_audio,set_keyboard,set_hKey,set_rfid,set_lidar
from Communication.sync_backend_requests import operator_login,send_order_request
from Communication.robo_com import audio_loop,video_loop
from utilities import get_physical_location,get_x,get_y
from Communication.keyboard import door_control
import sys

class Ui:
    def __init__(self):
        self.root=Tk()
        self.root.geometry("1350x1000")


        self.message=Label(self.root)

        #Pre-login Screen
        self.username_label=Label(self.root)
        self.password_label=Label(self.root)
        self.username_enrty=Entry(self.root)
        self.password_entry=Entry(self.root,show="*")
        self.remember_me=IntVar()
        self.remember_me_chkbox=Checkbutton(self.root,text="remember me",variable=self.remember_me,onvalue=1,offvalue=0)
        self.login_button=Button(self.root,text="Login",command=self.login)

        #Post Login Screen
        self.image=ImageTk.PhotoImage(Image.open("blank.png"))
        self.video_label=Label(self.root,text="Line Camera")
        self.video_panel=Label(self.root,image=self.image)
        self.video_panel.image=self.image
        self.video_panel1=Label(self.root,image=self.image)
        self.video_panel1.image=self.image
        self.video_label1=Label(self.root,text="Main Camera")
        self.mapview=Canvas(self.root, width = 450, height = 500)
        self.audio_button=Button(self.root,text="Switch ON Audio",command= lambda: audio_loop(self))
        self.video_button=Button(self.root,text="Switch ON Video",command= lambda: video_loop(self))
        self.search_places=Entry(self.root)
        self.search_label=Label(self.root)
        self.search_label.config(text="Search Places in Map")
        self.door_button=Button(self.root,text="Open the Door",command=lambda: door_control(self))

        #self.ord_req_data_msg=Message(self.root,text="")

        #Start and Stop button are for starting the navigation command and stoping them(Which will basically stop the robot too)
        self.start_button=Button(self.root,text="Start")
        self.stop_button=Button(self.root,text="Stop")

        #Request data
        self.request_view_button=Button(self.root,text="Show Order Request Data",command=self.show_order_req_data)

        self.logout_button=Button(self.root,text="Logout")

        #Notif Screen

        #self.notif_bar=MessageBox(self.root)

        self.root.wm_title("Medmate Private Ltd.")





    def pre_login_screen(self):
        self.username_label.configure(text="Username")
        self.username_label.place(relx=0.4,rely=0.45)
        self.username_enrty.place(relx=0.6,rely=0.45)
        self.password_label.configure(text="Password")
        self.password_label.place(relx=0.4,rely=0.55)
        self.password_entry.place(relx=0.6,rely=0.55)
        self.remember_me_chkbox.place(relx=0.5,rely=0.6)
        self.login_button.place(relx=0.5,rely=0.65)
        self.message.configure(text="Welcome. Please Login")
        self.message.place(relx=0.5,rely=0.1)

    def clear_pre_login_screen(self):
        self.username_label.place_forget()
        self.username_enrty.place_forget()
        self.password_label.place_forget()
        self.password_entry.place_forget()
        self.remember_me_chkbox.place_forget()
        self.login_button.place_forget()

    def post_login_pre_notif_screen(self,location_arr):
        self.message.configure(text="Waiting For The Request To Come")
        self.message.place(relx=0.5,rely=0.1)

        #self.video_panel.place(relx=0.05,rely=0.2,height=400,width=300)
        self.video_panel1.place(relx=0.05,rely=0.2,height=400,width=700)
        self.video_button.place(relx=0.2,rely=0.75)
        self.video_label.place(relx=0.15,rely=0.15)
        self.video_label1.place(relx=0.4,rely=0.15)
        self.audio_button.place(relx=0.285,rely=0.75)
        self.lock_audio_button()
        self.lock_video_button()

        self.search_label.place(relx=0.65,rely=0.15)
        self.search_places.place(relx=0.75,rely=0.15,width=250)

        location_list=[]
        for location in location_arr:
            physicalName=location_arr[location]['physicalName']
            if physicalName != 'Unknown':
                location_list.append(physicalName)

        self.creat_request_button=Button(self.root,text="Create Request",command= lambda : self.create_request(location_list))
        self.creat_request_button.place(relx=0.25,rely=0.82)
        draw_map(location_arr,self.mapview,self.image)

    def post_login_post_notif_screen(self,ord_req_data):
        self.message.configure(text="Request Assigned")
        self.message.place(relx=0.5,rely=0.1)

        self.msg_data=self.generate_ord_req_text(ord_req_data)
        self.request_view_button.place(relx=0.25,rely=0.12)

        self.door_button.place(relx=0.38,rely=0.12)

        self.unlock_audio_button()
        self.unlock_video_button()
        set_keyboard(True)
        set_rfid(True)
        set_lidar(True)

        sen_loc=ord_req_data['orderRequest']['slocation']
        sen_x=get_x(sen_loc)
        sen_y=get_y(sen_loc)
        rec_loc=ord_req_data['orderRequest']['rlocation']
        rec_x=get_x(rec_loc)
        rec_y=get_y(rec_loc)
        robo_loc=ord_req_data['robot']['location']
        robo_x=get_x(robo_loc)
        robo_y=get_y(robo_loc)

        draw_point(self.mapview,sen_x,sen_y,'white',text='S',size=10)
        draw_point(self.mapview,rec_x,rec_y,'white',text='R',size=10)
        #self.mapview.create_text(220+sen_x*20,240+sen_y*20,font=("Arial",20),text='S')
        #self.mapview.create_text(220+rec_x*20,240+rec_y*20,font=("Arial",20),text='R')
        draw_point(self.mapview,robo_x,robo_y,'blue',size=10)

        #msg_data=self.generate_ord_req_text(ord_req_data)
        #self.ord_req_data_msg.configure(text=msg_data)
        #self.ord_req_data_msg.place(relx=0.1,rely=0.75)

        #draw_map(None,self.mapview,self.image)

    def create_request(self,location_arr):
        self.create_req_window=Tk()
        self.create_req_window.geometry("500x400")

        self.sender_loc_label=Label(self.create_req_window,text="Sender Location")
        self.sender_loc_label.place(relx=0.3,rely=0.2)
        self.sender_var=StringVar(self.create_req_window)
        self.sender_var.set(location_arr[0])
        self.sender_loc_menu=OptionMenu(self.create_req_window,self.sender_var,*location_arr)
        self.sender_loc_menu.place(relx=0.5,rely=0.18)

        self.rec_loc_label=Label(self.create_req_window,text="Receiver Location")
        self.rec_loc_label.place(relx=0.3,rely=0.4)
        self.rec_var=StringVar(self.create_req_window)
        self.rec_var.set(location_arr[1])
        self.rec_loc_menu=OptionMenu(self.create_req_window,self.rec_var,*location_arr)
        self.rec_loc_menu.place(relx=0.5,rely=0.38)

        self.req_msg=Entry(self.create_req_window,width=50)
        self.req_msg.place(relx=0.2,rely=0.6)
        self.req_msg.insert(0,"Request Message")

        self.req_button=Button(self.create_req_window,text="Request",command = lambda : send_order_request(self,self.sender_var.get(),self.rec_var.get(),self.req_msg.get()))
        self.req_button.place(relx=0.45,rely=0.7)


    def show_order_req_data(self):
        self.req_window=Tk()
        self.req_window.geometry("500x400")
        self.ord_req_data_msg=Message(self.req_window,text="")
        self.ord_req_data_msg.configure(text=self.msg_data)
        self.ord_req_data_msg.place(relx=0.1,rely=0.1)


    def generate_ord_req_text(self,ord_req_data):
        c_name="Clinet Name(Who generated the order Request) :  "+ord_req_data['client']['cName']+"\n"
        c_physical_loc=get_physical_location(ord_req_data['client']['workLocation'])
        c_location="Client Work Location : "+c_physical_loc+"\n"
        c_occupation = "Client Occupation : "+ord_req_data['client']['occupation']+"\n\n"
        send_physical_loc=get_physical_location(ord_req_data['orderRequest']['slocation'])
        o_send_location = "Sender Location :" + send_physical_loc+"\n"
        recv_physical_loc=get_physical_location(ord_req_data['orderRequest']['rlocation'])
        o_recv_location = "Receiver Location :" + recv_physical_loc+"\n"
        o_req_msg="Message : " + ord_req_data['orderRequest']['reqMsg']+"\n\n"
        r_mac_id="Assigned Robot mac_id : "+ord_req_data['robot']['macId']+"\n"
        r_name = "Robot Name : "+ord_req_data['robot']['rName']+"\n"
        r_direction = "Robot Direction : "+ord_req_data['robot']['direction']+"\n"
        r_status = "Number of Requests Assigned : "+ord_req_data['robot']['rStatus']+"\n"
        r_location = "Robot Location : " + get_physical_location(ord_req_data['robot']['location'])+"\n"
        return c_name+c_location+c_occupation+o_send_location+o_recv_location+o_req_msg+r_mac_id+r_name+r_direction+r_status+r_location


    def login(self):
        global login_success
        data={}
        data['contactNo']=self.username_enrty.get()
        data['password']=self.password_entry.get()
        response=operator_login(data)
        if response['response']=='Error':
            self.message.configure(text=response['error_message'])
        else:
            set_login_success(True)
            set_token_val(response['token'])
            set_hKey(str(response['hospital']))

    def audio(self,msg):
    	self.audio_button.configure(text=msg)

    def video(self,msg):
    	self.video_button.configure(text=msg)

    def door_config(self,msg):
    	self.door_button.configure(text=msg)

    def lock_audio_button(self):
    	self.audio_button.configure(state=DISABLED)

    def unlock_audio_button(self):
    	self.audio_button.configure(state=NORMAL)

    def lock_video_button(self):
    	self.video_button.configure(state=DISABLED)

    def unlock_video_button(self):
    	self.video_button.configure(state=NORMAL)


    def on_closing(self):
        self.root.destroy()
        set_video(False)
        set_audio(False)
        set_keyboard(False)
    	#close the stream permanantly


    def run_ui(self):
        self.root.mainloop()
