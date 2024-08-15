import json
import os


filename = "info.json"

def read_cache():

    file=None
    if os.path.exists(filename):
        file = open(filename,'r')

    else:
        cache={
        "token" : "",
        "hKey" : "",
        "timestamp" : "None",
        "locations" : ""
        }
        file = open(filename,"w+")
        json.dump(cache,file)
        file.close()
        file = open(filename,'r')

    cache = json.load(file)
    file.close()
    return cache

def write_cache(cache):
    file = open(filename,'w')
    json.dump(cache,file)
    file.close()

def store_cache_login_token(token):
    cache=read_cache()
    cache['token']=token
    write_cache(cache)

def get_cache_login_token():
    #get the login credentials for auto login
    cache=read_cache()
    return cache['token']

def store_cache_hKey(hKey):
    cache=read_cache()
    cache['hKey']=hKey
    write_cache(cache)

def get_cache_hKey():
    #get the login credentials for auto login
    cache=read_cache()
    return cache['hKey']

def get_map_data():
    #get the map data from the file to show it on canvas
    cache=read_cache()
    return cache['locations']

def store_map_data(location_arr):
    #set the map data in the file that you get from the backend
    cache=read_cache()
    cache['locations']={}
    for l in location_arr:
        d = {}
        key=l['sensorId']
        d['xCor']=l['xCor']
        d['yCor']=l['yCor']
        d['floorNo']=l['floorNo']
        d['physicalName'] = l['physicalName']
        cache['locations'][key]=d
    write_cache(cache)


def store_cached_ts(ts):
    #set the cached TS you get from backend
    cache=read_cache()
    cache['timestamp']=ts
    write_cache(cache)

def get_cached_ts():
    #get the cached ts
    cache=read_cache()
    return cache['timestamp']
