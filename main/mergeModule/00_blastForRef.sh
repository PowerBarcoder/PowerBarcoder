# ! /bin/bash

. ./config.sh

# 20220918 現在所有人都要從這個路徑下開始工作  /home/lykuo/lab_data/NGS_data/miseq/test_LIB720
echo "00_blastForRef is running"


# TODO #2 這邊要考慮把前一次blast的東西刪掉，不然blastResult.txt會沒有


for ((i=0; i<${#nameOfLoci[@]}; i++)) #迴圈處理，若dada2出來的nonmerge資料夾內為空，則須停止後續步驟
do

# ${localBlastToolDir}makeblastdb -in ${targetLibraryFilePath} -dbtype nucl -out refDB
# /home/lykuo/ncbi-blast-2.10.0+/bin/makeblastdb -in /home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/fermalies_rbcL.fasta -dbtype nucl -out refDB
${localBlastToolDir}makeblastdb -in ${mainDataPath}${sseqidFileName} -dbtype nucl -out ${resultDataPath}${nameOfLoci[i]}_refDB

# cat ${blastSequenceDir}r1/*.fas ${blastSequenceDir}r2/*.fas > catQuery.fas
# cat /home/sktang/powerBC/r1/*.fas /home/sktang/powerBC/r2/*.fas > catQuery.fas
cat ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r1/*.fas ${resultDataPath}${nameOfLoci[i]}_demultiplex/denoice_best/nonmerged/r2/*.fas > ${resultDataPath}${nameOfLoci[i]}_catQuery.fas

# ${localBlastToolDir}blastn -db refDB -query catQuery.fas -num_threads 20 -out refResult.txt -outfmt 6
# /home/lykuo/ncbi-blast-2.10.0+/bin/blastn -db refDB -query catQuery.fas -num_threads 20 -out refResult.txt -outfmt 6
${localBlastToolDir}blastn -db ${resultDataPath}${nameOfLoci[i]}_refDB -query ${resultDataPath}${nameOfLoci[i]}_catQuery.fas -num_threads 20 -out ${resultDataPath}${nameOfLoci[i]}_refResult.txt -outfmt 6

done

echo "00_blastForRef is ended"

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