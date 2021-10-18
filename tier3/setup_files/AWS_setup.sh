#!/bin/bash
sudo amazon-linux-extras install -y epel
sudo yum update -y -q
sudo yum install -y -q mosquitto
sudo yum install -y -q mariadb-server
sudo yum install -y -q nginx

#NOTE: please change the passwords from default values before implementing
touch passwd
mosquitto_passwd -b passwd publisher 1234
mosquitto_passwd -b passwd subscriber 5678
chmod 600 passwd
sudo mv passwd /etc/mosquitto

printf "user publisher\ntopic write #\nuser subscriber\ntopic read #"> acl
sudo mv acl /etc/mosquitto

#CA key (ca.key)
openssl genrsa -des3 -out ca.key 2048

#CA certificate (ca.crt)
#NOTE: remember to use host name not ip
# can get host name by using command host public_ip_address
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt

#Broker key pair (server.key)
openssl genrsa -out server.key 2048

#Certificate request (server.csr)
openssl req -new -out server.csr -key server.key

#Sign certificate (server.crt)
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

#move ca.crt, server.crt and server.key to certs directory
#also copy them to client

sudo mkdir /etc/mosquitto/certs
sudo mv ca.crt /etc/mosquitto/certs
sudo mv server.crt /etc/mosquitto/certs
sudo mv server.key /etc/mosquitto/certs

sudo systemctl start mosquitto # maybe comment out this to setup .conf file first
sudo systemctl enable mosquitto

sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mysql_secure_installation

sudo mkdir /etc/nginx/sites-available
sudo mkdir /etc/nginx/sites-enabled

#python setup in virtual environment
mkdir app_folder
cd app_folder
python3 -m venv app_environment
source app_environment/bin/activate
cd app_environment
pip3 install paho-MQTT dotenv flask SQLAlchemy gunicorn
mkdir templates