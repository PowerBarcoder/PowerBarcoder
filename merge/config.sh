# ! /bin/bash

# where is your NGS Data ?
mainDataPath="/home/lykuo/lab_data/NGS_data/miseq/test_pass_parameter/"

# where did you install fastp ?
myFastpPath="/home/lykuo/miniconda2/bin/"
# where is your Miseq gz data ?
myRowR1Gz="HGT22043_2_DNAL1_000000000-KHMTG_L1_R1.fastq.gz"
myRowR2Gz="HGT22043_2_DNAL1_000000000-KHMTG_L1_R2.fastq.gz"
myTrimmedR1Gz="HGT22043_2_DNAL1_000000000-KHMTG_L1_R1_trimmed.fastq.gz"
myTrimmedR2Gz="HGT22043_2_DNAL1_000000000-KHMTG_L1_R2_trimmed.fastq.gz"
summaryJsonFileName="HGT22043_2_DNAL1_000000000-KHMTG_L1.json"
summaryHtmlFileName="HGT22043_2_DNAL1_000000000-KHMTG_L1.html"


# where did you install cutadapt ?
myCutadaptPath="/home/lykuo/cutadapt-venv/bin/"
# Parameter in cutadaptor
nameOfLoci="rbcLN"
errorRateCutadaptor=0.125
minimumLengthCutadaptor=70
threadNumberCutadaptor=30
primerF="GAGACTAAAGCAGGTGTTGGATTCA"
primerR="TCAAGTCCACCRCGAAGRCATTC"
amplicon_r1="rbcLN_amplicon_r1.fq"
amplicon_r2="rbcLN_amplicon_r2.fq"
barcodesFile1='barcodes_rbcL_start_0.fasta'
barcodesFile2='barcodes_rbcLN_start2_0.fasta'
minimumLengthCutadaptorInLoop=150


# where did you unstall localBlast?
localBlastToolDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"
targetLibraryFilePath="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/fermalies_rbcL.fasta"
blastSequenceDir="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/"
# python params
sseqidFileName="fermalies_rbcL.fasta"

echo 'params imported!'