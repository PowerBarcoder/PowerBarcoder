#! /bin/bash


. ./config.sh

#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
#${myFastpPath}fastp -i $myRowR1Gz -I $myRowR2Gz -o $myTrimmedR1Gz -O $myTrimmedR2Gz -j $summaryJsonFileName -h $summaryHtmlFileName

#yixuan modified for multiLoci
for ((i=0; i<${#nameOfLoci[@]}; i++))
do

#using (universal) primer sequences to demultiplex
# rbcL C terminal
# 先trim，再取出跟指定primer一致的序列出來，方向一拉同 (e error錯誤率)
# using (universal) primer sequences to demultiplex
# rbcL N terminal
#"TAGGTCTGTCTGCYAARAATTATGG" and "GTTCCCCYTCTAGTTTRCCTACTAC" are VARIABLEs (sequences of rbcLC primers)
#"rbcLC" the name of the amplicon, which is a VARIABLE too

${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerF[i]} -G ${primerR[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.1_R1 -p ${resultDataPath}${nameOfLoci[i]}.1_R2 $myTrimmedR1Gz $myTrimmedR2Gz -j ${threadNumberCutadaptor[i]}
${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerR[i]} -G ${primerF[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.2_R1 -p ${resultDataPath}${nameOfLoci[i]}.2_R2 $myTrimmedR1Gz $myTrimmedR2Gz -j ${threadNumberCutadaptor[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R1 ${resultDataPath}${nameOfLoci[i]}.2_R2 > ${resultDataPath}${amplicon_r1[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}${nameOfLoci[i]}.2_R1 > ${resultDataPath}${amplicon_r2[i]}
rm ${resultDataPath}${nameOfLoci[i]}*_R*
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex
cd ${resultDataPath}${nameOfLoci[i]}_demultiplex

# # 做demultiplex
# #"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
# #{name1} and {name2} are header names of fasta


# AB test
# ${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLC_start2_0.fasta --action=none -o rbcLC_{name1}_{name2}_r1.fq -p rbcLC_{name1}_{name2}_r2.fq ../rbcLC_amplicon_r1.fq ../rbcLC_amplicon_r2.fq -j $threadNumberCutadaptor
${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:${mainDataPath}${barcodesFile1[i]} -G file:${mainDataPath}${barcodesFile2[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}_{name1}_{name2}_r1.fq -p ${resultDataPath}${nameOfLoci[i]}_{name1}_{name2}_r2.fq ${resultDataPath}${amplicon_r1[i]} ${resultDataPath}${amplicon_r2[i]} -j ${threadNumberCutadaptor[i]}


# # 迴圈去掉primer (絕對路徑下，用$(basename $file)取檔名)
for File in ${resultDataPath}*r1.fq
	do
	${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerF[i]} -o ${resultDataPath}trim_$(basename $File) ${resultDataPath}$(basename $File) -j ${threadNumberCutadaptor[i]}
	done

for file in ${resultDataPath}*r2.fq
	do
	${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerR[i]} -o ${resultDataPath}trim_$(basename $file) ${resultDataPath}$(basename $file) -j ${threadNumberCutadaptor[i]}
	done
# -----------------demultiplex完成------------------------

mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed
echo 3
mv ${resultDataPath}trim_* ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/r1
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/r2
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/r1
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/r2
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r1
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice/nonmerged/r2
mkdir -p  ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r2
cd ..

#yixuan modified for multiLoci
done




# # # -----------------------轉去執行R-----------------------------
# echo "start dada2_denoise_PE_newprimer.r"
# Rscript dada2_denoise_PE_newprimer.r $mainDataPath ${nameOfLoci[@]} > log_dada2.txt




# # # -----------------------nonmerge的要來執行python-----------------------------
# echo "start merge.sh"
# bash merge.sh

# echo "end of flow"