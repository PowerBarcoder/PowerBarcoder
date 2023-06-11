#!/bin/bash
datetime=202306111604'/'
myCutadaptPath=/venv/cutadapt-venv/bin/
myFastpPath=/usr/local/bin/
localBlastToolDir=/usr/local/bin/
ampliconInfo=/PowerBarcoder/data/amplicon_data/
resultDataPath=/PowerBarcoder/data/result/$datetime
missList=/PowerBarcoder/data/missingList.txt
R1FastqGz=/PowerBarcoder/data/amplicon_data/RUN1-5_R1.fastq.gz
R2FastqGz=/PowerBarcoder/data/amplicon_data/RUN1-5_R2.fastq.gz
summaryJsonFileName=quality.json
summaryHtmlFileName=quality.html
dada2LearnErrorFile=/PowerBarcoder/data/dada2LearnErrorFile/
dada2BarcodeFile=multiplex_cpDNAbarcode_clean.txt
nameOfLoci+=(rbcLN)
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
primerF+=(GAGACTAAAGCAGGTGTTGGATTCA)
primerR+=(TCAAGTCCACCRCGAAGRCATTC)
barcodesFile1+=(barcodes_rbcL_start_0.fasta)
barcodesFile2+=(barcodes_rbcLN_start2_0.fasta)
sseqidFileName+=(fermalies_rbcL.fasta)
minimumLengthCutadaptorInLoop+=(150)
customizedCoreNumber+=(30)
workingDirectory=/PowerBarcoder/main/
echo '[INFO] config imported!'
