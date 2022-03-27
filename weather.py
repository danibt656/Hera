# importing modules
import requests, json

# API base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# City Name
CITY = "Madrid"

# Your API key
API_KEY = "d9eabd7a98b614cff8a11b7e4b2ba540"

# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

# Sending HTTP request
response = requests.get(URL)

print(response.status_code)
# checking the status code of the request
if response.status_code == 200:
    
   # retrieving data in the json format
   data = response.json()
   
   # take the main dict block
   main = data['main']
   
   # getting temperature
   temperature = main['temp']
   # getting feel like
   temp_feel_like = main['feels_like']  
   # getting the humidity
   humidity = main['humidity']
   # getting the pressure
   pressure = main['pressure']
   
   # weather report
   weather_report = data['weather']
   # wind report
   wind_report = data['wind']
   
   print(f"{CITY:-^35}")
   print(f"City ID: {data['id']}")   
   print(f"Temperature: {temperature}")
   print(f"Feel Like: {temp_feel_like}")    
   print(f"Humidity: {humidity}")
   print(f"Pressure: {pressure}")
   print(f"Weather Report: {weather_report[0]['description']}")
   print(f"Wind Speed: {wind_report['speed']}")
   print(f"Time Zone: {data['timezone']}")
else:
   # showing the error message
   print("Error in the HTTP request")