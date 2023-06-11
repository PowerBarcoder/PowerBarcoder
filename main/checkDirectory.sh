# ! /bin/bash
. ./config.sh

echo "[INFO] checking file directories..."

#yixuan modified for multiLoci
for ((i=0; i<${#nameOfLoci[@]}; i++))
do
# create Layer 0 folder
mkdir -p ${resultDataPath}
# create Layer 1st folder
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result
# create Layer 2nd folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/blastResult
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/mergeResult
# create Layer 3rd folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/filtered
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best
# create Layer 4th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/mergeResult
# create Layer 5th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/r1Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/r2Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/mergeSeq
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise/nonmerged/aligned
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r1Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r2Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/aligned
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/mergeSeq
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/deGapMergeSeq
# create Layer 6th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/aligned/mafft

done