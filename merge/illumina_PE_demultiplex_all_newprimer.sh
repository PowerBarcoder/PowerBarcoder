#! /bin/bash


. ./config.sh


#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
${myFastpPath}fastp -i $myRowR1Gz -I $myRowR2Gz -o $myTrimmedR1Gz -O $myTrimmedR2Gz -j $summaryJsonFileName -h $summaryHtmlFileName


#using (universal) primer sequences to demultiplex
#rbcL C terminal
# 先trim，再取出跟指定primer一致的序列出來，方向一拉同 (e error錯誤率)
# using (universal) primer sequences to demultiplex
# rbcL N terminal
#"TAGGTCTGTCTGCYAARAATTATGG" and "GTTCCCCYTCTAGTTTRCCTACTAC" are VARIABLEs (sequences of rbcLC primers)
#"rbcLC" the name of the amplicon, which is a VARIABLE too
${myCutadaptPath}cutadapt -e $errorRateCutadaptor --no-indels --discard-untrimmed --pair-filter=both --minimum-length $minimumLengthCutadaptor --pair-adapters -g $primerF -G $primerR --action=none -o ${nameOfLoci}.1_R1 -p ${nameOfLoci}.1_R2 $myTrimmedR1Gz $myTrimmedR2Gz -j $threadNumberCutadaptor
${myCutadaptPath}cutadapt -e $errorRateCutadaptor --no-indels --discard-untrimmed --pair-filter=both --minimum-length $minimumLengthCutadaptor --pair-adapters -g $primerR -G $primerF --action=none -o ${nameOfLoci}.2_R1 -p ${nameOfLoci}.2_R2 $myTrimmedR1Gz $myTrimmedR2Gz -j $threadNumberCutadaptor
cat ${nameOfLoci}.1_R1 ${nameOfLoci}.2_R2 > $amplicon_r1
cat ${nameOfLoci}.1_R2 ${nameOfLoci}.2_R1 > $amplicon_r2
rm ${nameOfLoci}*_R*
mkdir ${nameOfLoci}_demultiplex
cd ${nameOfLoci}_demultiplex

# # 做demultiplex
# #"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
# #{name1} and {name2} are header names of fasta


# AB test
# ${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLN_start2_0.fasta --action=none -o rbcLN_{name1}_{name2}_r1.fq -p rbcLN_{name1}_{name2}_r2.fq ../rbcLN_amplicon_r1.fq ../rbcLN_amplicon_r2.fq -j $threadNumberCutadaptor
${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../${barcodesFile1} -G file:../${barcodesFile2} --action=none -o rbcLN_{name1}_{name2}_r1.fq -p rbcLN_{name1}_{name2}_r2.fq ../${amplicon_r1} ../${amplicon_r2} -j $threadNumberCutadaptor


# # 迴圈去掉primer
for File in *r1.fq
	do
	${myCutadaptPath}cutadapt -e $errorRateCutadaptor --no-indels --minimum-length $minimumLengthCutadaptorInLoop -g $primerF  -o trim_${File} ${File} -j $threadNumberCutadaptor
	done

for file in *r2.fq
	do
	${myCutadaptPath}cutadapt -e $errorRateCutadaptor --no-indels --minimum-length $minimumLengthCutadaptorInLoop -g $primerR -o trim_${file} ${file} -j $threadNumberCutadaptor
	done
# -----------------demultiplex完成------------------------

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
echo "start dada2_denoise_PE_newprimer.r"
Rscript dada2_denoise_PE_newprimer.r $mainDataPath > log_dada2.txt




# # -----------------------nonmerge的要來執行python-----------------------------
echo "start merge.sh"
bash merge.sh

echo "end of flow"