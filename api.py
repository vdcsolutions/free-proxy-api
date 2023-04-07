from fastapi import FastAPI
import datetime
import json
import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

app = FastAPI()


print(os.path.dirname(os.path.realpath(__file__)))
@app.get("/proxy-list")
async def get_json_list():
    print(get_script_path())
    relative_path = 'http-proxy-list/proxy-list/data-with-geolocation.json'
    absolute_path = os.path.abspath(relative_path)
    timestamp = os.path.getmtime(absolute_path)
    last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    with open(relative_path, 'r') as f:
        json_data = json.load(f)
        for element in json_data:
            element['updated_at'] = last_modified
    return json_data
