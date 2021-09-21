import os
from dotenv import load_dotenv
import requests
import time
import threading
from sensor_data import *

# all topics follow format IFN649/Group21/topic_name
topicBase = "IFN649/Group21/"

load_dotenv()
try:
  apikey = os.environ["WEATHER_API_KEY"]
  ip = os.environ["SERVER_IP"]
  location = os.environ["LOCATION"]
except KeyError:
  print("Missing environment variables, check env_vars.env before running")
  exit()

params = {
    "key":apikey,
    "q":location
    } #TODO: figure out what params are needed

numSensors = 1
threads = []
for sensor in range(numSensors):
    newThread = threading.Thread(target=process_sensor_data, args=(ip, topicBase, sensor))
    newThread.start()
    threads.append(newThread)

while True:
    res = requests.get("http://api.weatherapi.com/v1/current.json", params=params) #TODO: add error handling
    weatherData = res.json()
    print(weatherData)
    #send data to mqtt (for testing just print is good enough)
    time.sleep(300) #TODO: adjust time
