"""
Program geolocates the user, then gets the weather data from their location,
then displays the weather
"""

__author__ = "Joseph Hnatek"
__date__ = "12/23/17"

def geolocate():
    import urllib.request as link
    import json

    data = link.urlopen("http://freegeoip.net/json/")
    json_string = data.read().decode()
    data.close()
    location = json.loads(json_string)

    zip = location['zip_code']

    return(zip)


def getWeatherData(zipCode):
    import urllib.request as link
    import json
    import apikey

    API_KEY = apikey.getKey() #Get your own key at: http://openweathermap.org/appid

    url = ("http://api.openweathermap.org/data/2.5/weather?zip=" + zipCode + "&appid=" + API_KEY)

    data = link.urlopen(url)
    json_string = data.read().decode()
    data.close()

    data = json.loads(json_string)

    return(data)


def getWeather(Data):
    location = Data["name"]

    kelvin = Data["main"]["temp"]               #   Temperature
    fahrenheit = int(1.8 *(kelvin - 273) + 32)  #   Converting Kelvin to Fahrenheit

    """TODO calculate where the wind is blowing to"""
    wsMPS = Data['wind']['speed']   #   Wind speed in meters per second
    wsMPH = int(wsMPS * 2.2369)        #   Converting Wind speed m/s to mph

    if (fahrenheit <= 50 and wsMPH >= 3.0):  #  Wind chill in effect
        windchill = int(35.74 + (0.6215*fahrenheit) - 35.75*(wsMPH**0.16) + (0.4275*fahrenheit)*(wsMPH**0.16))
    else:
        windchill = "None"




    main = Data["weather"][0]["main"]
    mainDes = Data["weather"][0]["description"]

    return location, fahrenheit, main, mainDes, wsMPH, windchill


def printWeather(location, temp, curMain, mainDes, windSpeed, windChill):
    print("")
    print(location + ": ", temp , "°F | Wind Chill Advisory: ", windChill, "°F")
    print(curMain + ": " + mainDes)
    print("Wind Speed: ", windSpeed, "mph")
    


def main():
    import datetime
    import time

    while True:
        currentTime = datetime.datetime.today()
        print("Gathering weather information for your location... at:", currentTime.strftime('%I:%M%p'))

        zip = geolocate()
        data = getWeatherData(zip)
        location, temp, curMain, mainDes, windSpeed, windChill = getWeather(data)
        printWeather(location, temp, curMain, mainDes, windSpeed, windChill)

        time.sleep(1200)
        print("\n")


if __name__ == "__main__":
    version = "1.2.0"
    print("Version Number: ", version)
    main()


