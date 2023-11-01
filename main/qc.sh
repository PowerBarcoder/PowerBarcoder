#! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

echo "[INFO] Start generating quality control report !"

bash ./qcModule/fileLister.sh "$1" # bash is faster then python when listing the directory

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "${nameOfLoci[i]}"

  python3 ./qcModule/csvParser.py "$resultDataPath" "${nameOfLoci[i]}"

done

python3 ./qcModule/validator.py "$resultDataPath" "${nameOfLoci[i]}"


echo "[INFO] End of generating quality control report !"
