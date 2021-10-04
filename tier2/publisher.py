import os
from dotenv import load_dotenv
import threading
#import bluetooth as bt

from SensorCluster import *
from API import *



def weather_thread(threads, weatherAPI):
    weather = threading.Thread(target=API.fetch())
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
    except KeyError:
        print("Missing environment variables, check .env before running")
        exit()

    addresses = [""] * numClusters
    threads = [None] * (numClusters + 1)
    clusters = [None] * numClusters
    search_devices(clusterNames, addresses)

    for i in range(numClusters):
        clusters[i] = SensorCluster(addresses[i], clusterNames[i], ip)
        clusters[i].connect()
        newThread = threading.Thread(target=clusters[i].read())
        newThread.start()
        threads[i] = newThread

    weatherAPI = API("http://api.weatherapi.com/v1/current.json", params)
    weather_thread(weatherAPI)

    while True:
        handle_input(threads, clusters)
