import threading
from sqlalchemy.sql import text
import time

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

    while True:
        updated = False
        for topic in topics:
            updateTime = subscribers[topic].data[1]
            if updateTime > lastUpdated[topic]:
                updated = True
                lastUpdated[topic] = updateTime
                latest[topic] = subscribers[topic].data[0] # update datalist

        if updated:
            latest["Dew Point"] = 5.0 #TODO: add calculation here
            update.set()
            #TODO remove underscore from Heat Index
            query =  text("INSERT INTO weather_data VALUES (:a, :b, :c, :d, :e, :f, :g, :h, :i, :j)")
            #TODO: fix query
            #conn.execute(query, a=dt.datetime.now(), b=formatted_name, c=latest["Temperature"],
            #    d=latest["Humidity"], e=latest["Heat_Index"], f=latest["Dew Point"],
                #g=latest["Heading"], h=latest["Windspeed"], i=None, j=None) #TODO add i and j

            time.sleep(10)
