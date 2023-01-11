# ! /bin/bash

# Where did you install cutadapt ?
myCutadaptPath="/home/lykuo/cutadapt-venv/bin/"
# Where did you install fastp ? 
myFastpPath="/home/lykuo/miniconda2/bin/"
# Where did you install localBlast? 
localBlastToolDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"
# Where is your NGS Data ?
ampliconInfo="/home2/barcoder_test/RUN1.5/" #20230107可以改成ampliconInfo  done
# Where do you want to generate the results ?
resultDataPath="/home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result/"
# where is your Miseq gz data ?
R1FastqGz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R1.fq.gz" #20230107可以改成R1FastqGz done
R2FastqGz="/home/lykuo/lab_data/NGS_data/miseq/HGT22070_Amplicon_RUN1.5/trim_RUN1.5_R2.fq.gz" #20230107可以改成R2FastqGz done

# 20230107單次fastp的名稱，可以改成R2FastqGz.json這種感覺，避免做多次fastp有覆蓋問題 TODO
summaryJsonFileName="221229RUN1_5.json"
summaryHtmlFileName="221229RUN1_5.html"

dada2LearnErrorFile="/home/lykuo/lab_data/NGS_data/miseq/HGT21056_LIB1202/error_learn/SuperRed_35"
dada2BarcodeFile="multiplex_cpDNAbarcode_clean.txt" # under dir. ampliconInfo

# first dataset (We need at least on dataset)
nameOfLoci+=("rbcLC") # name of loci 
errorRateCutadaptor+=(0.125) # error rate in cutadaptor
minimumLengthCutadaptor+=(70) # minimum output sequence length in cutadaptor
primerF+=("TAGGTCTGTCTGCYAARAATTATGG") # front-end primer
primerR+=("GTTCCCCYTCTAGTTTRCCTACTAC") # back-end primer
amplicon_r1+=("rbcLC_amplicon_r1.fq") # amplicon files name  # under dir. ampliconInfo
amplicon_r2+=("rbcLC_amplicon_r2.fq") # amplicon files name  # under dir. ampliconInfo
barcodesFile1+=('barcodes_rbcLC_start_0.fasta') # barcode files name  # under dir. ampliconInfo
barcodesFile2+=('barcodes_rbcLC_start2_0.fasta') # barcode files name  # under dir. ampliconInfo
sseqidFileName+=("fermalies_rbcL.fasta") # local blast reference file name  # under dir. ampliconInfo
minimumLengthCutadaptorInLoop+=(150) # minimum output sequence length in cutadaptor
customizedThreadNumber+=(30) # customized thread numbers

# second dataset (Comment out if you don't need)
nameOfLoci+=("rbcLN")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
primerF+=("GAGACTAAAGCAGGTGTTGGATTCA")
primerR+=("TCAAGTCCACCRCGAAGRCATTC")
amplicon_r1+=("rbcLN_amplicon_r1.fq")
amplicon_r2+=("rbcLN_amplicon_r2.fq")
barcodesFile1+=('barcodes_rbcL_start_0.fasta')
barcodesFile2+=('barcodes_rbcLN_start2_0.fasta')
sseqidFileName+=("fermalies_rbcL.fasta")
minimumLengthCutadaptorInLoop+=(150)
customizedThreadNumber+=(30)

# third dataset (Comment out if you don't need)
nameOfLoci+=("trnL")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
primerF+=("GGCAATCCTGAGCCAAATC")
primerR+=("TAGAGGGANTCGAACCCTCA")
amplicon_r1+=("trnL_amplicon_r1.fq")
amplicon_r2+=("trnL_amplicon_r2.fq")
barcodesFile1+=('barcodes_trnL_1If1_0.fasta')
barcodesFile2+=('barcodes_trnL_3exonEND_0.fasta')
sseqidFileName+=("ftol_sanger_alignment_trnLLF_full_f.fasta")
minimumLengthCutadaptorInLoop+=(150)
customizedThreadNumber+=(30)

# fourth dataset (Comment out if you don't need)
nameOfLoci+=("trnLF")
errorRateCutadaptor+=(0.125)
minimumLengthCutadaptor+=(70)
primerF+=("TGAGGGTTCGANTCCCTCTA")
primerR+=("GGATTTTCAGTCCYCTGCTCT")
amplicon_r1+=("trnLF_amplicon_r1.fq")
amplicon_r2+=("trnLF_amplicon_r2.fq")
barcodesFile1+=('barcodes_trnL_3exonSTART_0.fasta')
barcodesFile2+=('barcodes_trnF_0.fasta')
sseqidFileName+=("ftol_sanger_alignment_trnLLF_full_f.fasta")
minimumLengthCutadaptorInLoop+=(150)
customizedThreadNumber+=(30)

# Where is our PowerBarcoder ?
workingDirectory="/home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/main/" #20230107 移到最底下、用參數傳進來 done

echo 'params imported!'
