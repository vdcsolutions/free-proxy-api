import os
import json
import datetime

data_file_path = os.path.abspath("http_proxy_list/proxy-list/data-with-geolocation.json")

with open(data_file_path, "r+") as f:
    data = json.load(f)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for element in data:
        if "updated_at" not in element:
            element["updated_at"] = now

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()