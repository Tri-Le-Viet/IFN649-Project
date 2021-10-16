import paho.mqtt.client as mqtt

class MQTT_subscriber:
    def __init__(self, port, lock, logger, username, password, topic):
        self.topic = topic
        mqttc = mqtt.Client()
        mqttc.username_pw_set(username=username, password=password)
        certs_dir = "/etc/mosquitto/certs"
        mqttc.tls_set(ca_certs=f"{certs_dir}/ca.crt", certfile=f"{certs_dir}server.crt", keyfile=f"{certs_dir}server.key")
        mqttc.connect("localhost", port)
