#!/bin/sh

cd /app
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers &
python add_timestamp.py

while true
do
    cd /app
    cd /app/http_proxy_list
    rm proxy-list/data.txt proxy-list/data.json
    python main.py >/dev/null 2>&1
    python add_timestamp.py
    sleep 300
done
