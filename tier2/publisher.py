import os
from dotenv import load_dotenv
import threading
import logging
import logging.config

from SensorCluster import *
from API import *
from bluetooth_functions import search_devices
from user_input import *


def weather_thread(threads, weatherAPI):
    weather = threading.Thread(target=weatherAPI.fetch)
    weather.start()
    threads[-1] = weather

if __name__ == "__main__":
    load_dotenv()
    try:
        topicBase = os.environ["TOPIC_NAME"]
        apikey = os.environ["WEATHER_API_KEY"]
        ip = os.environ["SERVER_IP"]
        location = os.environ["LOCATION"]
        clusterNames = os.environ["CLUSTER_NAMES"].split(" ")
        numClusters = len(clusterNames)
        params = {"key":apikey, "q":location}
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
    except KeyError:
        print("Missing environment variables, check .env before running")
        exit()

    addresses = [""] * numClusters
    threads = [None] * (numClusters + 1)
    clusters = [None] * numClusters
    search_devices(clusterNames, addresses)

    lock = threading.lock()
    logging.config.fileConfig("logger.conf")
    logger = logging.getLogger("root")

    for i in range(numClusters):
        clusters[i] = SensorCluster(topicBase, ip, lock, logger, username, password,
            addresses[i], clusterNames[i])
        clusters[i].connect()
        newThread = threading.Thread(target=clusters[i].read)
        newThread.start()
        threads[i] = newThread

    weatherAPI = API(topicBase, ip, lock, logger, username, password,
        "http://api.weatherapi.com/v1/current.json", params, "weather_API")
    weather_thread(threads, weatherAPI)

    while True:
        handle_input(threads, clusters, weatherAPI, lock, logger)
