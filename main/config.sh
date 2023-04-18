#!/bin/bash
myCutadaptPath=/venv/cutadapt-venv/bin/
myFastpPath=deprecated
localBlastToolDir=/usr/local/bin/
ampliconInfo=/PowerBarcoder/data/amplicon_data/
resultDataPath=/PowerBarcoder/data/result/
missList=/PowerBarcoder/data/missingList.txt
R1FastqGz=/PowerBarcoder/data/amplicon_data/trim_RUN1.5_R1.fq.gz
R2FastqGz=/PowerBarcoder/data/amplicon_data/trim_RUN1.5_R2.fq.gz
summaryJsonFileName=221229RUN1_5.json
summaryHtmlFileName=221229RUN1_5.html
dada2LearnErrorFile=/PowerBarcoder/data/dada2LearnErrorFile/
dada2BarcodeFile=multiplex_cpDNAbarcode_clean.txt
nameOfLoci+=(rbcLN)
nameOfLoci+=(trnLF)
errorRateCutadaptor+=(0.125)
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
minimumLengthCutadaptor+=(70)
primerF+=(GAGACTAAAGCAGGTGTTGGATTCA)
primerF+=(TGAGGGTTCGANTCCCTCTA)
primerR+=(TCAAGTCCACCRCGAAGRCATTC)
primerR+=(GGATTTTCAGTCCYCTGCTCT)
amplicon_r1+=(rbcLN_amplicon_r1.fq)
amplicon_r1+=(trnLF_amplicon_r1.fq)
amplicon_r2+=(rbcLN_amplicon_r2.fq)
amplicon_r2+=(trnLF_amplicon_r2.fq)
barcodesFile1+=(barcodes_rbcL_start_0.fasta)
barcodesFile1+=(barcodes_trnL_3exonSTART_0.fasta)
barcodesFile2+=(barcodes_rbcLN_start2_0.fasta)
barcodesFile2+=(barcodes_trnF_0.fasta)
sseqidFileName+=(fermalies_rbcL.fasta)
sseqidFileName+=(ftol_sanger_alignment_trnLLF_full_f.fasta)
minimumLengthCutadaptorInLoop+=(150)
minimumLengthCutadaptorInLoop+=(150)
customizedThreadNumber+=(30)
customizedThreadNumber+=(30)
workingDirectory=/PowerBarcoder/main/
echo '[INFO] config imported!'
