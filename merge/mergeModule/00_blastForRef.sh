
# 20220918 現在所有人都要從這個路徑下開始工作  /home/lykuo/lab_data/NGS_data/miseq/test_LIB720

blastdbDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"

targetLibraryFilePath="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/fermalies_rbcL.fasta"

# blastSequenceDir="/home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/rbcLC_demultiplex/denoice_best/"
blastSequenceDir="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/"

localBlastToolDir="/home/lykuo/ncbi-blast-2.10.0+/bin/"


${blastdbdir}makeblastdb -in ${targetLibraryDir} -dbtype nucl -out refDB

cat ${blastSequenceDir}r1/*.fas ${blastSequenceDir}r2/*.fas > catQuery.fas

${localBlastToolDir}blastn -db refDB -query catQuery.fas -num_threads 20 -out refResult.txt -outfmt 6


# Blast輸出的結果
# Microlepia_substrigosa_CYH20090514-016_0514-016_01_r1_0.994_abundance_2033	
# MH319942_Dennstaedtiaceae_Histiopteris_incisa	
# 94.656(this)	
# 262	(this)
# 13	
# 1	
# 1	
# 262	
# 558	
# 818	
# 1.44e-115	
# 405
# Microlepia_substrigosa_CYH20090514-0




# 20220918學長指定使用對象
# /home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/rbcLC_demultiplex/denoice_best/r1





# 20220920 Legacy
# # 20220918 現在所有人都要從這個路徑下開始工作  /home/lykuo/lab_data/NGS_data/miseq/test_LIB720


# /home/lykuo/ncbi-blast-2.10.0+/bin/makeblastdb -in /home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/fermalies_rbcL.fasta -dbtype nucl -out refDB

# cat /home/sktang/powerBC/r1/*.fas /home/sktang/powerBC/r2/*.fas > catQuery.fas

# /home/lykuo/ncbi-blast-2.10.0+/bin/blastn -db refDB -query catQuery.fas -num_threads 20 -out refResult.txt -outfmt 6



# # Microlepia_substrigosa_CYH20090514-016_0514-016_01_r1_0.994_abundance_2033	
# # MH319942_Dennstaedtiaceae_Histiopteris_incisa	
# # 94.656(this)	
# # 262	(this)
# # 13	
# # 1	
# # 1	
# # 262	
# # 558	
# # 818	
# # 1.44e-115	
# # 405
# # Microlepia_substrigosa_CYH20090514-0


# /home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/rbcLC_demultiplex/denoice_best/r1