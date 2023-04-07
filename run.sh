#!/bin/sh
cd /app/http_proxy_list
python main.py &
sleep 5
cd /app
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers
