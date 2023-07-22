#! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

if [ "${blastReadChoosingMode}" -eq 1 ]; then
  echo "[INFO] blastReadChoosingMode is 1, run nnSpliter.py before blast "
  for ((i = 0; i < ${#nameOfLoci[@]}; i++)); do
    python3 ./mergeModule/nnSpliter.py "$resultDataPath" "${nameOfLoci[i]}" #blast完，需要拆10N
  done
else #沒有的就跳過
  echo "[INFO] blastReadChoosingMode is 0, run nnSpliter.py after blast "
fi

bash ./mergeModule/00_blastForRef.sh "$1" #先blast，內部自帶迴圈處理

for ((i = 0; i < ${#nameOfLoci[@]}; i++)); do
  count=0
  dir=${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2/
  count=$(ls -1 "$dir" | grep ".fas" | wc -l) #計算檔案結尾是.fas的數量
  echo "[INFO] Number of '.fas' files: $count"

  if [ "${count}" -gt 1 ]; then #有檔案的才做
    #    ((count = $count/2))
    echo "[INFO] ${count} nonmerged files found in ${nameOfLoci[i]}"

    if [ "${blastReadChoosingMode}" -eq 0 ]; then
        # r1r2 cat起來blast
        #  就是這裡拆NN到原先的nonmerged/r1,r2資料夾裡(只負責拆，判斷方向交給下一步驟)
        python3 ./mergeModule/nnSpliter.py "$resultDataPath" "${nameOfLoci[i]}" #blast完，需要拆10N
    fi

    #  準備parsing各loci local blast的結果 --- input：10N seq 的 blast refResult; output：10N blastResult
    python3 ./mergeModule/blastResultParser.py "$ampliconInfo" "$resultDataPath" "${blastParsingMode[i]}" "${nameOfLoci[i]}"

    # 20230107 10N，需按blast的結果做reverse complement後，輸出正確方向的ref(改動的部分不太確定有沒有對，因為這整批好像都沒有在做reverse compliment)
    # 20230215 10N，reverse complement已確認是只轉ref的部分
    python3 ./mergeModule/alignmentPretreater.py "$ampliconInfo" "${sseqidFileName[i]}" "$resultDataPath" "${nameOfLoci[i]}"
    python3 ./mergeModule/alignmenter.py "$ampliconInfo" "$resultDataPath" "${nameOfLoci[i]}"
    python3 ./mergeModule/merger.py "$ampliconInfo" "$resultDataPath" "${nameOfLoci[i]}"

  else #沒有的就跳過
    echo "[WARNING] no nonmerged files found in ${nameOfLoci[i]}"
  fi

done
