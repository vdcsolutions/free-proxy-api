#!/bin/bash

# Check if remote host argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: sh scp_files.sh remote_host"
    exit 1
fi

# Remote host
remote_host=$1

# Source directory (current directory)
source_dir=$(pwd)

# Destination directory on remote host
destination_dir="/root"

# Loop through all files in the source directory
for file in "$source_dir"/*; do
    # Check if the item is a file
    if [ -f "$file" ]; then
        # Extract the file name
        file_name=$(basename "$file")

        # Use scp to copy the file to the remote host
        scp "$file" "$remote_host:$destination_dir/$file_name"

        # Check the exit status of the scp command
        if [ $? -eq 0 ]; then
            echo "File $file_name copied successfully."
        else
            echo "Error: Failed to copy file $file_name."
        fi
    fi
done

# Make first_boot and startup_routine files executable on the server
ssh "$remote_host" "chmod +x $destination_dir/first_boot.sh $destination_dir/startup_routine.sh"

# Run first_boot on the server
ssh "$remote_host" "$destination_dir/first_boot.sh"
