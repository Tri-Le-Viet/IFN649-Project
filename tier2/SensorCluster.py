import paho.mqtt.publish as publish
import bluetooth as bt
import json

class SensorCluster:
    def __init__(self, address, name, ip):
        self.address = address
        self.name = name
        self.ip = ip
        self.display = False
        self.connected = False

        if (self.address != ""):
            self.found = True
        else:
            self.found = False

    def set_address(self, address):
        self.address = address

    def connect(self):
        try:
            self.sock = bt.BluetoothSocket(bt.RFCOMM)
            self.sock.connect((self.address, 1))
            self.connected = True
            return 0
        except:
            print("Failed to connect")
            print(self.address)
            return 1


    def disconnect(self):
        try:
            sock.close()
            self.connected = False
            return 0
        except:
            return 1

    def read(self):
        msg = ""
        while(self.connected):
            byte = self.sock.recv(1)
            if byte == b"{": # new packet
                msg = byte
            elif byte == b"\n": #end of packet
                msg = msg.decode("utf-8").strip("\r")
                data = json.loads(msg)
                for entry in data:
                    publish.single(self.name+entry, data[entry], hostname=self.ip)
                if self.display:
                    print(f"{self.name} data: {data}")
            else:
                msg += byte
