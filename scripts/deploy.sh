#!/bin/bash

# Check if remote host and address arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: sh scp_files.sh remote_host remote_address"
    exit 1
fi

# Remote host and address
remote_host=$1
remote_address=$2

# Source directory (current directory)
source_dir=$(pwd)

# Destination directory on remote host
destination_dir="/root"

# Loop through all files in the source directory
for file in "$source_dir"/*; do
    # Check if the item is a file
    if [ -f "$file" ]; then
        # Use scp to copy the file to the remote host
        scp "$file" "$remote_host:$destination_dir"
    fi
done
