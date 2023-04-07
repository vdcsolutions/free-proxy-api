from fastapi import FastAPI
import datetime
import json
import os
import threading

app = FastAPI()


@app.get("/proxy-list")
async def get_json_list():
    relative_path = 'http_proxy_list/proxy-list/data-with-geolocation.json'
    absolute_path = os.path.abspath(relative_path)

    timestamp = os.path.getmtime(absolute_path)
    last_modified = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    with open(absolute_path, 'r+') as f:
        json_data = json.load(f)
        updated_json_data = []
        for element in json_data:
            if 'updated_at' in element:
                # Check if the element is older than 24 hours
                updated_at = datetime.datetime.strptime(element['updated_at'], '%Y-%m-%d %H:%M:%S')
                if now - updated_at > datetime.timedelta(hours=24):
                    continue
            else:
                element['updated_at'] = last_modified
                updated_json_data.append(element)

    return updated_json_data


# Function to run the dump loop in a separate thread
def dump_loop():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            with open(absolute_path, 'r+') as f:
                json_data = json.load(f)
                # Filter out elements older than 24 hours
                updated_json_data = [element for element in json_data if 'updated_at' in element]
                json.dump(updated_json_data, f, indent=4)
        time.sleep(60)


# Start the dump loop thread
dump_thread = threading.Thread(target=dump_loop)
dump_thread.start()
