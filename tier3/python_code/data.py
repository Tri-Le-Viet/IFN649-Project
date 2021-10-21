import threading
from sqlalchemy.sql import text

from MQTT_subscriber import *

def collect_data(latest_data, update, engine, topics, port, lock, logger, username, password, name):
    data = {}
    subscribers = {}
    lastUpdated = {}
    conn = engine.connect()
    for topic in topics:
        lastUpdated[topic] = dt.datetime.now()
        data[topic] = {}
        subscriber = MQTT_subscriber(data[topic], port, lock, logger, username, password, f"{name}{topic}", threading.Event())
        subscribers.append(subscriber)
        #subscriber_thread = threading.Thread(target=subscriber)

    while True:
        for topic in topics:
            updateTime = subscribers[topic].data[1]
            if updateTime > lastUpdated[topic]:
                lastUpdated[topic] = updateTime
                latest_data[name][topic] = subscribers[topic].data[0] # update data

                #insert into db
                query =  text("INSERT INTO weather_data (:a, :b, :c, :d, :e, :f, :g, :h, :i)")
                conn.execute(query) #TODO: insert data or None if data is blank
