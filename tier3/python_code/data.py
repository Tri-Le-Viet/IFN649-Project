import threading
from sqlalchemy.sql import text
import time
import json
import math

from MQTT_subscriber import *

def collect_data(latest_data, update, engine, topics, hostname, port, lock, logger, username, password, name):
    formatted_name = name.replace('_', ' ')
    subscribers = {}
    lastUpdated = {}
    latest = {}
    latest_data[name] = latest
    conn = engine.connect()
    for topic in topics:
        current = dt.datetime.now()
        lastUpdated[topic] = current
        latest[topic] = None
        subscriber = MQTT_subscriber([None, current], hostname, port, lock, logger, username, password, f"{name}/{topic}")
        subscribers[topic] = subscriber
        sub_thread = threading.Thread(target=subscriber.conn)
        sub_thread.start()

    current = dt.datetime.now()
    lastUpdated["API"] = current
    latest["API"] = {}
    latest["Dew Point"] = None
    APISubscriber = MQTT_subscriber([None, current], hostname, port, lock, logger, username, password, f"{name}/API")
    sub_thread = threading.Thread(target=APISubscriber.conn)
    sub_thread.start()

    while True:
        updated = False
        for topic in topics:
            updateTime = subscribers[topic].data[1]
            if updateTime > lastUpdated[topic]:
                updated = True
                lastUpdated[topic] = updateTime
                latest[topic] = subscribers[topic].data[0] # update datalist

        updateTime = APISubscriber.data[1]
        if updateTime > lastUpdated["API"]:
            updated = True
            lastUpdated[topic] = updateTime
            latest["API"] = json.loads(APISubscriber.data[0])

        if updated:
            if latest["Temperature"] and latest["Humidity"]:
                latest["Dew Point"] = 17.271 * latest["Temperature"] / (237.7 + latest["Temperature"] + math.log(latest["Humidity"] / 100))

            update.set()
            query =  text("INSERT INTO weather_data VALUES (:a, :b, :c, :d, :e, :f, :g, :h)")
            #TODO: fix query
            #conn.execute(query, a=dt.datetime.now(), b=formatted_name, c=latest["Temperature"],
            #    d=latest["Humidity"], e=latest["Heat Index"], f=latest["Dew Point"],
                #g=latest["Heading"], h=latest["Windspeed"])

            time.sleep(10)
