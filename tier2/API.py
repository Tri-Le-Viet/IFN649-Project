import paho.mqtt.client as mqtt
import threading
import requests
import time
from mqtt_functions import mqtt_connect

class API:
    def __init__(self, link, params, topicBase, ip, lock, logger, username, password, name):
        self.link = link
        self.params = params

        self.ip = ip
        self.lock = lock
        self.logger = logger

        self.display = False
        self.running = threading.Event()

        self.mqttc = mqtt.Client(userdata={"logger":logger,"lock":lock})
        mqtt.connect(self.mqttc, username, password, ip)

        self.link = link
        self.params = params

    def fetch(self):
        while not self.running.is_set():
            try:
                res = requests.get(self.link, params=self.params)

                if (res.status_code == 200):
                    weatherData = res.json()
                    topic = f"{self.topicBase}{self.name}"
                    rc = self.mqttc.publish(topic, hostname=self.ip)
                    self.log_publish(rc, topic)

                    if (self.display):
                        print(weatherData)

                else:
                    log(self.logger.error, f"Request to weather API failed with status {res.status_code}")
            except:
                log(self.logger.error, f"Could not connect to {self.link}")
            time.sleep(100) #TODO: adjust time for final

    def log(lock, func, message):
        with lock:
            func(message)

    def on_connect(client, userdata, flags, rc):
        logger = userdata["logger"]
        lock = userdata["lock"]

        log_type = logger.info if rc == 0 else logger.critical
        log_message = mqtt_co-nnect_codes[rc]
        log(lock, log_type, log_message)
