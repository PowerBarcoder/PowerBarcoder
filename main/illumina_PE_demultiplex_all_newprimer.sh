#! /bin/bash

. ./config.sh

# 20230107這一步myRowR1Gz消失了需修正、另外可以用一個參數控制要不要做這步 done (之前亦煊把這註解掉了，所以不用作這筆討論)
# 20230604啟用fastp #FIXME fastp按以下指令操作，跟之前給的trim檔案大小不同 184MB & 224MB -> 167MB & 208MB
#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
${myFastpPath}fastp -i ${R1FastqGz} -I ${R2FastqGz} -o ${resultDataPath}trim_R1FastqGz.gz -O ${resultDataPath}trim_R2FastqGz.gz -j ${resultDataPath}summaryJsonFileName.json -h ${resultDataPath}summaryHtmlFileName.html

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

${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerF[i]} -G ${primerR[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.1_R1 -p ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}trim_R1FastqGz.gz ${resultDataPath}trim_R2FastqGz.gz -j ${customizedCoreNumber[i]}
${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerR[i]} -G ${primerF[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.2_R1 -p ${resultDataPath}${nameOfLoci[i]}.2_R2 ${resultDataPath}trim_R1FastqGz.gz ${resultDataPath}trim_R2FastqGz.gz -j ${customizedCoreNumber[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R1 ${resultDataPath}${nameOfLoci[i]}.2_R2 > ${resultDataPath}${amplicon_r1[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}${nameOfLoci[i]}.2_R1 > ${resultDataPath}${amplicon_r2[i]}
rm ${resultDataPath}${nameOfLoci[i]}*_R*

# # 做demultiplex
# #"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
# #{name1} and {name2} are header names of fasta

# AB test
# ${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLC_start2_0.fasta --action=none -o rbcLC_{name1}_{name2}_r1.fq -p rbcLC_{name1}_{name2}_r2.fq ../rbcLC_amplicon_r1.fq ../rbcLC_amplicon_r2.fq -j $customizedCoreNumber
${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:${ampliconInfo}${barcodesFile1[i]} -G file:${ampliconInfo}${barcodesFile2[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}_demultiplex/${nameOfLoci[i]}_{name1}_{name2}_r1.fq -p ${resultDataPath}${nameOfLoci[i]}_demultiplex/${nameOfLoci[i]}_{name1}_{name2}_r2.fq ${resultDataPath}${amplicon_r1[i]} ${resultDataPath}${amplicon_r2[i]} -j ${customizedCoreNumber[i]}

## If we iterate the file with "&" and "wait", which means we can run the loop in parallel processes, it will be faster.
## Also, in each cutadapt instance, the "core_numbers = 4" can be test to see if it is the best number of multiprocessing.
## (The logic of the loop doesn't change, we just beautify the code.)
# Set the number of core_numbers to use
core_numbers=4

# Loop over r1 files
for r1_file in ${resultDataPath}${nameOfLoci[i]}_demultiplex/*r1.fq; do
    # Define the output file name
    out_file="${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/trim_$(basename ${r1_file})"

    # Run cutadapt with parallel processing
    ${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerF[i]} -o ${out_file} ${resultDataPath}${nameOfLoci[i]}_demultiplex/$(basename ${r1_file}) -j ${core_numbers} &
done

# Loop over r2 files
for r2_file in ${resultDataPath}${nameOfLoci[i]}_demultiplex/*r2.fq; do
    # Define the output file name
    out_file="${resultDataPath}${nameOfLoci[i]}_demultiplex/trimmed/trim_$(basename ${r2_file})"

    # Run cutadapt with parallel processing
    ${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerR[i]} -o ${out_file} ${resultDataPath}${nameOfLoci[i]}_demultiplex/$(basename ${r2_file}) -j ${core_numbers} &
done

# Wait for all processes to finish
wait
# -----------------demultiplex完成------------------------

# [20230421][test] 648 ASV in in AMD Ryzen 5 5600U with Radeon Graphics, 32GB RAM
# for loop for r1 and r2, 2 minutes 52 seconds
# [2023-04-20 17:47:37]This is cutadapt 4.3 with Python 3.10.6
# [2023-04-20 17:50:29]done
# multiprocessing for r1 and r2, 25 seconds
# [2023-04-20 19:03:58]This is cutadapt 4.3 with Python 3.10.6
# [2023-04-20 19:04:23]done

done
