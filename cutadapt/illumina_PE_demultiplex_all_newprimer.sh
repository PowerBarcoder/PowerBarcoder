#! /bin/bash
#starting read miseq files "LIB810_S9_L001_R1_001.fastq.gz" "LIB810_S9_L001_R2_001.fastq.gz" at /home/lykuo/lab_data/NGS_data/miseq
# trim the reads
fastp -i LIB214_S77_L001_R1_001.fastq.gz -I LIB214_S77_L001_R2_001.fastq.gz -o LIB214_S77_L001_R1_001_trimmed.fastq.gz -O LIB214_S77_L001_R2_001_trimmed.fastq.gz -j LIB1202_S76_L001.json -h LIB1202_S76_L001.html

#using (universal) primer sequences to demultiplex
#rbcL C terminal
#"TAGGTCTGTCTGCYAARAATTATGG" and "GTTCCCCYTCTAGTTTRCCTACTAC" are VARIABLEs (sequences of rbcLC primers)
#"rbcLC" the name of the amplicon, which is a VARIABLE too
/home/lykuo/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g TAGGTCTGTCTGCYAARAATTATGG -G GTTCCCCYTCTAGTTTRCCTACTAC --action=none -o rbcLC.1_R1 -p rbcLC.1_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
/home/lykuo/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g GTTCCCCYTCTAGTTTRCCTACTAC -G TAGGTCTGTCTGCYAARAATTATGG --action=none -o rbcLC.2_R1 -p rbcLC.2_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
cat rbcLC.1_R1 rbcLC.2_R2 > rbcLC_amplicon_r1.fq
cat rbcLC.1_R2 rbcLC.2_R1 > rbcLC_amplicon_r2.fq
rm rbcLC.*_R*
mkdir rbcLC_demultiplex
cd rbcLC_demultiplex
#"../barcodes_rbcLC_start_0.fasta" and "../barcodes_rbcLC_start2_0.fasta" are VARIABLEs (sequences of indexed primers)
#{name1} and {name2} are header names of fasta
/home/lykuo/cutadapt-venv/bin/cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcLC_start_0.fasta -G file:../barcodes_rbcLC_start2_0.fasta --action=none -o rbcLC_{name1}_{name2}_r1.fq -p rbcLC_{name1}_{name2}_r2.fq ../rbcLC_amplicon_r1.fq ../rbcLC_amplicon_r2.fq -j 30


for File in *r1.fq
	do
	/home/lykuo/cutadapt-venv/bin/cutadapt -e 0.125 --minimum-length 200 --no-indels -g TAGGTCTGTCTGCYAARAATTATGG  -o trim_${File} ${File} -j 30
	done

for file in *r2.fq
	do
	/home/lykuo/cutadapt-venv/bin/cutadapt -e 0.125 --minimum-length 200 --no-indels -g GTTCCCCYTCTAGTTTRCCTACTAC  -o trim_${file} ${file} -j 30
	done


mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
mkdir denoice/r1
mkdir denoice/r2
mkdir denoice_best/r1
mkdir denoice_best/r2
mkdir denoice/nonmerged
mkdir denoice_best/nonmerged
mkdir denoice/nonmerged/r1
mkdir denoice_best/nonmerged/r1
mkdir denoice/nonmerged/r2
mkdir denoice_best/nonmerged/r2
cd ..

# using (universal) primer sequences to demultiplex
#rbcL N terminal
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g GAGACTAAAGCAGGTGTTGGATTCA -G TCAAGTCCACCRCGAAGRCATTC --action=none -o rbcLN.1_R1 -p rbcLN.1_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g TCAAGTCCACCRCGAAGRCATTC -G GAGACTAAAGCAGGTGTTGGATTCA --action=none -o rbcLN.2_R1 -p rbcLN.2_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
cat rbcLN.1_R1 rbcLN.2_R2 > rbcLN_amplicon_r1.fq
cat rbcLN.1_R2 rbcLN.2_R1 > rbcLN_amplicon_r2.fq
rm rbcLN.*_R*
mkdir rbcLN_demultiplex
cd rbcLN_demultiplex
~/cutadapt-venv/bin/cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_rbcL_start_0.fasta -G file:../barcodes_rbcLN_start2_0.fasta --action=none -o rbcLN_{name1}_{name2}_r1.fq -p rbcLN_{name1}_{name2}_r2.fq ../rbcLN_amplicon_r1.fq ../rbcLN_amplicon_r2.fq -j 30


for File in *r1.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 150 -g GAGACTAAAGCAGGTGTTGGATTCA  -o trim_${File} ${File} -j 30
	done

for file in *r2.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 150 -g TCAAGTCCACCRCGAAGRCATTC -o trim_${file} ${file} -j 30
	done
	

mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
mkdir denoice/r1
mkdir denoice/r2
mkdir denoice_best/r1
mkdir denoice_best/r2
mkdir denoice/nonmerged
mkdir denoice_best/nonmerged
mkdir denoice/nonmerged/r1
mkdir denoice_best/nonmerged/r1
mkdir denoice/nonmerged/r2
mkdir denoice_best/nonmerged/r2
cd ..

# using (universal) primer sequences to demultiplex
#trnL intron
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g GGCAATCCTGAGCCAAATC -G TAGAGGGANTCGAACCCTCA --action=none -o trnL.1_R1 -p trnL.1_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g TAGAGGGANTCGAACCCTCA -G GGCAATCCTGAGCCAAATC --action=none -o trnL.2_R1 -p trnL.2_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
cat trnL.1_R1 trnL.2_R2 > trnL_amplicon_r1.fq
cat trnL.1_R2 trnL.2_R1 > trnL_amplicon_r2.fq
rm trnL.*_R*
mkdir trnL_demultiplex
cd trnL_demultiplex
~/cutadapt-venv/bin/cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_trnL_1If1_0.fasta -G file:../barcodes_trnL_3exonEND_0.fasta --action=none -o trnL_{name1}_{name2}_r1.fq -p trnL_{name1}_{name2}_r2.fq ../trnL_amplicon_r1.fq ../trnL_amplicon_r2.fq -j 30


for File in *r1.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 150 -g GGCAATCCTGAGCCAAATC  -o trim_${File} ${File} -j 30
	done

for file in *r2.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 150 -g TAGAGGGANTCGAACCCTCA -o trim_${file} ${file} -j 30
	done


mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
mkdir denoice/r1
mkdir denoice/r2
mkdir denoice_best/r1
mkdir denoice_best/r2
mkdir denoice/nonmerged
mkdir denoice_best/nonmerged
mkdir denoice/nonmerged/r1
mkdir denoice_best/nonmerged/r1
mkdir denoice/nonmerged/r2
mkdir denoice_best/nonmerged/r2
cd ..

# using (universal) primer sequences to demultiplex
#trnLF IGS
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g TGAGGGTTCGANTCCCTCTA -G GGATTTTCAGTCCYCTGCTCT --action=none -o trnLF.1_R1 -p trnLF.1_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --discard-untrimmed --pair-filter=both --minimum-length 70 --pair-adapters -g GGATTTTCAGTCCYCTGCTCT -G TGAGGGTTCGANTCCCTCTA --action=none -o trnLF.2_R1 -p trnLF.2_R2 LIB214_S77_L001_R1_001_trimmed.fastq.gz LIB214_S77_L001_R2_001_trimmed.fastq.gz -j 30
cat trnLF.1_R1 trnLF.2_R2 > trnLF_amplicon_r1.fq
cat trnLF.1_R2 trnLF.2_R1 > trnLF_amplicon_r2.fq
rm trnLF.*_R*
mkdir trnLF_demultiplex
cd trnLF_demultiplex
~/cutadapt-venv/bin/cutadapt -e 0 --no-indels --pair-filter=both --discard-untrimmed -g file:../barcodes_trnL_3exonSTART_0.fasta -G file:../barcodes_trnF_0.fasta --action=none -o trnLF_{name1}_{name2}_r1.fq -p trnLF_{name1}_{name2}_r2.fq ../trnLF_amplicon_r1.fq ../trnLF_amplicon_r2.fq -j 30

for File in *r1.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 125 -g TGAGGGTTCGANTCCCTCTA -o trim_${File} ${File} -j 30
	done

for file in *r2.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 125 -g GGATTTTCAGTCCYCTGCTCT -o trim_${file} ${file} -j 30
	done

mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
mkdir denoice/r1
mkdir denoice/r2
mkdir denoice_best/r1
mkdir denoice_best/r2
mkdir denoice/nonmerged
mkdir denoice_best/nonmerged
mkdir denoice/nonmerged/r1
mkdir denoice_best/nonmerged/r1
mkdir denoice/nonmerged/r2
mkdir denoice_best/nonmerged/r2

cd ..

Rscript dada2_denoise_PE_newprimer.R > log_dada2.txt