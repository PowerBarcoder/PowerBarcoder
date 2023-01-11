# ! /bin/bash

# Where is our PowerBarcoder ? 
workingDirectory="/home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/main/" #20230107 移到最底下、用參數傳進來
# Where did you install cutadapt ? 
myCutadaptPath="/home/lykuo/cutadapt-venv/bin/"
# Where did you install fastp ? 
myFastpPath="/home/lykuo/miniconda2/bin/"
# Where did you install localBlast? 
localBlastToolDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"
# Where is your NGS Data ?
mainDataPath="/home2/barcoder_test/RUN1.5/" #20230107可以改成ampliconInfo
# Where do you want to generate the results ?
resultDataPath="/home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/"
# where is your Miseq gz data ?
myTrimmedR1Gz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R1.fq.gz" #20230107可以改成R1FastqGz
myTrimmedR2Gz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R2.fq.gz" #20230107可以改成R2FastqGz

# 單次fastp的名稱，可以改成myTrimmedR2Gz.json這種感覺，避免做多次fastp有覆蓋問題
summaryJsonFileName="221229RUN1_5.json"
summaryHtmlFileName="221229RUN1_5.html"


# first dataset (We need at least on dataset)
nameOfLoci+=("rbcLC") # name of loci 
errorRateCutadaptor+=(0.125) # error rate in cutadaptor
minimumLengthCutadaptor+=(70) # minimum output sequence length in cutadaptor
threadNumberCutadaptor+=(30) # thread numbers in cutadaptor
primerF+=("TAGGTCTGTCTGCYAARAATTATGG") # front-end primer
primerR+=("GTTCCCCYTCTAGTTTRCCTACTAC") # back-end primer
amplicon_r1+=("rbcLC_amplicon_r1.fq") # amplicon files name
amplicon_r2+=("rbcLC_amplicon_r2.fq") # amplicon files name
barcodesFile1+=('barcodes_rbcLC_start_0.fasta') # barcode files name
barcodesFile2+=('barcodes_rbcLC_start2_0.fasta') # barcode files name
minimumLengthCutadaptorInLoop+=(150) # minimum output sequence length in cutadaptor
sseqidFileName+=("fermalies_rbcL.fasta") # local blast reference file name

# second dataset (Comment out if you don't need)
nameOfLoci+=("rbcLN")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
threadNumberCutadaptor+=(30)
primerF+=("GAGACTAAAGCAGGTGTTGGATTCA")
primerR+=("TCAAGTCCACCRCGAAGRCATTC")
amplicon_r1+=("rbcLN_amplicon_r1.fq")
amplicon_r2+=("rbcLN_amplicon_r2.fq")
barcodesFile1+=('barcodes_rbcL_start_0.fasta')
barcodesFile2+=('barcodes_rbcLN_start2_0.fasta')
minimumLengthCutadaptorInLoop+=(150)
sseqidFileName+=("fermalies_rbcL.fasta")

# third dataset (Comment out if you don't need)
nameOfLoci+=("trnL")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
threadNumberCutadaptor+=(30)
primerF+=("GGCAATCCTGAGCCAAATC")
primerR+=("TAGAGGGANTCGAACCCTCA")
amplicon_r1+=("trnL_amplicon_r1.fq")
amplicon_r2+=("trnL_amplicon_r2.fq")
barcodesFile1+=('barcodes_trnL_1If1_0.fasta')
barcodesFile2+=('barcodes_trnL_3exonEND_0.fasta')
minimumLengthCutadaptorInLoop+=(150)
sseqidFileName+=("ftol_sanger_alignment_trnLLF_full_f.fasta")

# fourth dataset (Comment out if you don't need)
nameOfLoci+=("trnLF")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
threadNumberCutadaptor+=(30)
primerF+=("TGAGGGTTCGANTCCCTCTA")
primerR+=("GGATTTTCAGTCCYCTGCTCT")
amplicon_r1+=("trnLF_amplicon_r1.fq")
amplicon_r2+=("trnLF_amplicon_r2.fq")
barcodesFile1+=('barcodes_trnL_3exonSTART_0.fasta')
barcodesFile2+=('barcodes_trnF_0.fasta')
minimumLengthCutadaptorInLoop+=(150)
sseqidFileName+=("ftol_sanger_alignment_trnLLF_full_f.fasta")


echo 'params imported!'
