#! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

echo "[INFO] Start generating quality control report !"

bash ./qc/fileLister.sh "$1" # bash is faster then python when listing the directory

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "${nameOfLoci[i]}"

  python3 ./qc/csvParser.py "$resultDataPath" "${nameOfLoci[i]}"

  python3 ./qc/validator.py "$resultDataPath" "${nameOfLoci[i]}"

#  # Export data from SQLite to CSV for each loci
#  python3 ./qc/sql_to_csv.py "${resultDataPath}${nameOfLoci[i]}_result/"

done

echo "[INFO] End of generating quality control report !"
