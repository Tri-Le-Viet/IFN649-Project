#!/bin/bash

sudo amazon-linux-extras install -y epel
sudo yum update -yq
sudo yum install -yq mosquitto
sudo yum install -yq mysql-server
sudo yum install -yq node-js
sudo systemctl start mosquitto
sudo systemctl enable mosquitto


pip3 install paho-MQTT
pip3 install dotenv
pip3 install requests
pip3 install pyserial
pip3 install flask


py = "/python_files/"*.py
chmod +x $py

chmod +x "sql_setup.sh"
