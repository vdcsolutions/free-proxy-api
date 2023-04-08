from fastapi import FastAPI
import json
import os
import argparse
import logging

app = FastAPI()

# Set up the argument parser


# Set up the logger
logging.basicConfig(filename='logs.log',level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/live-proxy-list")
async def get_newest_proxies():
    with open(os.path.abspath('http_proxy_list/proxy-list/data-with-geolocation.json'), "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            # Find the newest timestamp in the data
            newest_timestamp = max(d.get("timestamp", 0) for d in data)

            # Filter out dictionaries that have an old timestamp
            filtered_data = [d for d in data if d.get("timestamp", 0) == newest_timestamp]

            return filtered_data
        else:
            return data

@app.get("/proxy-list")
async def get_proxy_list():
    with open(os.path.abspath('http_proxy_list/proxy-list/dumped_data.json'), 'r') as f:
        json_data = json.load(f)

    return json_data