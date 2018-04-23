"""
This program geolocates the user,
then gets the weather data from their location(zipcode),
then displays the local weather.
"""


__author__ = "Joseph Hnatek"
__date__ = "12/23/17"

import time
import datetime
import Weather

def main():
    """Gathers the data and refreshes every 20mins"""

    while True:

        currentTime = datetime.datetime.today()
        print("Gathering weather information for your location... at: {}"
              .format(currentTime.strftime('%I:%M%p')))

        zip = Weather.geolocate()
        Data = Weather.getWeatherData(zip)

        weather = Weather.Weather(Data)
        
        print(weather)

        time.sleep(1200)    #   Refreshes ever 20mins
        print("\n")


if __name__ == "__main__":
    version = "3.0.0"
    print("Version Number: {}".format(version))
    main()
