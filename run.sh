#!/bin/sh
exec uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --proxy-headers
sleep 5
python ./http_proxy_list/main.py &
