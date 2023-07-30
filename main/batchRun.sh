#!/bin/bash

mkdir -p "/PowerBarcoder/data/result/batchRun"

batchRunNumber=30
configFile="blasttest1"

for ((i = 0; i <= batchRunNumber; i++)); do
    targetDir="/PowerBarcoder/data/result/batchRun/blasttest$i"

    # Check if the directory already exists
    if [ ! -d "$targetDir" ]; then
        # Create the directory if it doesn't exist
        mkdir -p "$targetDir"

        # Execute the bash script powerBarcode.sh using $configFile
        bash powerBarcode.sh "$configFile"

        # Copy the contents from /PowerBarcoder/data/result/blasttest1 to the target directory
        cp -r /PowerBarcoder/data/result/blasttest1/* "$targetDir/"

        # Remove all files in the target directory except "config.sh"
        find "$targetDir" -type f ! -name "config.sh" -exec rm {} \;
    else
        echo "Directory $targetDir already exists. Skipping..."
    fi
done

