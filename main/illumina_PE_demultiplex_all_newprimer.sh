#! /bin/bash

. ./config.sh

# trim the reads by fastp
${myFastpPath}fastp -i ${ampliconInfo}${R1FastqGz} -I ${ampliconInfo}${R2FastqGz} -o ${resultDataPath}trim_R1FastqGz.gz -O ${resultDataPath}trim_R2FastqGz.gz -j ${resultDataPath}summary.json -h ${resultDataPath}summary.html

#yixuan modified for multiLoci
for ((i=0; i<${#nameOfLoci[@]}; i++))
do

# first step: demultiplex by locus primer,
# create two files: ${nameOfLoci[i]}_amplicon_r1.fq and ${nameOfLoci[i]}_amplicon_r2.fq
# in path: ${resultDataPath}${nameOfLoci[i]}_result/
${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerF[i]} -G ${primerR[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.1_R1 -p ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}trim_R1FastqGz.gz ${resultDataPath}trim_R2FastqGz.gz -j ${customizedCoreNumber[i]}
${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --discard-untrimmed --pair-filter=both --minimum-length ${minimumLengthCutadaptor[i]} --pair-adapters -g ${primerR[i]} -G ${primerF[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}.2_R1 -p ${resultDataPath}${nameOfLoci[i]}.2_R2 ${resultDataPath}trim_R1FastqGz.gz ${resultDataPath}trim_R2FastqGz.gz -j ${customizedCoreNumber[i]}
cat ${resultDataPath}${nameOfLoci[i]}.1_R1 ${resultDataPath}${nameOfLoci[i]}.2_R2 > ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r1.fq
cat ${resultDataPath}${nameOfLoci[i]}.1_R2 ${resultDataPath}${nameOfLoci[i]}.2_R1 > ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r2.fq
rm ${resultDataPath}${nameOfLoci[i]}*_R*

# second step: demultiplex by sample barcode,
# create multiple files naming with ${nameOfLoci[i]}_{name1}_{name2}_r1.fq and ${nameOfLoci[i]}_{name1}_{name2}_r2.fq styles
# in path: ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/
${myCutadaptPath}cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:${ampliconInfo}${barcodesFile1[i]} -G file:${ampliconInfo}${barcodesFile2[i]} --action=none -o ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/${nameOfLoci[i]}_{name1}_{name2}_r1.fq -p ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/${nameOfLoci[i]}_{name1}_{name2}_r2.fq ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r1.fq ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r2.fq -j ${customizedCoreNumber[i]}


# third step: trim the primer sites,
# create multiple files naming with ${nameOfLoci[i]}_{name1}_{name2}_r1.fq and ${nameOfLoci[i]}_{name1}_{name2}_r2.fq styles
# in path: ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed/

## If we iterate the file with "&" and "wait", which means we can run the loop in parallel processes, it will be faster.
## Also, in each cutadapt instance, the "core_numbers = 4" can be test to see if it is the best number of multiprocessing.
## (The logic of the loop doesn't change, we just beautify the code.)
# Set the number of core_numbers to use
core_numbers=${customizedCoreNumber[i]}

# Loop over r1 files
for r1_file in ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/*r1.fq; do
    # Define the output file name
    out_file="${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed/trim_$(basename ${r1_file})"

    # Run cutadapt with parallel processing
    ${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerR[i]} -o ${out_file} ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/$(basename ${r1_file}) -j ${core_numbers} &

done

# Loop over r2 files
for r2_file in ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/*r2.fq; do
    # Define the output file name
    out_file="${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed/trim_$(basename ${r2_file})"

    # Run cutadapt with parallel processing
    ${myCutadaptPath}cutadapt -e ${errorRateCutadaptor[i]} --no-indels --minimum-length ${minimumLengthCutadaptorInLoop[i]} -g ${primerR[i]} -o ${out_file} ${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/$(basename ${r2_file}) -j ${core_numbers} &
done

# Wait for all processes to finish
wait

# [20230421][test] 648 ASV in in AMD Ryzen 5 5600U with Radeon Graphics, 32GB RAM
# for loop for r1 and r2, 2 minutes 52 seconds
# [2023-04-20 17:47:37]This is cutadapt 4.3 with Python 3.10.6
# [2023-04-20 17:50:29]done
# multiprocessing for r1 and r2, 25 seconds
# [2023-04-20 19:03:58]This is cutadapt 4.3 with Python 3.10.6
# [2023-04-20 19:04:23]done


# -----------------finish of demultiplex------------------------
done
