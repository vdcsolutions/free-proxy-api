#!/bin/bash

# Check if Docker is running
if ! pgrep docker >/dev/null 2>&1 ; then
    echo "Docker is not running. Starting Docker service..."
    service docker start
fi

# Purge all Docker containers
echo "Purging all Docker containers..."
docker rm -f $(docker ps -aq) >/dev/null 2>&1

# Purge all Docker images
echo "Purging all Docker images..."
docker rmi -f $(docker images -aq) >/dev/null 2>&1

# Purge all Docker networks
echo "Purging all Docker networks..."
docker network prune -f >/dev/null 2>&1

# Create Docker network 'mynetwork'
echo "Creating Docker network 'mynetwork'..."
docker network create mynetwork >/dev/null 2>&1

# Build Docker image 'app' from the Dockerfile
echo "Building Docker image 'app'..."
docker build -t app /root/ --no-cache >/dev/null

# Run the 'app' container in 'mynetwork'
echo "Running 'app' container in 'mynetwork'..."
docker run -d -p 8000:8000 --network mynetwork --network-alias app --name app-container app >/dev/null

# Run Nginx container in 'mynetwork' with default.conf
echo "Running Nginx container in 'mynetwork'..."
docker run -d -p 80:80 --network mynetwork --name nginx-container -v /root/default.conf:/etc/nginx/conf.d/default.conf nginx >/dev/null

# Print Docker network 'mynetwork' information
echo "Docker network 'mynetwork' details:"
docker network inspect mynetwork

