import requests
import time
from MQTT_client import *

class API(MQTT_publisher):
    def __init__(self, topicBase, ip, port, lock, logger, username, password, name, link, params):
        super().__init__(topicBase, ip, port, lock, logger, username, password, name)
        self.link = link
        self.params = params

    def fetch(self):
        while not self.running.is_set():
            try:
                res = requests.get(self.link, params=self.params)
                if (res.status_code == 200):
                    weatherData = res.json()
                    topic = f"{self.topicBase}{self.name}"
                    rc = self.mqttc.publish(topic, str(weatherData))[0]
                    self.log_publish(rc, topic)

                    if (self.display):
                        print(weatherData)

                else:
                    log(self.lock, self.logger.error, f"Request to weather API failed with status {res.status_code}")
            except Exception as e:
                print(e)
                log(self.lock, self.logger.error, f"Could not connect to {self.link}")
            time.sleep(100) #TODO: adjust time for final
