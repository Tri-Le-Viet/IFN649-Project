import paho.mqtt.publish as publish
import threading
import requests
import time

class API:
    def __init__(self, link, params, topicBase, ip, lock, logger):
        self.link = link
        self.params = params
        self.topicName = topicBase + "/API_data"
        self.ip = ip
        self.lock = lock
        self.logger = logger

        self.display = False
        self.running = threading.Event()


    def fetch(self):
        while not self.running.is_set():
            try:
                res = requests.get(self.link, params=self.params)

                if (res.status_code == 200):
                    weatherData = res.json()

                    publish.single(self.topicName, hostname=self.ip) #TODO: add auth

                    if (self.display):
                        print(weatherData)

                else:
                    self.log(self.logger.error, f"Request to weather API failed with status {res.status_code}")
            except:
                self.log(self.logger.error, f"Could not connect to {self.link}")
            time.sleep(100) #TODO: adjust time for final

    def log(self, func, message):
        with self.lock:
            func(message)
