#! /bin/bash

. ./config.sh

bash ./mergeModule/00_blastForRef.sh
python3 ./mergeModule/BlastResult.py $mainDataPath
python3 ./mergeModule/BeforeAlignment.py $mainDataPath $sseqidFileName
python3 ./mergeModule/Alignment.py $mainDataPath
python3 ./mergeModule/merge.py $mainDataPath
