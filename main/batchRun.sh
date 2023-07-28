#!/bin/bash

mkdir -p "/PowerBarcoder/data/result/batchRun"

batchRunNumber=30
configFile="blasttest1"

for ((i = 0; i <= batchRunNumber; i++)); do
    mkdir -p "/PowerBarcoder/data/result/batchRun/blasttest$i"
    bash powerBarcode.sh $configFile
    cp -r /PowerBarcoder/data/result/blasttest1/* "/PowerBarcoder/data/result/batchRun/blasttest$i/"
done

