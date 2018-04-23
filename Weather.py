__author__ = "Joseph Hnatek"
__date__ = "April 18, 2018"

import datetime
import urllib as link
import json
import apikey

class Weather():
    def __init__(self, Data):
        self.__location = str(Data["name"])

        self.__temp = int(1.8 * (Data["main"]["temp"] - 273) + 32)

        self.__windSpeed = int(Data["wind"]["speed"] * 2.2369)

        if self.__temp <= 50 and self.__windSpeed >= 3.0:  # Wind chill in effect
            self.__windChill = int(35.74  # Formula: https://goo.gl/yuuWb2
                            + (0.6215 * self.__temp)  #
                            - 35.75 * (self.__windSpeed ** 0.16)  #
                            + (0.4275 * self.__temp)  #
                            * (self.__windSpeed ** 0.16))  #
        else:
            self.__windChill = "None"

        self.__humidity = Data["main"]["humidity"]

        if (self.__temp >= 80):

            c1 = -42.379
            c2 = 2.04901523
            c3 = 10.14333127
            c4 = -0.22475541
            c5 = -6.83783e-3
            c6 = -5.481717e-2
            c7 = 1.22874e-3
            c8 = 8.5282e-4
            c9 = -1.99e-6

            temp = self.__temp
            hum = self.__humidity

            heatIndex = (c1 + c2 * temp + c3 * hum + c4  #
                         * temp * hum + c5 * temp ** 2  #
                         + c6 * hum ** 2 + c7 * temp ** 2  # Formula: https://goo.gl/TnfpLw
                         * hum + c8 * temp * hum ** 2  #
                         + c9 * temp ** 2 * hum ** 2)  #

            if (heatIndex >= 80 and heatIndex <= 90):
                self.__heatIndex = "use CAUTION"
            elif (heatIndex >= 91 and heatIndex <= 103):
                self.__heatIndex = "use EXTREME CAUTION"
            elif (heatIndex >= 104 and heatIndex <= 125):
                self.__heatIndex = "DANGER; STAY INSIDE"
            else:
                self.__heatIndex = "EXTREME DANGER; STAY INSIDE"
        else:
            self.__heatIndex = "None"

        self.__mDesc = Data["weather"][0]["main"]
        self.__oDesc = Data["weather"][0]["description"]


        deg = Data["wind"]["deg"]

        val = int((deg / 22.5) + .5)                              # Special Thanks to:
        arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",  #
               "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]  #
                                                                  #   https://stackoverflow.com/users/697151/steve-gregory
        self.__windDir = arr[(val % 16)]

        sunriseTimeStamp = Data["sys"]["sunrise"]
        sunRise = datetime.datetime.fromtimestamp(sunriseTimeStamp)  # UNIX to time

        self.__sunRise = sunRise.strftime("%I:%M%p")

        sunsetTimeStamp = Data["sys"]["sunset"]
        sunSet = datetime.datetime.fromtimestamp(sunsetTimeStamp)  # UNIX to time

        self.__sunSet = sunSet.strftime("%I:%M%p")


    @property
    def getLocation(self):
        return self.__location

    @property
    def getTemp(self):
        return self.__temp

    @property
    def getWindSpeed(self):
        return self.__windSpeed

    @property
    def getWindChill(self):
        return self.__windChill

    @property
    def getHumidity(self):
        return self.__humidity

    @property
    def getHeatIndex(self):
        return self.__heatIndex

    @property
    def getMainDesc(self):
        return self.__mDesc

    @property
    def getODesc(self):
        return self.__oDesc

    @property
    def getWindDir(self):
        return self.__windDir

    @property
    def getSunRise(self):
        return self.__sunRise

    @property
    def getSunSet(self):
        return self.__sunSet

    def __str__(self):
        string =  """{}: {}F | Wind chill advisory: {} | Heat index advisory: {}
{}: {}
Wind speed: {}mph | Wind direction: {}
Humidity: {}%
Sunrise: {}
Sunset: {}""".format(self.getLocation, self.getTemp, self.__windChill, self.getHeatIndex,
                     self.getMainDesc, self.getODesc, self.getWindSpeed, self.getWindDir,
                     self.getHumidity, self.getSunRise, self.getSunSet)
        return string


def geolocate():
    """Returns the users zip code based from their ip"""

    geoData = link.urlopen("http://freegeoip.net/json/")
    json_string = geoData.read().decode()
    geoData.close()
    location = json.loads(json_string)

    zip = location['zip_code']

    return(zip)


def getWeatherData(zipCode):
    """Returns the JSON dict from the API of openweathermap.com"""

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
