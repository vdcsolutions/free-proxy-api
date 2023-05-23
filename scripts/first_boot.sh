#!/bin/bash

# Install Docker
apt-get update
apt-get install -y docker.io

# Install UFW
apt-get install -y ufw

# Allow ports in UFW
ufw allow 80
ufw allow 80/tcp
ufw allow 8000
ufw allow 8000/tcp

# Enable UFW at boot
ufw enable

# Move startup_routine.sh to /etc/init.d/
mv startup_routine.sh /etc/init.d/
chmod +x /etc/init.d/startup_routine.sh

# Reboot the server
reboot
