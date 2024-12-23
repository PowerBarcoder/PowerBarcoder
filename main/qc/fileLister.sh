#! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "[INFO] Start to collect all files in ${nameOfLoci[i]}!"

  echo " " >"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

  cd "${resultDataPath}${nameOfLoci[i]}_result/"

  echo "----------------------^|${nameOfLoci[i]}^|Cutadapt demultiplex by locus primer r1----------------------" >>"${resultDataPath}overallQcReport.txt"
  seqtk fqchk "${nameOfLoci[i]}_amplicon_r1.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
  seqkit stats "${nameOfLoci[i]}_amplicon_r1.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

  echo "----------------------^|${nameOfLoci[i]}^|Cutadapt demultiplex by locus primer r2----------------------" >>"${resultDataPath}overallQcReport.txt"
  seqtk fqchk "${nameOfLoci[i]}_amplicon_r2.fq" | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
  seqkit stats "${nameOfLoci[i]}_amplicon_r2.fq" | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

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


echo "[INFO] Start to report overall qcReport!"

echo "[INFO] Decompressing ${ampliconInfo}${R1FastqGz}..."
pv -p "${ampliconInfo}${R1FastqGz}" | gunzip >"${resultDataPath}rawR1Fastq.fq"

echo "[INFO] Decompressing ${ampliconInfo}${R2FastqGz}..."
pv -p "${ampliconInfo}${R2FastqGz}" | gunzip >"${resultDataPath}rawR2Fastq.fq"

echo "[INFO] Decompressing ${resultDataPath}trim_R1FastqGz.gz..."
pv -p "${resultDataPath}trim_R1FastqGz.gz" | gunzip >"${resultDataPath}trim_R1FastqGz.fq"

echo "[INFO] Decompressing ${resultDataPath}trim_R2FastqGz.gz..."
pv -p "${resultDataPath}trim_R2FastqGz.gz" | gunzip >"${resultDataPath}trim_R2FastqGz.fq"
echo " " >"${resultDataPath}overallQcReport.txt"

cd "${resultDataPath}"

echo "[INFO] Processing rawR1Fastq.fq..."
echo "------------------------------------Raw data r1------------------------------------" >>"${resultDataPath}overallQcReport.txt"
pv rawR1Fastq.fq | seqtk fqchk - | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
pv rawR1Fastq.fq | seqkit stats - | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "[INFO] Processing rawR2Fastq.fq..."
echo "------------------------------------Raw data r2------------------------------------" >>"${resultDataPath}overallQcReport.txt"
pv rawR2Fastq.fq | seqtk fqchk - | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
pv rawR2Fastq.fq | seqkit stats - | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "[INFO] Processing trim_R1FastqGz.fq..."
echo "-------------------------------Fastp quality trim r1-------------------------------" >>"${resultDataPath}overallQcReport.txt"
pv trim_R1FastqGz.fq | seqtk fqchk - | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
pv trim_R1FastqGz.fq | seqkit stats - | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

echo "[INFO] Processing trim_R2FastqGz.fq..."
echo "-------------------------------Fastp quality trim r2-------------------------------" >>"${resultDataPath}overallQcReport.txt"
pv trim_R2FastqGz.fq | seqtk fqchk - | awk 'NR == 3 { print $8, $9 }' >>"${resultDataPath}overallQcReport.txt"
pv trim_R2FastqGz.fq | seqkit stats - | awk 'NR == 2 { print $4, $5 ,$6 ,$7 }' >>"${resultDataPath}overallQcReport.txt"
echo "--------------------------------------------------------------------------------" >>"${resultDataPath}overallQcReport.txt"

cd "${workingDirectory}"
python3 "./qc/save_overall_qc_report.py" "${resultDataPath}"

cd "${resultDataPath}"
rm "${resultDataPath}rawR1Fastq.fq"
rm "${resultDataPath}rawR2Fastq.fq"
rm "${resultDataPath}trim_R1FastqGz.fq"
rm "${resultDataPath}trim_R2FastqGz.fq"
rm "${resultDataPath}overallQcReport.txt"

echo "[INFO] End of reporting overall qcReport!"
