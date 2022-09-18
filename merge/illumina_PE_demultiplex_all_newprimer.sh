#! /bin/bash


targetFilePrefix="HGT22043_2_DNAL1_000000000-KHMTG_L1"
targetFileR1FileName="${targetFilePrefix}_R1.fastq.gz"
targetFileR2FileName="${targetFilePrefix}_R2.fastq.gz"
trimedR1FileName="${targetFilePrefix}_R1_trimmed.fastq.gz"
trimedR2FileName="${targetFilePrefix}_R2_trimmed.fastq.gz"

#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
/home/lykuo/miniconda2/bin/fastp -i $targetFileR1FileName -I $targetFileR2FileName -o $trimedR1FileName -O $trimedR2FileName -j ${targetFilePrefix}.json -h ${targetFilePrefix}.html

#using (universal) primer sequences to demultiplex
#rbcL C terminal
# 先trim，再取出跟指定primer一致的序列出來，方向一拉同 (e error錯誤率)
# using (universal) primer sequences to demultiplex
# rbcL N terminal
#"TAGGTCTGTCTGCYAARAATTATGG" and "GTTCCCCYTCTAGTTTRCCTACTAC" are VARIABLEs (sequences of rbcLC primers)
#"rbcLC" the name of the amplicon, which is a VARIABLE too

myCutadapt="/home/lykuo/cutadapt-venv/bin/"
errorRate="0.125"
minimumLength="70"
primerF="GAGACTAAAGCAGGTGTTGGATTCA"
primerR="TCAAGTCCACCRCGAAGRCATTC"
nameOfLoci="rbcLN"
amplicon_r1="${nameOfLoci}_amplicon_r1.fq"
amplicon_r2="${nameOfLoci}_amplicon_r2.fq"
threadNumber="30"

${myCutadapt}cutadapt -e $errorRate --no-indels --discard-untrimmed --pair-filter=both --minimum-length $minimumLength --pair-adapters -g $primerF -G $primerR --action=none -o ${nameOfLoci}.1_R1 -p ${nameOfLoci}.1_R2 $trimedR1FileName $trimedR2FileName -j $threadNumber
${myCutadapt}cutadapt -e $errorRate --no-indels --discard-untrimmed --pair-filter=both --minimum-length $minimumLength --pair-adapters -g $primerR -G $primerF --action=none -o ${nameOfLoci}.2_R1 -p ${nameOfLoci}.2_R2 $trimedR1FileName $trimedR2FileName -j $threadNumber
cat ${nameOfLoci}.1_R1 ${nameOfLoci}.2_R2 > $amplicon_r1
cat ${nameOfLoci}.1_R2 ${nameOfLoci}.2_R1 > $amplicon_r2
rm ${nameOfLoci}*_R*
mkdir ${nameOfLoci}_demultiplex
cd ${nameOfLoci}_demultiplex

# # 做demultiplex
# #"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
# #{name1} and {name2} are header names of fasta

barcodesFile1='barcodes_rbcL_start_0.fasta'
barcodesFile2='barcodes_rbcLN_start2_0.fasta'
# AB test
# ${myCutadapt}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLN_start2_0.fasta --action=none -o rbcLN_{name1}_{name2}_r1.fq -p rbcLN_{name1}_{name2}_r2.fq ../rbcLN_amplicon_r1.fq ../rbcLN_amplicon_r2.fq -j $threadNumber
${myCutadapt}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../${barcodesFile1} -G file:../${barcodesFile2} --action=none -o rbcLN_{name1}_{name2}_r1.fq -p rbcLN_{name1}_{name2}_r2.fq ../${amplicon_r1} ../${amplicon_r2} -j $threadNumber


# # 迴圈去掉primer
minimumLengthOfForLoop="150"

for File in *r1.fq
	do
	${myCutadapt}cutadapt -e $errorRate --no-indels --minimum-length $minimumLengthOfForLoop -g $primerF  -o trim_${File} ${File} -j $threadNumber
	done

for file in *r2.fq
	do
	${myCutadapt}cutadapt -e $errorRate --no-indels --minimum-length $minimumLengthOfForLoop -g $primerR -o trim_${file} ${file} -j $threadNumber
	done
# # -----------------demultiplex完成------------------------

mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
mkdir denoice/r1
mkdir denoice/r2
mkdir denoice_best/r1
mkdir denoice_best/r2
mkdir denoice/nonmerged
mkdir denoice_best/nonmerged
mkdir denoice/nonmerged/r1
mkdir denoice_best/nonmerged/r1
mkdir denoice/nonmerged/r2
mkdir denoice_best/nonmerged/r2
cd ..

# # -----------------------轉去執行R-----------------------------
Rscript dada2_denoise_PE_newprimer.r > log_dada2.txt


