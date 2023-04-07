from fastapi import FastAPI
import os
import datetime
import json
from http_proxy_list.main import main as get_proxy_list
from http_proxy_list.sources import SOURCES

app = FastAPI()

@app.get("/proxy-list")
async def get_json_list():
    #get_proxy_list()
    relative_path = 'http-proxy-list/proxy-list/data-with-geolocation.json'
    absolute_path = os.path.abspath(relative_path)
    timestamp = os.path.getmtime(absolute_path)
    last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    with open(absolute_path, 'r') as f:
        json_data = json.load(f)
        for element in json_data:
            element['updated_at'] = last_modified
    return json_data
