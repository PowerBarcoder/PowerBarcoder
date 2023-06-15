#! /bin/bash

. ./config.sh

echo "[INFO] Start generating quality control report !"

apt install seqkit

echo "------------------------------------Raw data------------------------------------" >> ${resultDataPath}/qcReport.txt
seqkit stats ${ampliconInfo}${R1FastqGz} >> ${resultDataPath}/qcReport.txt
seqkit stats ${ampliconInfo}${R2FastqGz} >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "-------------------------------Fastp quality trim-------------------------------" >> ${resultDataPath}/qcReport.txt
seqkit stats ${resultDataPath}trim_R1FastqGz.gz >> ${resultDataPath}/qcReport.txt
seqkit stats ${resultDataPath}trim_R2FastqGz.gz >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------Cutadapt demultiplex by locus primer----------------------" >> ${resultDataPath}/qcReport.txt
seqkit stats ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r1.fq >> ${resultDataPath}/qcReport.txt
seqkit stats ${resultDataPath}${nameOfLoci[i]}_result/${nameOfLoci[i]}_amplicon_r2.fq >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "---------------------Cutadapt demultiplex by sample barcode---------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "-------------------------Cutadapt trim the primer sites-------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------------------DADA2 filter----------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------------------DADA2 denoise---------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "-----------------------------------DADA2 merge----------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------DADA2 10N concat--------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------------------Merger blast----------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------------------Merger align----------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt
echo "----------------------------------Merger merge----------------------------------" >> ${resultDataPath}/qcReport.txt
echo "#TODO" >> ${resultDataPath}/qcReport.txt
echo "--------------------------------------------------------------------------------" >> ${resultDataPath}/qcReport.txt

rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r1
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/r2
rm -r ${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/aligned

python3 ./qcModule/missingList.py

echo "[INFO] End of generating quality control report !"
