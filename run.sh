#!/bin/sh

cd /app
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers &
echo '[  {    "message": "JUST WOKE UP! I AM COOKING FIRST BATCH OF DELICIOUS FREE PROXIES FOR YOU RIGHT NOW, SO CHECK AGAIN IN FEW MINUTES!"  }]' > http-proxy-list/proxy-list/data-with-geolocation.json
echo '[  {    "message": "JUST WOKE UP! I AM COOKING FIRST BATCH OF DELICIOUS FREE PROXIES FOR YOU RIGHT NOW, SO CHECK AGAIN IN FEW MINUTES!"  }]' > http-proxy-list/proxy-list/dumped_data.json

while true
do
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$timestamp: Starting update process"
    cd /app/http-proxy-list
    echo "$timestamp: Fetching new proxy data"
    python main.py >/dev/null 2>&1
    cd /app
    echo "$timestamp: Updating timestamp and deleting old entries"
    echo "$timestamp: Updating timestamp and deleting old entries"
    python update_data.py
    sleep 300
    echo "$timestamp: Removing unused proxy data files"
done
