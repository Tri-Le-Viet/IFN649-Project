import paho.mqtt.client as mqtt
import threading
from mqtt_functions import *

class MQTT_publisher:
    def __init__(self, topicBase, ip, port, lock, logger, username, password, name):
        self.topicBase = topicBase
        self.ip = ip
        self.port = port
        self.lock = lock
        self.logger = logger
        self.display = False
        self.running = threading.Event()
        self.name = name
        mqttc = mqtt.Client(userdata={"logger":logger,"lock":lock, "name":name})
        mqttc.username_pw_set(username=username, password=password)
        mqttc.tls_set("certs/ca.crt")
        mqttc.on_connect = on_connect
        mqttc.on_disconnect = on_disconnect
        mqttc.connect(ip, port)
        self.mqttc = mqttc


    def log_publish(self, rc, topic):
        if rc == 0:
            log(self.lock, self.logger.info, f"Successfully published to {topic}")
        else:
            log(self.lock, self.logger.error, f"Failed to publish to {topic}")
