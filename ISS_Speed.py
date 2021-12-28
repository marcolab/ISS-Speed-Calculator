# import pandas library to read and manipulate JSON data from API
import pandas as pd
# import timedelta class to compute difference between timestamps
from datetime import timedelta
# import sleep function to pause execution at each polling period
from time import sleep
# import useful math functions for spherical distance computation
from math import sin, cos, asin, sqrt, pi


# functions

# computes spherical distance between two (lat, lon) coordinate sets
def compute_distance(lat1, lon1, lat2, lon2):

    # earth radius + iss altitude, in km
    radius = 6371 + 423
    # switch to radians
    rad = pi/180
    # haversine formula to compute the distance
    hav = (( sin((( lat2 - lat1 ) * rad )/ 2 )) ** 2 ) + cos(lat1 * rad) * cos(lat2 * rad) * (( sin((( lon2 - lon1 ) * rad )/ 2 )) ** 2 )
    return 2 * radius * asin(sqrt(hav))

# poll API and get needed data from the JSON response
def get_data():

    # save the JSON response from the API into a dataframe
    df = pd.read_json(url)

    # get coordinates and timestamp
    longitude = df["iss_position"]["longitude"]
    latitude = df["iss_position"]["latitude"]
    coords = (latitude, longitude)
    timestamp = df["timestamp"][0]

    return coords, timestamp

"""
Compute speed as distance between two coordinates sets 
divided by time difference between their respective timestamps
"""
def compute_speed(coords_1, coords_2, timestamp_1, timestamp_2):

    # time difference between the two timestamps in hours
    time_delta = timedelta.total_seconds(timestamp_2 - timestamp_1) / 3600
    
    # distance between the two (latitude, longitude) coordinates
    distance = compute_distance(coords_1[0], coords_1[1], coords_2[0], coords_2[1])

    speed = distance / time_delta

    return speed

"""
At each time interval:
- get API data
- compute speed using previous interval data (except first iteration)
- save current speed in speed_list
"""
def get_speed_list(tot_number_of_polls, polling_period):

    # contains computed speed at each polling interval
    speed_list = []

    """ 
    Poll API tot_number_of_polls times and get current speed 
    using coordinates from previous poll
    """
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

        # wait for polling period, then repeat the process (except for last poll)
        if not (poll_number == tot_number_of_polls - 1):
            sleep(polling_period)

    return speed_list
    
# compute average of elements in a list
def average(list):
    return sum(list) / len(list)

# Execution

# URL to get ISS position
url = "http://api.open-notify.org/iss-now.json"

# how many times the API will be polled
tot_number_of_polls = 10
# time interval to poll the API
polling_period = 10

print('\n')
# get list containing ISS speed at each polling interval
speed_list = get_speed_list(tot_number_of_polls, polling_period)

# compute average speed over each polling interval
avg_speed = average(speed_list)

print("\nAverage ISS speed over %d samples is: %.2f Km/h\n" %(tot_number_of_polls, avg_speed))


