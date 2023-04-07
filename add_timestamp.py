import os
import json
import datetime


relative_path = 'http_proxy_list/proxy-list/data-with-geolocation.json'
absolute_path = os.path.abspath(relative_path)

with open(absolute_path, "r+") as f:
    data = json.load(f)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_data = []
    for element in data:
        if "updated_at" not in element:
            element["updated_at"] = now
            updated_data.append(element)
        else:
            updated_at = datetime.datetime.strptime(element["updated_at"], "%Y-%m-%d %H:%M:%S")
            if (now - updated_at) <= datetime.timedelta(hours=24):
                updated_data.append(element)

    f.seek(0)
    json.dump(updated_data, f, indent=4)
    f.truncate()