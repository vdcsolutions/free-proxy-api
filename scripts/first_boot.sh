#!/bin/bash

# Install Docker
apt-get update
apt-get install -y docker.io

# Move startup_routine.sh to /etc/init.d/
mv startup_routine.sh /etc/init.d/
chmod +x /etc/init.d/startup_routine.sh

# Reboot the server
reboot
