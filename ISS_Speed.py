# import urlib library -- only useful modules?
import urllib.request
# import json library
import json
# import time library
from time import sleep

from math import sin, cos, asin, sqrt, pi


# functions

def compute_distance(lat1, lon1, lat2, lon2):

    # earth radius + iss altitude, in km
    radius = 6371 + 423
    p = pi/180
    # a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    a = (( sin((( lat2 - lat1 ) * p )/ 2 )) ** 2 ) + cos(lat1 * p) * cos(lat2 * p) * (( sin((( lon2 - lon1 ) * p )/ 2 )) ** 2 )
    return 2 * radius * asin(sqrt(a))


def get_data():

    # save the response from the URL
    response = urllib.request.urlopen(url)
    # storing the JSON response 
    json_data = json.loads(response.read())

    # get coordinates and timestamp
    iss_position = json_data["iss_position"]
    longitude = float(iss_position["longitude"])
    latitude = float(iss_position["latitude"])
    coords = (latitude, longitude)
    timestamp = json_data["timestamp"]

    return coords, timestamp


def compute_speed(coords_old, coords_new, timestamp_old, timestamp_new):

    # time difference between the two timestamps in hours
    time_delta = (timestamp_new - timestamp_old) / 3600
    
    # distance between the two (latitude, longitude) coordinates
    distance = compute_distance(coords_old[0], coords_old[1], coords_new[0], coords_new[1])

    speed = distance / time_delta

    return speed


def get_speed_list(tot_number_of_polls, polling_period):

    # contains computed speed at each polling interval
    speed_list = []

    for poll_number in range(tot_number_of_polls):

        # get current ISS data
        coords_new, timestamp_new = get_data()

        # if not first poll
        if poll_number != 0:
            current_speed = compute_speed(coords_old, coords_new, timestamp_old, timestamp_new)
            print("ISS Current Speed is: %.2f Km/h" %current_speed)
            speed_list.append(current_speed)

        # save current data for next poll
        coords_old = coords_new
        timestamp_old = timestamp_new

        # wait for polling period to repeat the process, except for last poll
        if not (poll_number == tot_number_of_polls - 1):
            sleep(polling_period)

    return speed_list
    

def average(list):
    return sum(list) / len(list)

# Execution

# URL to get ISS position
url = "http://api.open-notify.org/iss-now.json"

# how many times the API will be polled
tot_number_of_polls = 3
# time interval to poll the API
polling_period = 100

# get list containing ISS speed at each polling interval
speed_list = get_speed_list(tot_number_of_polls, polling_period)

# compute average speed over each polling interval
avg_speed = average(speed_list)

print("Average ISS speed over %d samples is: %.2f Km/h" %(tot_number_of_polls, avg_speed))


