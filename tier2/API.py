import paho.mqtt.publish as publish
import threading
import requests
import time

class API:
    def __init__(self, link, params):
        self.link = link
        self.params = params
        self.display = False
        self.running = threading.Event()

    def fetch(self):
        while not self.running.is_set():
            res = requests.get(self.link, params=self.params) #TODO: add error handling
            weatherData = res.json()
            

            if (self.display):
                print(weatherData)


            time.sleep(300) #TODO: adjust time
