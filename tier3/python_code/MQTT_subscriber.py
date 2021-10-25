import paho.mqtt.client as mqtt
import datetime as dt

class MQTT_subscriber:
    def __init__(self, data, hostname, port, lock, logger, username, password, topic):
        self.topic = topic
        self.data = data
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(username=username, password=password)
        self.mqttc.tls_set(ca_certs="/etc/mosquitto/certs/ca.crt")
        self.mqttc.on_connect = self.subcscribe
        self.mqttc.on_message = self.read
        self.mqttc.connect(hostname, port)


    def subcsribe(self, client, userdata, flags, rc):
        self.mqttc.subscribe(self.topic)


    def read(self, client, userdata, msg):
        contents = msg.payload.decode('utf-8')
        try:
            value = float(contents)
            self.data = [value, dt.datetime.now()]
        except ValueError:
            pass
