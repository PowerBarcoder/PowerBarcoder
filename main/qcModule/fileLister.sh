#! /bin/bash

. ./config.sh

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do

  echo "[INFO] Start to collect all files !"
  echo " " >"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

#  echo "------------------------------------Raw data------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${ampliconInfo}${R1FastqGz}" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${ampliconInfo}${R2FastqGz}" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

#  echo "-------------------------------Fastp quality trim-------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${resultDataPath}trim_R1FastqGz.gz" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${resultDataPath}trim_R2FastqGz.gz" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

#  echo "----------------------Cutadapt demultiplex by locus primer----------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r1.fq" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  seqkit stats "${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r2.fq" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"
#  echo "--------------------------------------------------------------------------------" >>"${resultDataPath}${nameOfLoci[i]}_result/qcResult/qcReport.txt"

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

  echo "[INFO] End of collecting all files !"

done
