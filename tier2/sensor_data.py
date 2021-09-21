import paho.mqtt.publish as publish
import serial
import json

def process_sensor_data(ip, topicBase):
    try:
        ser = serial.Serial("/dev/rfcomm0", 9600) # TODO: change if serial is different
    except serial.serialutil.SerialException:
        print("Could not open serial port")
        exit()

    while True:
      if ser.in_waiting > 0:
        rawserial = ser.readline()
        cookedserial = rawserial.decode('utf-8').strip('\r\n')
        print(cookedserial)

    	# data from teensy is sent as JSON for easier decoding
        data = json.loads(cookedserial)
        for entry in data:
            publish.single(topicBase + entry, data[entry], hostname=ip)
