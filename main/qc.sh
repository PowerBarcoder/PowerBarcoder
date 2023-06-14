#! /bin/bash

. ./config.sh

rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned

python3 ./qcModule/missingList.py
