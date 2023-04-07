from fastapi import FastAPI
import datetime
import json
import os

app = FastAPI()


@app.get("/proxy-list")
async def get_json_list():
    relative_path = 'http_proxy_list/proxy-list/data-with-geolocation.json'
    absolute_path = os.path.abspath(relative_path)
    print(absolute_path)
    print(relative_path)
    timestamp = os.path.getmtime(absolute_path)
    last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    with open(absolute_path, 'r') as f:
        json_data = json.load(f)
        for element in json_data:
            element['updated_at'] = last_modified
    return json_data
