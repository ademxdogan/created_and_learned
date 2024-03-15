#!/bin/bash

# Define the base folder
base_folder="/log/path"

# Get the list of folders under the base folder
folders=$(find "$base_folder" -mindepth 1 -maxdepth 1 -type d)

# Get today's date in YYYYMMDD format
today=$(date +"%Y%m%d")

# Flag to check if any folder is older than today
flag=0

# File to store non-file folders
output_file="/home/adem/notloggedservers.txt"

# Loop through each folder
for folder in $folders; do
    # Check if the folder is older than today
    if [ ! -z "$(find "$folder" -mindepth 1 -type f -newermt $today | head -1)" ]; then
    	#echo "$folder works!"
    	continue
    else
        #echo "Folder does not contain a file from today. $folder"
        flag=1
	if ! grep -q "^$folder$" "$output_file"; then
          echo "Folder $folder does not contain a file modified within the last 1 hour."
          echo "$folder" >> "$output_file"
        fi
	#echo "$folder" >> "$output_file"
    fi
done

# Generate an alarm if any folder is older than today
if [ $flag -eq 1 ]; then
    echo "Houston, we have a problem. Some servers didn't send log from last 24h "
    # Add your alarm command here
    cat $output_file
    exit 1
fi

