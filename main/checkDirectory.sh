# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

echo "[INFO] checking file directories..."

mkdir -p ${resultDataPath}blastResult



#yixuan modified for multiLoci
for ((i = 0; i < ${#nameOfLoci[@]}; i++)); do
  # create Layer 0 folder
  mkdir -p ${resultDataPath}
  # create Layer 1st folder
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result
  # create Layer 2nd folders
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/blastResult
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/qcResult
  # create Layer 3rd folders
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/filtered
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/r1
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/r2
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/dada2
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/qcResult/validator
  # create Layer 4th folders
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/dada2/merged
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1Ref
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2Ref
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/rawMerged
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/merged
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/qcResult/validator/all
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/qcResult/validator/denoise
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/qcResult/validator/merge
  # create Layer 5th folders
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2/forSplit
  mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned/mafft

done
