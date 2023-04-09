import argparse
import json
import time
import os
import logging

# Set up the logger
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('__update_data__')


def add_timestamp(file):
    logger.info(f"Adding timestamp to {file.name}")
    data = json.load(file)
    for item in data:
        if 'timestamp' not in item:
            item['timestamp'] = int(time.time())
        item['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()
    logger.info(f"Timestamp added to {file.name}")
    return data


def remove_duplicates_by_ip(data):
    logger.info("Removing duplicate entries by IP address")
    ips = set()
    result = []
    for entry in data:
        ip = entry['ip']
        if ip not in ips:
            result.append(entry)
            ips.add(ip)
    logger.info("Duplicate entries removed")
    return result


def remove_old_dicts(data, time_threshold=86400):
    logger.info(f"Removing entries older than {time_threshold} seconds")
    now = time.time()
    result = []
    for entry in data:
        timestamp = entry['timestamp']
        if now - timestamp <= time_threshold:
            result.append(entry)
    logger.info(f"{len(data) - len(result)} entries removed")
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
        logger.error('Error: Please provide a file argument.')
        return

    # Check if file exists
    if not os.path.isfile(file_path):
        logger.error(f"File '{file_path}' not found.")
        return

    logger.info(f"Processing file {file_path}")

    # Open the file and apply the timestamp
    with open(file_path, 'r+') as f:
        data = add_timestamp(f)

    dump_filepath = file_path.rstrip(file_path.split('/')[-1]) + 'dumped_data.json'
    if not os.path.isfile(dump_filepath):
        with open(dump_filepath, 'w') as f:
            json.dump([], f)

    logger.info(f"Dump file '{dump_filepath}' loaded")

    with open(dump_filepath, 'r+') as f:
        old_data = json.load(f)

    data.extend(old_data)

    if args.delete_after:
        logger.info(f"Removing entries older than {args.delete_after} hours")
        data = remove_old_dicts(data, args.delete_after * 3600)
    else:
        logger.info("No time threshold specified, keeping all entries")
        data = remove_old_dicts(data)

    data = remove_duplicates_by_ip(data)

    with open(dump_filepath, 'w') as f:
        json.dump(data, f)

    logger.info(f"{len(data)} entries saved to {dump_filepath}")


if __name__ == '__main__':
    main()