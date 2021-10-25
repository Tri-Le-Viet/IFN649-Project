import os
from dotenv import load_dotenv
import logging
import logging.config

from SensorNode import *
from API import *
from bluetooth_functions import search_devices
from user_input import *


def weather_thread(threads, weatherAPI):
    weather = threading.Thread(target=weatherAPI.fetch)
    weather.start()
    threads[-1] = weather

load_dotenv()
try:
    topicBase = os.environ["TOPIC_NAME"]
    apikey = os.environ["WEATHER_API_KEY"]
    ip = os.environ["SERVER_IP"]
    port = int(os.environ["PORT"])
    location = os.environ["LOCATION"]
    clusterNames = os.environ["CLUSTER_NAMES"].split(" ")
    numNodes = len(clusterNames)
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    encryptionKey = os.environ["ENC_KEY"]
except KeyError:
    print("Missing environment variables, check .env before running")
    exit()

addresses = [""] * numNodes
threads = [None] * (numNodes + 1)
clusters = [None] * numNodes
search_devices(clusterNames, addresses)

lock = threading.Lock()
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")

for i in range(numNodes):
    clusters[i] = SensorNode(topicBase, ip, port, lock, logger, username, password,
        clusterNames[i], addresses[i], encryptionKey)
    clusters[i].connect()
    newThread = threading.Thread(target=clusters[i].read)
    newThread.start()
    threads[i] = newThread

params = {"key":apikey, "q":location}
weatherAPI = API(topicBase, ip, port, lock, logger, username, password, "weather_API",
    "http://api.weatherapi.com/v1/current.json", params)
weather_thread(threads, weatherAPI)

if __name__ == "__main__":
    while True:
        handle_input(threads, clusters, weatherAPI, lock, logger)
