#! /bin/bash

. ./config.sh

echo "[INFO] Start generating quality control report !"

#rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2"
#rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1"
#rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2"
#rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned"

bash ./qcModule/fileLister.sh
bash ./qcModule/csvParser.sh
python3 ./qcModule/networkVisualizer.py
echo "[INFO] End of generating quality control report !"

