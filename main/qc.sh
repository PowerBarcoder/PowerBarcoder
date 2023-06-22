#! /bin/bash

. ./config.sh

echo "[INFO] Start generating quality control report !"

bash ./qcModule/fileLister.sh
bash ./qcModule/csvParser.sh

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "${nameOfLoci[i]}"

  python3 ./qcModule/networkVisualizer.py "$resultDataPath" "${nameOfLoci[i]}"
  #rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2"
  #rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1"
  #rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2"
  #rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned"

done

echo "[INFO] End of generating quality control report !"
