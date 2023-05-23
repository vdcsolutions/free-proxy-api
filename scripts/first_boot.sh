#!/bin/bash

# Install Docker
apt-get update
apt-get install -y docker.io

# Install UFW
apt-get install -y ufw

# Allow ports in UFW
ufw allow 20
ufw allow 20/tcp
ufw allow 80
ufw allow 80/tcp
ufw allow 8000
ufw allow 8000/tcp

# Move startup_routine.sh to /etc/init.d/
cp startup_routine.sh /etc/init.d/
chmod +x /etc/init.d/startup_routine.sh


# Enable UFW at boot
ufw enable

# Reboot the server
reboot
