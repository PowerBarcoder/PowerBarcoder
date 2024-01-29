#! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

echo "[INFO] Start cleaning !"

# if dev_mode is 1, then clean the directory, else do nothing
if [ "${dev_mode}" -eq 1 ]; then

  for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

    echo "${nameOfLoci[i]}, start to clean the directory"

    # Layer 4th folders
  #  rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/dada2/merged"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1Ref"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2Ref"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned"
#    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/rawMerged"
  #  rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/merged"
    # Layer 3rd folders
  #  rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/dada2"
  #  rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger"
    # Layer 2nd folders
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult"
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/denoiseResult"
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/blastResult"
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/mergeResult"
  #  rm -r "${resultDataPath}${nameOfLoci[i]}_result/qcResult"
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r1.fq"
    rm -r "${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r2.fq"

  done

  rm -r "${resultDataPath}trim_R1FastqGz.gz"
  rm -r "${resultDataPath}trim_R2FastqGz.gz"

fi

echo "[INFO] End of cleaning !"
