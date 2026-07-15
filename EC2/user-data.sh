#!/bin/bash

# updating ubuntu packages
apt update -y

# upgrading ubuntu packages and dependencies 
apt upgrade -y 

# installing and starting a nginx server
apt install nginx -y

systemctl start nginx 

systemctl enable nginx