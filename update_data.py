import json
import time
import os
import logging
from db_handler import DBHandler

# Set up the logger
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('__update_data__')


def add_timestamp(file_path):
    logger.info(f"Adding timestamp to {file_path}")
    with open(file_path, 'r+') as file:
        data = json.load(file)
        for item in data:
            if 'timestamp' not in item:
                item['timestamp'] = int(time.time())
            item['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    logger.info(f"Timestamp added and file saved: {file_path}")
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
    data_file_path = '/app/http-proxy-list/proxy-list/data-with-geolocation.json'
    dump_file_path = os.path.join(os.path.dirname(data_file_path), 'dumped_data.json')

    # Check if data file exists
    if not os.path.isfile(data_file_path):
        logger.error(f"Data file '{data_file_path}' not found.")
        return

    # Check if dump file exists
    if not os.path.isfile(dump_file_path):
        logger.error(f"Dump file '{dump_file_path}' not found.")
        return

    logger.info(f"Processing data file: {data_file_path}")

    # Open the data file and apply the timestamp
    data = add_timestamp(data_file_path)

    # Create an instance of the DBHandler class
    db_handler = DBHandler(config_file='config.ini', section='MONGODB')

    # Insert the data into MongoDB
    db_handler.insert_data(data)

    logger.info(f"{len(data)} entries inserted into MongoDB")

    logger.info(f"Dump file '{dump_file_path}' loaded")

    # Open the dump file
    with open(dump_file_path, 'r+') as dump_file:
        old_data = json.load(dump_file)
        # Make it an empty file
        dump_file.truncate(0)

    data.extend(old_data)

    # Remove old dictionaries
    data = remove_old_dicts(data)

    # Remove duplicate IPs
    data = remove_duplicates_by_ip(data)

    # Dump the updated data into the dump file
    with open(dump_file_path, 'w') as dump_file:
        json.dump(data, dump_file)

    logger.info(f"{len(data)} entries saved to {dump_file_path}")


if __name__ == '__main__':
    main()
