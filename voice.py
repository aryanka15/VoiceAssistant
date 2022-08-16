import pyttsx3
import requests

MAX_LIMIT = 5
UNITS = ["imperial", "metric", "standard"]
OWM_KEY = "f3ca8ffdd42e95ff30155fbe8882a532"
OWM_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={unit}"
OWM_URL_GEOCODING = "http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={API_key}"

def talk(engine, text, cmd=False):
    if (cmd):
        print(text)
    engine.say(text)
    engine.runAndWait()

def main():
   
    engine = pyttsx3.init()

    city = input("City for weather. Format as city,state,country or city,country or city: ").strip().lower()

    req = requests.get(OWM_URL_GEOCODING.format(city=city, limit=MAX_LIMIT,API_key=OWM_KEY))
    data = req.json()

    for i, loc in enumerate(data):
        print(str(i+1) + ":", loc["name"], loc["state"], loc["country"], loc["lat"], loc["lon"])

    if (len(data) == 0):
        print("no data found")
        exit()

    elif len(data) > 1:
        while True:
            choice = input("Multiple locations found. Type in the number of the place you would like to get the weather of: ")
            if choice.isdigit():
                break
            print("Invalid input try again")
    else:
        choice = 0

    lat = data[int(choice)]["lat"]
    lon = data[int(choice)]["lon"]

    weather_req = requests.get(OWM_URL.format(lat=lat, lon=lon, API_key=OWM_KEY, unit=UNITS[0]))
    data = weather_req.json()
    print(data["weather"][0]["description"])
    print(data["main"]["temp"], "degrees Fahrenheit")

main()