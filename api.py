from fastapi import FastAPI
import json
import os
import logging
from fastapi import FastAPI, Request


app = FastAPI()

# Set up the argument parser


# Set up the logger
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


@app.get("/live-proxy-list")
async def get_newest_proxies(request: Request):
    logger.info(f"Request received from {request.client.host} to get newest proxies")

    with open(os.path.abspath('http_proxy_list/proxy-list/data-with-geolocation.json'), "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            # Find the newest timestamp in the data
            newest_timestamp = max(d.get("timestamp", 0) for d in data)

            # Filter out dictionaries that have an old timestamp
            filtered_data = [d for d in data if d.get("timestamp", 0) == newest_timestamp]

            logger.info(f"{len(filtered_data)} newest proxies returned to {request.client.host}")
            return filtered_data
        else:
            logger.error(f"Error: data is not a list, request from {request.client.host}")
            return data


@app.get("/proxy-list")
async def get_proxy_list(request: Request):
    logger.info(f"Request received from {request.client.host} to get proxy list")

    with open(os.path.abspath('http_proxy_list/proxy-list/dumped_data.json'), 'r') as f:
        json_data = json.load(f)

    logger.info(f"{len(json_data)} proxies returned to {request.client.host}")
    return json_data
