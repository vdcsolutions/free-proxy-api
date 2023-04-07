from fastapi import FastAPI
import json
import os


app = FastAPI()

relative_path = 'http_proxy_list/proxy-list/data-with-geolocation.json'
absolute_path = os.path.abspath(relative_path)


@app.get("/live-proxy-list")
async def get_json_list():
    with open(absolute_path, 'r') as f:
        json_data = json.load(f)

    try:
        max_updated_at = max(element.get('updated_at', '') for element in json_data)
        most_recent_dicts = [element for element in json_data if element.get('updated_at', '') == max_updated_at]
    except:
        most_recent_dicts = []

    return most_recent_dicts

@app.get("/proxy-list")
async def get_proxy_list():
    with open(absolute_path, 'r') as f:
        json_data = json.load(f)

    return json_data