# ! /bin/bash
. ./config.sh

echo "[INFO] checking file directories..."

#yixuan modified for multiLoci
for ((i=0; i<${#nameOfLoci[@]}; i++))
do

# create Layer 1st folder
mkdir -p ${resultDataPath}blastResult
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex
# create Layer 2nd folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best
# create Layer 3rd folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/mergeResult
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/mergeResult #目前只做這個
# create Layer 4th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r1Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r2Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/mergeSeq
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/aligned
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r2
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r2Ref
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/aligned
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/mergeSeq
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/deGapMergeSeq
# create Layer 5th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/aligned/mafft

done