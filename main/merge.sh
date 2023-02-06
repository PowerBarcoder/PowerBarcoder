#! /bin/bash

. ./config.sh

#  新的DADA2已經將r1跟r2合併了，所以是放在nonmerged下，檔名結尾是_.fas
#  /home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result20230206_rbcL/rbcLC_demultiplex/denoice_best/nonmerged
#  所以blast裡面會處理變更的路徑，處理完之後，
#  檢查blast的結果方向是否與原本的相反，相反的話，反轉ref，之後再去alignment

bash ./mergeModule/00_blastForRef.sh #先blast，內部自帶迴圈處理


for ((i=0; i<${#nameOfLoci[@]}; i++))
do
    count=0
    dir=${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/
    count=$(ls -1 $dir | grep ".fas" | wc -l) #計算檔案結尾是.fas的數量
    echo "Number of '.fas' files: $count"

    if [ ${count} -gt 1 ] 
    then #有檔案的才做
#    ((count = $count/2))
        echo "${count} nonmerged files found in ${nameOfLoci[i]}"
        #  就是這裡拆NN到原先的nonmerged/r1,r2資料夾裡
        python3 ./mergeModule/nnSpliter.py $resultDataPath ${nameOfLoci[i]} #blast完，需要拆10N

        #  準備parsing各loci local blast的結果
        python3 ./mergeModule/blastResultParser.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}

        # TODO 20230107接NNNNN的話，底下這兩部就要改成一個檔案，用來把NNNNNN拆掉，然後按blast的結果做reverse complement後，輸出正確方向的ref
        python3 ./mergeModule/alignmentPretreater.py $ampliconInfo ${sseqidFileName[i]} $resultDataPath ${nameOfLoci[i]}
        python3 ./mergeModule/alignmenter.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}
#        python3 ./mergeModule/merge.py $ampliconInfo $resultDataPath ${nameOfLoci[i]}

    else #沒有的就跳過
    echo "no nonmerged files found in ${nameOfLoci[i]}"
    fi

done
