#! /bin/bash

. ./config.sh

bash ./mergeModule/00_blastForRef.sh

for ((i=0; i<${#nameOfLoci[@]}; i++))
do

    count=0
    for File in ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1/*
    do
    ((count = $count+1))
    done

    if [ ${count} -gt 1 ] 
    then #有檔案的才做
    echo "${count} pairs nonmerged files found in ${nameOfLoci[i]}"
        python3 ./mergeModule/BlastResult.py $mainDataPath $resultDataPath ${nameOfLoci[i]}
        python3 ./mergeModule/BeforeAlignment.py $mainDataPath $sseqidFileName $resultDataPath ${nameOfLoci[i]}
        python3 ./mergeModule/Alignment.py $mainDataPath $resultDataPath ${nameOfLoci[i]}
        python3 ./mergeModule/merge.py $mainDataPath $resultDataPath ${nameOfLoci[i]}
    else #沒有的就跳過
    echo "no nonmerged files found in ${nameOfLoci[i]}"
    fi

done