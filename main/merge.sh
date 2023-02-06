#! /bin/bash

. ./config.sh

#  新的DADA2已經將r1跟r2合併了，所以是放在nonmerged下，檔名結尾是_.fas
#  /home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result20230206_rbcL/rbcLC_demultiplex/denoice_best/nonmerged
#  所以blast裡面會處理變更的路徑，處理完之後，交由下一步的python拆出來到原先的r1,r2資料夾裡，拆完其他路徑都就照舊了
bash ./mergeModule/00_blastForRef.sh #內部自帶迴圈處理


for ((i=0; i<${#nameOfLoci[@]}; i++))
do
    count=0
#    for File in ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1/*
    for File in ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/*
    do
    echo ${File}
    if [[ -d $PASSED ]]; then
        echo "$PASSED is a directory"
    elif [[ -f $PASSED ]]; then
        echo "$PASSED is a file"
        ((count = $count+1))
    else
        echo "$PASSED is not valid"
    fi
    done

    if [ ${count} -gt 1 ] 
    then #有檔案的才做
    ((count = $count/2))
    echo "${count} pairs nonmerged files found in ${nameOfLoci[i]}"

         #  就是這裡拆NN到原先的r1,r2資料夾裡
         python3 ./mergeModule/nnSpliter.py $ampliconInfo ${sseqidFileName[i]} $resultDataPath ${nameOfLoci[i]} #內部需要拆10N

#        準備parsing各loci local blast的結果
#        python3 ./mergeModule/BlastResult.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}
#
#        # TODO
#        # 20230107接NNNNN的話，底下這兩部就要改成一個檔案，用來把NNNNNN拆掉，然後按blast的結果做reverse complement後，輸出正確方向的ref
#        python3 ./mergeModule/BeforeAlignment.py $ampliconInfo ${sseqidFileName[i]} $resultDataPath ${nameOfLoci[i]}
#        python3 ./mergeModule/Alignment.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}
#
#
#        python3 ./mergeModule/merge.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}
    else #沒有的就跳過
    echo "no nonmerged files found in ${nameOfLoci[i]}"
    fi

done
