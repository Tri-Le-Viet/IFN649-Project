#!/bin/bash

sudo amazon-linux-extras install -y epel
sudo yum update -y
sudo yum install -y mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

pip3 install paho-MQTT
pip3 install dotenv
pip3 install requests
pip3 install pyserial

sudo apt install mysql-server
