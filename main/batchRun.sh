#!/bin/bash

# Function to process a configuration
process_config() {
  local configFile="$1"
  local batchRunNumber="$2"

  for ((i = 0; i <= batchRunNumber; i++)); do
    targetDir="/PowerBarcoder/data/result/batchRun/${configFile}${i}"
    sourceDir="/PowerBarcoder/data/result/${configFile}"

    # Check if the directory already exists
    if [ ! -d "${targetDir}" ]; then
      # Create the directory if it doesn't exist
      mkdir -p "${targetDir}"
      # Execute the bash script powerBarcode.sh using $configFile
      bash powerBarcode.sh "$configFile"
      # Copy the contents from sourceDir to the targetDir
      cp -r "${sourceDir}/"* "${targetDir}/"
      # Remove all files in the source directory except "config.sh"
      find "${sourceDir}" -type f ! -name "config.sh" -exec rm {} \;
    else
      echo "Directory ${targetDir} already exists. Skipping..."
    fi
  done
}

# Process different configurations
configs=("SuperRed_35" "filtered_selected_pure" "filtered")
loopRun="1"
for configFile in "${configs[@]}"; do
  process_config "${configFile}" "${loopRun}"
done
