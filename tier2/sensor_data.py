import paho.mqtt.publish as publish
import serial #is this necessary?
#import bluetooth as bt
import json

def process_sensor_data(sock, ip, topicBase, num):
    while True:
      if ser.in_waiting > 0:
        rawserial = ser.readline()
        cookedserial = rawserial.decode('utf-8').strip('\r\n')
        print(cookedserial)

        #TODO: add crypto and integrity checking

    	# data from teensy is sent as JSON for easier decoding
        data = json.loads(cookedserial)
        for entry in data:
            publish.single(topicBase + entry, data[entry], hostname=ip)


def new():
    print("Searching for sensors")
    devices = bt.discover
