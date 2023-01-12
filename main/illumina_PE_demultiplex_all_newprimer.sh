#! /bin/bash

. ./config.sh

# 20230107這一步myRowR1Gz消失了需修正、另外可以用一個參數控制要不要做這步 done (之前亦煊把這註解掉了，所以不用作這筆討論)
#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
#${myFastpPath}fastp -i $myRowR1Gz -I $myRowR2Gz -o $R1FastqGz -O $R2FastqGz -j $summaryJsonFileName -h $summaryHtmlFileName

#yixuan modified for multiLoci
for ((i=0; i<${#nameOfLoci[@]}; i++))
do

# create Layer 1st folder
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
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/mergeSeq
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/aligned
# create Layer 5th folders
mkdir -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/aligned/mafft

#using (universal) primer sequences to demultiplex
# rbcL C terminal
# 先trim，再取出跟指定primer一致的序列出來，方向一拉同 (e error錯誤率)
# using (universal) primer sequences to demultiplex
# rbcL N terminal
#"TAGGTCTGTCTGCYAARAATTATGG" and "GTTCCCCYTCTAGTTTRCCTACTAC" are VARIABLEs (sequences of rbcLC primers)
#"rbcLC" the name of the amplicon, which is a VARIABLE too

${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerF[i]} -G ${primerR[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.1_R1 -p ${resultDataPath}${nameOfLoci[i]}.1_R2 $R1FastqGz $R2FastqGz -j ${customizedThreadNumber[i]}
${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerR[i]} -G ${primerF[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.2_R1 -p ${resultDataPath}${nameOfLoci[i]}.2_R2 $R1FastqGz $R2FastqGz -j ${customizedThreadNumber[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R1 ${resultDataPath}${nameOfLoci[i]}.2_R2 > ${resultDataPath}${amplicon_r1[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}${nameOfLoci[i]}.2_R1 > ${resultDataPath}${amplicon_r2[i]}
rm ${resultDataPath}${nameOfLoci[i]}*_R*
cd ${resultDataPath}${nameOfLoci[i]}_demultiplex

# # 做demultiplex
# #"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
# #{name1} and {name2} are header names of fasta


# AB test
# ${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLC_start2_0.fasta --action=none -o rbcLC_{name1}_{name2}_r1.fq -p rbcLC_{name1}_{name2}_r2.fq ../rbcLC_amplicon_r1.fq ../rbcLC_amplicon_r2.fq -j $customizedThreadNumber
${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:${ampliconInfo}${barcodesFile1[i]} -G file:${ampliconInfo}${barcodesFile2[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}_demultiplex/${nameOfLoci[i]}_{name1}_{name2}_r1.fq -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/${nameOfLoci[i]}_{name1}_{name2}_r2.fq ${resultDataPath}${amplicon_r1[i]} ${resultDataPath}${amplicon_r2[i]} -j ${customizedThreadNumber[i]}


# # 迴圈去掉primer (絕對路徑下，用$(basename $file)取檔名)
for File in ${resultDataPath}${nameOfLoci[i]}_demultiplex/*r1.fq
	do
	${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerF[i]} -o ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/trim_$(basename $File) ${resultDataPath}${nameOfLoci[i]}_demultiplex/$(basename $File) -j ${customizedThreadNumber[i]}
	done

for file in ${resultDataPath}${nameOfLoci[i]}_demultiplex/*r2.fq
	do
	${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerR[i]} -o ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/trim_$(basename $file) ${resultDataPath}${nameOfLoci[i]}_demultiplex/$(basename $file) -j ${customizedThreadNumber[i]}
	done
# -----------------demultiplex完成------------------------

# # 直接把檔案寫到指定地點就不用再移動檔案了，所以這行不要
# mv ${resultDataPath}${nameOfLoci[i]}_demultiplex/trim_${nameOfLoci[i]}* ${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/

cd .. # 應該不需要再切路徑了，因為底下有切

done


# # -----------------------轉去執行R-----------------------------
cd ${workingDirectory}
# echo "$PWD"

echo "start dada2_denoise_PE_newprimer.r"
Rscript ${workingDirectory}dada2_denoise_PE_newprimer.r $ampliconInfo $workingDirectory $resultDataPath $dada2LearnErrorFile $dada2BarcodeFile ${nameOfLoci[@]} > ${resultDataPath}log_dada2.txt

#echo "start dada2_denoise_PE_10Ns.r"
#Rscript ${workingDirectory}dada2_denoise_PE_10Ns.r $ampliconInfo $workingDirectory $resultDataPath ${nameOfLoci[@]} > log_dada2.txt

# # -----------------------nonmerge的要來執行python-----------------------------
cd ${workingDirectory}
# echo "$PWD"
echo "start merge.sh"
bash ${workingDirectory}merge.sh

echo "end of flow"