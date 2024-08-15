from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
from global_variables import set_notif_success,set_request_id
from tkinter import *
from tkinter import messagebox
#here you subscribe to the pubsub and execute it
pnconfig = PNConfiguration()
#grab pubsub keys from backend not hardcoded
pnconfig.publish_key = 'pub-c-fca05d8b-0c16-48c1-889a-b1359a08ed58'
pnconfig.subscribe_key = 'sub-c-9b44bd3e-9b65-11ea-8d30-d29256d12d3d'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        #set the global_variable flag here to notify main thread
        print (message.message)
        '''
        window =Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()
        '''
        answer = messagebox.askyesno("Question", "Request has come with the request Id "+ message.message['request_id']+". Accept?")

        if answer:
            set_notif_success(True)
            set_request_id(message.message['request_id'])
        '''
        window.deiconify()
        window.destroy()
        window.quit()
        '''
def notif_wait_loop():
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("chan-1").execute()
