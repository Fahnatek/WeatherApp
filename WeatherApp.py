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
    strData = str(Data)

    location = Data["name"]
    kelvin = Data["main"]["temp"]

    fahrenheit = int(1.8 *(kelvin - 273) + 32)

    main = Data["weather"][0]["main"]
    mainDes = Data["weather"][0]["description"]
    
    return (location, fahrenheit, main, mainDes)
    
def printWeather(location, temp, curMain, mainDes):
    print("")
    print(location + ": " , temp , "°F")
    print(curMain + ": " + mainDes)


def main():
    import datetime
    import time

    while True:
        currentTime = datetime.datetime.today()
        print("Gathering weather information for your location... at:", currentTime.strftime('%I:%M%p'))
       
        zip = geolocate()
        data = getWeatherData(zip)
        location, temp, curMain, mainDes = getWeather(data)
        printWeather(location, temp, curMain, mainDes)

        time.sleep(1200)
        print("\n")

if __name__ == "__main__":
    version = "1.1.1"
    print("Version Number: ", version)
    main()


