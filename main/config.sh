# ! /bin/bash

# where is your NGS Data ?
mainDataPath="/home2/barcoder_test/RUN1.5/"

# where did you install fastp ?
myFastpPath="/home/lykuo/miniconda2/bin/"
# where is your Miseq gz data ?
#myRowR1Gz="/home/powerbarcoder/workshop/LIB214_S77_L001_R1_001.fastq.gz"
#myRowR2Gz="/home/powerbarcoder/workshop/LIB214_S77_L001_R2_001.fastq.gz"
myTrimmedR1Gz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R1.fq.gz"
myTrimmedR2Gz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R2.fq.gz"
summaryJsonFileName="221229RUN1_5.json"
summaryHtmlFileName="221229RUN1_5.html"


# where did you install cutadapt ?
myCutadaptPath="/home/lykuo/cutadapt-venv/bin/"
# Parameter in cutadaptor
nameOfLoci+=("rbcLC")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
threadNumberCutadaptor+=(30)
primerF+=("TAGGTCTGTCTGCYAARAATTATGG")
primerR+=("GTTCCCCYTCTAGTTTRCCTACTAC")
amplicon_r1+=("rbcLC_amplicon_r1.fq")
amplicon_r2+=("rbcLC_amplicon_r2.fq")
barcodesFile1+=('barcodes_rbcLC_start_0.fasta')
barcodesFile2+=('barcodes_rbcLC_start2_0.fasta')
minimumLengthCutadaptorInLoop+=(150)

# yixuan modified
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

# yixuan modified
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

# yixuan modified
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


# where did you unstall localBlast?
localBlastToolDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"
targetLibraryFilePath="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/fermalies_rbcL.fasta"
blastSequenceDir="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLC_demultiplex/denoice_best/nonmerged/"
# python params
sseqidFileName="fermalies_rbcL.fasta"

echo 'params imported!'