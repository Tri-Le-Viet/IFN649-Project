import threading
from sqlalchemy.sql import text
import time

from MQTT_subscriber import *

def collect_data(latest_data, update, engine, topics, hostname, port, lock, logger, username, password, name):
    data = {}
    subscribers = {}
    lastUpdated = {}
    conn = engine.connect()
    for topic in topics:
        lastUpdated[topic] = dt.datetime.now()
        data[topic] = {}
        subscriber = MQTT_subscriber(data[topic], hostname, port, lock, logger, username, password, f"{name}{topic}")
        subscribers.append(subscriber)

    while True:
        updated = False
        for topic in topics:
            updateTime = subscribers[topic].data[1]
            if updateTime > lastUpdated[topic]:
                updated = True
                lastUpdated[topic] = updateTime
                latest_data[name][topic] = subscribers[topic].data[0] # update datalist

        if updated:
            latest_data["Dew point"] = 5 #TODO: add calculation here
            update.set()
            query =  text("INSERT INTO weather_data (:a, :b, :c, :d, :e, :f, :g, :h)")
            conn.execute(query, a=dt.datetime.now(), b=name, c=latest_data["Temperature"],
                d=latest_data["Humidity"], e=latest_data["Heat Index"], f=latest_data["Dew Point"],
                g=latest_data["Heading"], h=latest_data["Wind Speed"])

            time.sleep(10)
