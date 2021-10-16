import threading
from MQTT_subscriber import MQTT_subscriber

def collect_data(latest_data, update, engine, topics, port, lock, logger, username, password, name):
    for topic in topics:
        subscriber = MQTT_subscriber(port, lock, logger, username, password, f"{name}{topic}")
        subscriber_thread = threading.Thread(target=subscriber)
