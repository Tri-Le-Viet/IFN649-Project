import paho.mqtt.publish as publish
import bluetooth as bt
import json

class SensorCluster:
    def __init__(self, address, name, topic, ip, lock, logger):
        self.address = address
        self.name = name
        self.topic = topic
        self.ip = ip
        self.display = False
        self.connected = False
        self.running = True
        self.found = (self.address != "")
        self.lock = lock
        self.logger = logger

    def set_address(self, address):
        self.address = address
        self.found = True

    def connect(self):
        if not self.found:
            return 2

        try:
            self.sock = bt.BluetoothSocket(bt.RFCOMM)
            self.sock.connect((self.address, 1))
            self.connected = True
            self.log(self.logger.info, f"Successfully connected to {self.name}")
            return 0
        except:
            self.log(self.logger.error, f"Failed to connect to {self.name}")
            return 1

    def disconnect(self):
        if not self.running:
            return 2

        try:
            sock.close()
            self.connected = False
            return 0
        except:
            return 1

    def read(self):
        msg = ""
        while(self.running):
            if self.connected:
                try:
                    byte = self.sock.recv(1)
                    if byte == b"{": # new packet
                        msg = byte
                    elif byte == b"\n": #end of packet
                        msg = msg.decode("utf-8").strip("\r")
                        self.log(self.logger.info, f"Received data from {self.name}")
                        data = json.loads(msg)
                        for entry in data:
                            publish.single(f"{self.topic}/{entry}", data[entry], hostname=self.ip) #TODO: add auth
                        if self.display:
                            print(f"{self.name} data: {data}")
                    else:
                        msg += byte
                except:
                    self.connected = False
                    self.log(self.logger.error, f"Lost connection to {self.name}")
            else: #attempt to reconnect if disconnected
                self.log(self.logger.error, f"Attempting to reconnect to {self.name}")
                self.connect()

    def log(self, func, message):
        with self.lock:
            func(message)
