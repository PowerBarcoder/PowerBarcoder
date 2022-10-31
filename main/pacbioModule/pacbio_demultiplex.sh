fastp -i analysis-unknown-2500-m54089_210627_073255.Q20.fastq -o trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq -w 30

seqkit seq trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq -r -p -o trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq_rev

#rbcL
# 這邊的GTAGTAGGYAAACTAGARGGGGAAC式已經從config反轉過的序列
~/cutadapt-venv/bin/cutadapt  -e 0.25 -g one=GAGACTAAAGCAGGTGTTGGATTCA -a one=GTAGTAGGYAAACTAGARGGGGAAC --action=none --discard-untrimmed -o rbcL_{name}_amplicon trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq -j 30
~/cutadapt-venv/bin/cutadapt  -e 0.25 -g two=GAGACTAAAGCAGGTGTTGGATTCA -a two=GTAGTAGGYAAACTAGARGGGGAAC --action=none --discard-untrimmed -o rbcL_{name}_amplicon trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq_rev -j 30

# rmdup移除重複的
cat rbcL_*_amplicon | seqkit rmdup -n -o rbcL_amplicon_all
rm rbcL_*_amplicon

# 迴圈做demultiplex
mkdir rbcL_demultiplex
cd rbcL_demultiplex
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 70 -g file:../barcodes_rbcL_start.fasta --discard-untrimmed --action=none -o rbcL_{name} ../rbcL_amplicon_all -j 30
find -size 0 -print -delete
for temp in rbcL_*
# barcodes_rbcL_end.fasta這個檔案再別人準備的時候是前者，我們要幫他轉成後者(^NNaacctacgGAGACTAA -->GGGGAACgagacgacNN$)
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels -a file:../barcodes_rbcL_end.fasta --discard-untrimmed --action=none -o dd_${temp}_{name}.fq ${temp} -j 30
	rm ${temp}
	done
find -size 0 -print -delete
for fq in dd_rbcL_fVGF_*_0_rVVG_*_0.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.25 --minimum-length 70 -g GAGACTAAAGCAGGTGTTGGATTCA...GTAGTAGGYAAACTAGARGGGGAAC -o trim_${fq} ${fq} -j 30
	done
mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
cd ..

#trnLLF
~/cutadapt-venv/bin/cutadapt  -e 0.25 -g one=ATGGCGRAATGGTAGACGC -a one=AGAGCAGRGGACTGAAAATCC --action=none --discard-untrimmed -o trnLLF_{name}_amplicon trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq -j 30
~/cutadapt-venv/bin/cutadapt  -e 0.25 -g two=ATGGCGRAATGGTAGACGC -a two=AGAGCAGRGGACTGAAAATCC --action=none --discard-untrimmed -o trnLLF_{name}_amplicon trim_analysis-unknown-2500-m54089_210627_073255.Q20.fastq_rev -j 30

cat trnLLF_*_amplicon | seqkit rmdup -n -o trnLLF_amplicon_all
rm trnLLF_*_amplicon

mkdir trnLLF_demultiplex
cd trnLLF_demultiplex
~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels --minimum-length 70 -g file:../barcodes_trnLLF_start.fasta --discard-untrimmed --action=none -o trnLLF_{name} ../trnLLF_amplicon_all -j 30
find -size 0 -print -delete
for temp in trnLLF_*
	do
	~/cutadapt-venv/bin/cutadapt -e 0.125 --no-indels -a file:../barcodes_trnLLF_end.fasta --discard-untrimmed --action=none -o dd_${temp}_{name}.fq ${temp} -j 30
	rm ${temp}
	done
find -size 0 -print -delete
for fq in dd_trnLLF_L0725_*_0_F4121_*_0.fq
	do
	~/cutadapt-venv/bin/cutadapt -e 0.25 --minimum-length 70 -g ATGGCGRAATGGTAGACGC...AGAGCAGRGGACTGAAAATCC -o trim_${fq} ${fq} -j 30
	done
mkdir trimmed
mv trim_* ./trimmed/
mkdir denoice
mkdir denoice_best
cd ..

Rscript dada2_denoise_pacbio.R > log_dada2.txt