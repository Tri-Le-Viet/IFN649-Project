import bluetooth as bt
import json
import time
from MQTT_client import *

class SensorCluster(MQTT_publisher):
    def __init__(self, topicBase, ip, port, lock, logger, username, password, name, address):
        super().__init__(topicBase, ip, port, lock, logger, username, password, name)
        self.address = address
        self.connected = False
        self.found = (self.address != "")

    def set_address(self, address):
        self.address = address
        self.found = True

    def connect(self):
        if not self.found:
            log(self.lock, self.logger.error, f"{self.name} - Need to know address before connecting")
            return 2

        try:
            self.sock = bt.BluetoothSocket(bt.RFCOMM)
            self.sock.connect((self.address, 1))
            self.connected = True
            log(self.lock, self.logger.info, f"Successfully connected to {self.name}")
            return 0
        except Exception as e:
            print(e)
            log(self.lock, self.logger.error, f"Failed to connect to {self.name}")
            return 1

    def disconnect(self):
        if not self.running:
            log(self.lock, self.logger.info, f"{self.name} - Already disconnected")
            return 2

        try:
            sock.close()
            self.connected = False
            log(self.lock, self.logger.info, f"Successfully disconnected from {self.name}")
            return 0
        except:
            log(self.lock, self.logger.error, f"Failed to disconnect from {self.name}")
            return 1

    def read(self):
        msg = ""
        while not self.running.is_set():
            if self.connected:
                try:
                    byte = self.sock.recv(1)
                    if byte == b"{": # new packet
                        msg = byte
                    elif byte == b"\n": #end of packet
                        msg = msg.decode("utf-8").strip("\r")
                        log(self.lock, self.logger.info, f"Received data from {self.name}")
                        data = json.loads(msg)
                        for entry in data:
                            topic = f"{self.topicBase}{entry}"
                            rc = self.mqttc.publish(topic, data[entry])[0]
                            self.log_publish(rc, topic)
                        if self.display:
                            print(f"{self.name} data: {data}")
                        msg = ""
                    else:
                        msg += byte
                except:
                    self.connected = False
                    log(self.lock, self.logger.error, f"Lost connection to {self.name}")

            elif not self.found:
                pass
            else: #attempt to reconnect if disconnected
                log(self.lock, self.logger.error, f"Attempting to reconnect to {self.name}")
                if(self.connect() != 0):
                    time.sleep(10) #wait 10 seconds and try again
