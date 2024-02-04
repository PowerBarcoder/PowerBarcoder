#!/bin/bash

######
# 需將config檔放置於 /PowerBarcoder/data/result/$configFile/，
# 並注意要修改config.sh中的時間戳記，改成configFile的名稱
# 若有新library引入，記得重啟docker
######

mkdir -p "/PowerBarcoder/data/result/batchRun"

batchRunNumber=1
configFile="SuperRed_35"

for ((i = 0; i <= batchRunNumber; i++)); do
  targetDir="/PowerBarcoder/data/result/batchRun/$configFile$i"

  # Check if the directory already exists
  if [ ! -d "$targetDir" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$targetDir"

    # Execute the bash script powerBarcode.sh using $configFile
    bash powerBarcode.sh "$configFile"

    # Copy the contents from /PowerBarcoder/data/result/$configFile to the target directory
    cp -r /PowerBarcoder/data/result/$configFile/* "$targetDir/"

    wait

    # Remove all files in the target directory except "config.sh"
    find "$targetDir" -type f ! -name "config.sh" -exec rm {} \;
  else
    echo "Directory $targetDir already exists. Skipping..."
  fi
done

batchRunNumber=1
configFile="filtered_selected_pure"

for ((i = 0; i <= batchRunNumber; i++)); do
  targetDir="/PowerBarcoder/data/result/batchRun/$configFile$i"

  # Check if the directory already exists
  if [ ! -d "$targetDir" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$targetDir"

    # Execute the bash script powerBarcode.sh using $configFile
    bash powerBarcode.sh "$configFile"

    # Copy the contents from /PowerBarcoder/data/result/$configFile to the target directory
    cp -r /PowerBarcoder/data/result/$configFile/* "$targetDir/"

    wait

    # Remove all files in the target directory except "config.sh"
    find "$targetDir" -type f ! -name "config.sh" -exec rm {} \;
  else
    echo "Directory $targetDir already exists. Skipping..."
  fi
done

batchRunNumber=1
configFile="filtered"

for ((i = 0; i <= batchRunNumber; i++)); do
  targetDir="/PowerBarcoder/data/result/batchRun/$configFile$i"

  # Check if the directory already exists
  if [ ! -d "$targetDir" ]; then
    # Create the directory if it doesn't exist
    mkdir -p "$targetDir"

    # Execute the bash script powerBarcode.sh using $configFile
    bash powerBarcode.sh "$configFile"

    # Copy the contents from /PowerBarcoder/data/result/$configFile to the target directory
    cp -r /PowerBarcoder/data/result/$configFile/* "$targetDir/"

    wait

    # Remove all files in the target directory except "config.sh"
    find "$targetDir" -type f ! -name "config.sh" -exec rm {} \;
  else
    echo "Directory $targetDir already exists. Skipping..."
  fi
done
