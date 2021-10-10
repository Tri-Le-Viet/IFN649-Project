#!/bin/bash

sudo amazon-linux-extras install -y epel
sudo yum update -y -q
sudo yum install -y -q mosquitto
sudo yum install -y -q mysql-server
sudo yum install -yq mysql-community-server

pip3 install paho-MQTT
pip3 install dotenv
pip3 install requests
pip3 install pyserial
pip3 install flask

#NOTE: please change the passwords from default values before implementing
#TODO: figure out why this doesn't work,
# command works when entered normally but not from shell script
touch passwd
mosquitto_passwd -b passwd publisher 1234
mosquitto_passwd -b passwd subscriber 5678
chmod 600 passwd
sudo mv passwd /etc/mosquitto

touch acl
echo "user publisher
topic write #
user subscriber
topic read #"> acl
sudo mv acl /etc/mosquitto


sudo systemctl start mosquitto
sudo systemctl enable mosquitto
