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
            res = requests.get(self.link, params=self.params)

            if (res.status_code == 200):
                weatherData = res.json()
                if (self.display):
                    print(weatherData)

            else: #TODO add error logging
                pass
            time.sleep(100) #TODO: adjust time for final
