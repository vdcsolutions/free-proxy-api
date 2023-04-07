#!/bin/sh
python /app/http_proxy_list/main.py &
sleep 5
exec /opt/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers
