from mqtt_functions import *

class MQTT_client:
    def __init__(self, topicBase, ip, lock, logger, username, password, name):
        self.ip = ip
        self.lock = lock
        self.logger = logger
        self.display = False
        self.running = threading.Event()
        self.name = name
        self.mqttc = mqtt.Client(userdata={"logger":logger,"lock":lock, "name":name})
        self.mqttc.username_pw_set(username=username, password=password)
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.connect(ip, port)

    def shutdown(self):
        self.mqttc.wait_for_publish()
        self.mqttc.disconnect()

    def log_publish(self, rc, topic):
        if rc == 0:
            log(self.lock, self.logger.info, f"Successfully published to {topic}")
        else:
            log(self.lock, self.logger.error, f"Failed to publish to {topic}")
