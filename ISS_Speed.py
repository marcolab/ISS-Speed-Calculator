# Import pandas library to read and manipulate JSON data from API
import pandas as pd
# Import timedelta class to compute difference between timestamps
from datetime import timedelta
# Import sleep function to pause execution at each polling period
from time import sleep
# Import useful math functions for spherical distance computation
from math import sin, cos, asin, sqrt, pi


# Global variables

# URL to get ISS position
url = "http://api.open-notify.org/iss-now.json"

# How many times the API will be polled
tot_number_of_polls = 20
# Time interval to poll the API
polling_period = 30


# Functions

# Computes spherical distance between two (lat, lon) coordinate sets
def compute_distance(lat1, lon1, lat2, lon2):

    # Earth radius + iss altitude, in km
    radius = 6371 + 423
    # Variable to switch to radians
    rad = pi/180
    # Haversine formula to compute the distance
    hav = (( sin((( lat2 - lat1 ) * rad )/ 2 )) ** 2 ) + cos(lat1 * rad) * cos(lat2 * rad) * (( sin((( lon2 - lon1 ) * rad )/ 2 )) ** 2 )
    return 2 * radius * asin(sqrt(hav))

# Poll API and get needed data from the JSON response
def get_data():

    # Save the JSON response from the API into a dataframe
    df = pd.read_json(url)

    # Get coordinates and timestamp
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

    # Time difference between the two timestamps in hours
    time_delta = timedelta.total_seconds(timestamp_2 - timestamp_1) / 3600
    
    # Distance between the two (latitude, longitude) coordinates
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

    # Contains computed speed at each polling interval
    speed_list = []

    """ 
    Poll API tot_number_of_polls times and get current speed 
    using coordinates from previous poll
    """
    for poll_number in range(tot_number_of_polls):

        # Get current ISS data
        coords_new, timestamp_new = get_data()

        # If not first poll
        if poll_number != 0:
            current_speed = compute_speed(coords_old, coords_new, timestamp_old, timestamp_new)
            print("ISS Current Speed is: %.2f Km/h" %current_speed)
            speed_list.append(current_speed)

        # Save current data for next poll
        coords_old = coords_new
        timestamp_old = timestamp_new

        # Wait for polling period, then repeat the process (except for last poll)
        if not (poll_number == tot_number_of_polls - 1):
            sleep(polling_period)

    return speed_list
    
# Compute average of elements in a list
def average(list):
    return sum(list) / len(list)

# Function to execute when script is run
def main():
    print('\n')

    # Get list containing ISS speed at each polling interval
    speed_list = get_speed_list(tot_number_of_polls, polling_period)

    # Compute average speed over each polling interval
    avg_speed = average(speed_list)

    print("\nAverage ISS speed over %d samples is: %.2f Km/h\n" %(tot_number_of_polls, avg_speed))


# Execution

if __name__ == "__main__": 
	main()