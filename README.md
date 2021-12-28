# ISS-Speed-Calculator

This script has the aim of estimating the current speed of the **International Space Station** based on its position at distinct moments. It follows this procedure:
- Get real-time ISS coordinates from the public API at http://api.open-notify.org/iss-now.json
- API is polled every 30 seconds and data regarding ISS position is saved
- At each time interval, the current speed is calculated (and printed to screen) by dividing the covered distance by the elapsed time
- Distance is calculated as a spherical distance through the Haversine formula (ISS orbit approximated to a sphere)
- This operation is repeated for a set number (20) of API polls, after which an average speed is provided as an output

## Libraries

Some useful libraries were exploited for this program:
- Pandas (https://pandas.pydata.org/): get response from API, read and manipulate JSON data
- Datetime (https://docs.python.org/3/library/datetime.html): deal with timestamps and compute time difference between them
- Time (https://docs.python.org/3/library/time.html): sleep function to pause execution at each polling period
- Math (https://docs.python.org/3/library/math.html): useful mathematical functions to calculate traveled distance

## Assumptions

- Distance covered at each time interval is calculated assuming that the station travels on a spherical orbit, hence not changing its altitude
- Time difference between each poll is computed exploiting timestamps provided by the API, since some delays to get the response can be registered
