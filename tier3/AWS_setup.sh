#!/bin/bash

sudo amazon-linux-extras install -y epel
sudo yum update -y -q
sudo yum install -y -q mosquitto
sudo yum install -y -q mysql-server

pip3 install paho-MQTT
pip3 install dotenv
pip3 install requests
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


#TODO: fix ssl stuff
#CA key (ca.key)
openssl genrsa -des3 -out ca.key 2048

#CA certificate (ca.crt)
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt

#
#Broker key pair (server.key)
openssl genrsa -out server.key 2048

#Certificate request (server.csr)
openssl req -new -out server.csr -key server.key

#Sign certificate (server.crt)
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

#move ca.crt to ca_certificates and server.crt and server.key to certs directory

mkdir /etc/mosquitto/certs
sudo mv ca.crt /etc/mosquitto/certs
sudo mv server.crt /etc/mosquitto/certs
sudo mv server.key /etc/mosquitto/certs


sudo systemctl start mosquitto
sudo systemctl enable mosquitto
