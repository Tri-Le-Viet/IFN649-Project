import threading
from MQTT_subscriber import *

def collect_data(latest_data, update, engine, topics, port, lock, logger, username, password, name):
    data = {}
    subscribers = {}
    lastUpdated = {}
    for topic in topics:
        lastUpdated[topic] = dt.datetime.now()
        data[topic] = {}
        subscriber = MQTT_subscriber(data[topic], port, lock, logger, username, password, f"{name}{topic}", threading.Event())
        subscribers.append(subscriber)
        #subscriber_thread = threading.Thread(target=subscriber)

    while True:
        for topic in topics:
            if subscribers[topic].data[1] > lastUpdated[topic]:
                pass
                #
