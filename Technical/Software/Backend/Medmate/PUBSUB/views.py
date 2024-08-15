from django.shortcuts import render
from django.http import HttpResponse
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub,SubscribeListener
import time
import os


pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-fca05d8b-0c16-48c1-889a-b1359a08ed58'
pnconfig.subscribe_key = 'sub-c-9b44bd3e-9b65-11ea-8d30-d29256d12d3d'
pnconfig.uuid = 'server'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)



def pubsub_view(request):
    pubnub.publish().channel("chan-1").message(request).sync()
