#! /bin/bash

. ./config.sh

rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/powerbarcoder/nCatR1R2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/powerbarcoder/r1
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/powerbarcoder/r2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/powerbarcoder/aligned

python3 ./qcModule/missingList.py
