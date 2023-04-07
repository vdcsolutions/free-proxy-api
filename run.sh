#!/bin/sh

cd /app
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers &


while true
do
    cd /app/http_proxy_list
    echo "Deleting old data files..."
    rm proxy-list/data.txt proxy-list/data.json
    echo "Updating proxy list..."
    python main.py
    cd /app
    python add_timestamp.py
    sleep 300
done
