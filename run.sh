#!/bin/sh

cd /app
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers &

cd /app/http_proxy_list
while true
do
    echo "Updating proxy list..."
    python main.py
    sleep 300
done
