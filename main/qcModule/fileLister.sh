#! /bin/bash

. ./config.sh

echo "[INFO] Start to report overall qcReport!"

gunzip -c "${ampliconInfo}${R1FastqGz}" > "${resultDataPath}rawR1Fastq.fq"
gunzip -c "${ampliconInfo}${R2FastqGz}" > "${resultDataPath}rawR2Fastq.fq"
gunzip -c "${resultDataPath}trim_R1FastqGz.gz" > "${resultDataPath}trim_R1FastqGz.fq"
gunzip -c "${resultDataPath}trim_R2FastqGz.gz" > "${resultDataPath}trim_R2FastqGz.fq"

echo " " >"${resultDataPath}overallQcReport.txt"

cd "${resultDataPath}"
echo "------------------------------------Raw data r1------------------------------------" >>"${resultDataPath}overallQcReport.txt"
seqtk fqchk "rawR1Fastq.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
seqkit stats "rawR1Fastq.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "------------------------------------Raw data r2------------------------------------" >>"${resultDataPath}overallQcReport.txt"
seqtk fqchk "rawR2Fastq.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
seqkit stats "rawR2Fastq.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "-------------------------------Fastp quality trim r1-------------------------------" >>"${resultDataPath}overallQcReport.txt"
seqtk fqchk "trim_R1FastqGz.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
seqkit stats "trim_R1FastqGz.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "-------------------------------Fastp quality trim r2-------------------------------" >>"${resultDataPath}overallQcReport.txt"
seqtk fqchk "trim_R2FastqGz.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
seqkit stats "trim_R2FastqGz.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

rm "${resultDataPath}rawR1Fastq.fq"
rm "${resultDataPath}rawR2Fastq.fq"
rm "${resultDataPath}trim_R1FastqGz.fq"
rm "${resultDataPath}trim_R2FastqGz.fq"

echo "[INFO] End of reporting overall qcReport!"

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "[INFO] Start to collect all files in ${nameOfLoci[i]}!"

  echo " " >"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cat "${resultDataPath}overallQcReport.txt" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  cd "${resultDataPath}${nameOfLoci[i]}_result/"

  echo "----------------------Cutadapt demultiplex by locus primer r1----------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  seqtk fqchk "${nameOfLoci[i]}_amplicon_r1.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  seqkit stats "${nameOfLoci[i]}_amplicon_r1.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "----------------------Cutadapt demultiplex by locus primer r2----------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  seqtk fqchk "${nameOfLoci[i]}_amplicon_r2.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  seqkit stats "${nameOfLoci[i]}_amplicon_r2.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "-------------------Cutadapt demultiplex by sample barcode r1--------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/" && ls *r1.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "-------------------Cutadapt demultiplex by sample barcode r2--------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/untrimmed/" && ls *r2.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "-----------------------Cutadapt trim the primer sites r1------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed/" && ls *r1.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "-----------------------Cutadapt trim the primer sites r2------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed/" && ls *r2.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "----------------------------------DADA2 filter r1--------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/filtered/" && ls *r1.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "----------------------------------DADA2 filter r2--------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/filtered/" && ls *r2.fq >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "--------------------------------DADA2 denoise r1--------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/r1" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "--------------------------------DADA2 denoise r2--------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/r2" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "-----------------------------------DADA2 merge----------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/dada2/merged/" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "--------------------------------DADA2 10N concat--------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2/" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "--------------------------------Merger blast r1---------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1Ref/" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "--------------------------------Merger blast r2---------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2Ref/" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  #echo "----------------------------------Merger align----------------------------------" >> "${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  #echo "#TODO" >> "${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  #echo "--------------------------------------------------------------------------------" >> "${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "----------------------------------Merger merge----------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  cd "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/merged/" && ls *.fas >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  echo "[INFO] End of collecting all files in ${nameOfLoci[i]}!"

done

rm "${resultDataPath}overallQcReport.txt"