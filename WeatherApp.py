"""
This program geolocates the user,
then gets the weather data from their location(zipcode),
then displays the local weather.
"""


__author__ = "Joseph Hnatek"
__date__ = "12/23/17"


def geolocate():
    """Returns the users zip code based from their ip"""

    import urllib.request as link
    import json

    geoData = link.urlopen("http://freegeoip.net/json/")
    json_string = geoData.read().decode()
    geoData.close()
    location = json.loads(json_string)

    zip = location['zip_code']

    return(zip)


def getWeatherData(zipCode):
    """Returns the JSON dict from the API of openweathermap.com"""

    import urllib.request as link
    import json
    import apikey             #Remove when you get your own key

    API_KEY = apikey.getKey() #Get your own key at: http://openweathermap.org/appid
                              #Replace the code: apikey.getKey() with your key
    url = ("http://api.openweathermap.org/data/2.5/weather?zip=" 
           + zipCode 
           + "&appid=" 
           + API_KEY)

    Data = link.urlopen(url)
    json_string = Data.read().decode()
    Data.close()

    Data = json.loads(json_string)

    return(Data)


def getLocation(Data):
    """Returns the users location"""

    return Data["name"]


def getTemp(Data):
    """Returns the temperature"""

    kelvin = Data["main"]["temp"]
    fahrenheit = int(1.8 *(kelvin - 273) + 32)  #   Converting kelvin to fahrenheit

    return fahrenheit


def getMainDesc(Data):
    """Returns the description of the weather"""

    return Data["weather"][0]["main"]


def getDesc(Data):
    """Returns the description of the weather"""

    return Data["weather"][0]["description"]


def getWindSpeed(Data):
    """Returns the wind speed"""

    wsMPS = Data['wind']['speed']
    wsMPH = int(wsMPS * 2.2369) #   Converting meters per second to miles per hour

    return wsMPH


def getWindDirection(Data):
    """Returns in which way the wind is blowing"""

    deg = Data["wind"]["deg"]

    val=int((deg/22.5)+.5)                              #   Special Thanks to:
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE",   #
         "S","SSW","SW","WSW","W","WNW","NW","NNW"]     #   
                                                        #   https://stackoverflow.com/users/697151/steve-gregory
    return arr[(val % 16)]                              #                                           


def getHumidity(Data):
    """Returns the humidity"""

    return Data["main"]["humidity"]


def getWindChill(Data):
    """Returns the windchill"""

    fahrenheit = getTemp(Data)
    wsMPH = getWindSpeed(Data)

    if (fahrenheit <= 50 and wsMPH >= 3.0):     #   Wind chill in effect
        windchill = int(35.74                   #   Formula: https://goo.gl/yuuWb2
                        + (0.6215*fahrenheit)   #
                        - 35.75*(wsMPH**0.16)   #   
                        + (0.4275*fahrenheit)   #
                        * (wsMPH**0.16))        #
    else:
        windchill = "None"

    return windchill


def getHeatIndex(Data):
    """Returns the heat index"""

    if (getTemp(Data) >= 80):

        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.14333127
        c4 = -0.22475541
        c5 = -6.83783e-3
        c6 = -5.481717e-2
        c7 = 1.22874e-3
        c8 = 8.5282e-4
        c9 = -1.99e-6

        temp = getTemp(Data)
        hum = getHumidity(Data)

        heatIndex = (c1 + c2 * temp + c3 * hum + c4 #
                      * temp * hum + c5 * temp**2   #
                      + c6 * hum**2 + c7 * temp**2  #   Formula: https://goo.gl/TnfpLw
                      * hum + c8 *temp * hum**2     #
                      + c9 * temp**2 * hum**2)      #
    
        if (heatIndex >= 80 and heatIndex <= 90):
            return "use CAUTION"
        elif (heatIndex >= 91 and heatIndex <= 103):
            return "use EXTREME CAUTION"
        elif (heatIndex >= 104 and heatIndex <= 125):
            return "DANGER; STAY INSIDE"
        else: 
            return "EXTREME DANGER; STAY INSIDE"
    else:
        return "None"


def getSunRise(Data):
    """Returns the sunrise time"""

    import datetime

    sunriseTimeStamp = Data["sys"]["sunrise"]
    sunRise = datetime.datetime.fromtimestamp(sunriseTimeStamp) #   UNIX to time

    return sunRise.strftime("%I:%M%p")


def getSunSet(Data):
    """Returns the sunset time"""

    import datetime

    sunsetTimeStamp = Data["sys"]["sunset"]
    sunSet = datetime.datetime.fromtimestamp(sunsetTimeStamp)   #   UNIX to time

    return sunSet.strftime("%I:%M%p")


def printWeather(Data):
    """Displays the weather information"""

    print(getLocation(Data) + ": ", getTemp(Data) 
          , "°F | Wind Chill Advisory: ", getWindChill(Data)
          , "°F | Heat Index Advisory: " + getHeatIndex(Data))

    print(getMainDesc(Data) + ": " + getDesc(Data))

    print("Wind Speed: ", getWindSpeed(Data)
          , "mph | Wind Direction: " + getWindDirection(Data))

    print("Humidity: ", getHumidity(Data), "%")
    print("Sunrise: ", getSunRise(Data))
    print("Sunset: ", getSunSet(Data))
    

def main():
    """Gathers the data and refreshes every 20mins"""

    import time
    import datetime

    while True:

        currentTime = datetime.datetime.today()
        print("Gathering weather information for your location... at:"
              , currentTime.strftime('%I:%M%p'), "\n")

        zip = geolocate()
        Data = getWeatherData(zip)
        printWeather(Data)

        time.sleep(1200)    #   Refreshes ever 20mins
        print("\n")


if __name__ == "__main__":
    version = "2.0.0"
    print("Version Number: ", version)
    main()