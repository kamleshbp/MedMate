from Cache.cache import get_map_data

def generate_header(token):
    headers={}
    headers['Authorization']='Token '+token
    return headers

def get_physical_location(sensor_id):
    location_arr=get_map_data()
    if location_arr:
        try:
            return location_arr[sensor_id]['physicalName']
        except:
            print("No such location")
    return ""


def get_sensor_id(physical_name):
    location_arr=get_map_data()
    if location_arr:
        try:
            for sensor_id in location_arr:
                if location_arr[sensor_id]['physicalName']==physical_name:
                    return sensor_id
        except:
            print("No such location")
    return ""


def get_x(sensor_id):
    location_arr=get_map_data()
    if location_arr:
        try:
            return location_arr[sensor_id]['xCor']
        except:
            print("No such location")
    return ""

def get_y(sensor_id):
    location_arr=get_map_data()
    if location_arr:
        try:
            return location_arr[sensor_id]['yCor']
        except:
            print("No such location")
    return ""
