import argparse
import json
import time
import os


def add_timestamp(file):
    data = json.load(file)
    for item in data:
        if 'timestamp' not in item:
            item['timestamp'] = int(time.time())
        item['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()
    return data

import time

def remove_duplicates_by_ip(data):
    ips = set()
    result = []
    for entry in data:
        ip = entry['ip']
        if ip not in ips:
            result.append(entry)
            ips.add(ip)
    return result

def remove_old_dicts(data, time_threshold=86400):
    now = time.time()
    result = []
    for entry in data:
        timestamp = entry['timestamp']
        if now - timestamp <= time_threshold:
            result.append(entry)
    return result




def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process JSON file with timestamps')

    # Add the filepath argument
    parser.add_argument('--filepath', type=str, help='Path to the JSON file')
    parser.add_argument('--delete_after', type=int, default=24, help='Hours before deleting proxy, defaults to 24hour')

    # Parse the command line arguments
    args = parser.parse_args()

    # Check if the file argument was provided
    if args.filepath:
        file_path = args.filepath
    else:
        print('Error: Please provide a file argument.')
        return

    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        return

    # Open the file and apply the timestamp
    with open(file_path, 'r+') as f:
        data = add_timestamp(f)

    dump_filepath = file_path.rstrip(file_path.split('/')[-1])+'dumped_data.json'
    if not os.path.isfile(dump_filepath):
         with open(dump_filepath, 'w') as f:
             json.dump([], f)
    with open(dump_filepath, 'r+') as f:
        json.dump(data, f)
    with open(dump_filepath, 'r+') as f:
        old_data = json.load(f)

    if args.delete_after:
        remove_old_dicts(old_data,args.delete_after*3600)
    else:

        remove_old_dicts(old_data)
    remove_duplicates_by_ip(old_data)

    with open(dump_filepath, 'w') as f:
        json.dump(old_data,f)

main()
