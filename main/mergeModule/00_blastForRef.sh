# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

# refResult.txt是localBlast的結果，blastResult.txt是我們parsing後的結果，在blastResultParser.py產生的

echo "[INFO] 00_blastForRef is running"

for ((i = 0; i < "${#nameOfLoci[@]}"; i++)); do #迴圈處理，若dada2出來的nonmerge資料夾內為空，則須停止後續步驟

  # /home/lykuo/ncbi-blast-2.10.0+/bin/makeblastdb -in /home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/fermalies_rbcL.fasta -dbtype nucl -out refDB
  ${localBlastToolDir}makeblastdb -in "${ampliconInfo}""${sseqidFileName[i]}" -dbtype nucl -out "${resultDataPath}""${nameOfLoci[i]}"_result/blastResult/"${nameOfLoci[i]}"_refDB

  #這一步不需要cat了，使用R做出來的10N直接當catQuery.fas作第三步
  #cat r1
  # cat ${blastSequenceDir}r1/*.fas ${blastSequenceDir}r2/*.fas > catQuery.fas
  #cat r2
  # cat /home/sktang/powerBC/r1/*.fas /home/sktang/powerBC/r2/*.fas > catQuery.fas  #
  #cat r1 r2
  #cat ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r1/*.fas ${resultDataPath}${nameOfLoci[i]}_result/denoiseResult/denoise_best/nonmerged/r2/*.fas > ${resultDataPath}${nameOfLoci[i]}_result/blastResult/${nameOfLoci[i]}_catQuery.fas

  #cat 10N
  # 這步驟改成直接cat nonmerge資料夾裡所有的檔案
  cat "${resultDataPath}${nameOfLoci[i]}_result/mergeResult/merger/nCatR1R2/"*.fas >"${resultDataPath}${nameOfLoci[i]}_result/blastResult/${nameOfLoci[i]}_catQuery.fas"

  # /home/lykuo/ncbi-blast-2.10.0+/bin/blastn -db refDB -query catQuery.fas -num_threads 20 -out refResult.txt -outfmt 6
  ${localBlastToolDir}blastn -db "${resultDataPath}${nameOfLoci[i]}_result/blastResult/${nameOfLoci[i]}_refDB" -query "${resultDataPath}""${nameOfLoci[i]}"_result/blastResult/"${nameOfLoci[i]}"_catQuery.fas -num_threads 20 -out "${resultDataPath}""${nameOfLoci[i]}"_result/blastResult/"${nameOfLoci[i]}"_refResult.txt -outfmt 6

done

echo "[INFO] 00_blastForRef is ended"

# blast完之後要用10N拆掉，檔名可以在10Ncat後加r1(N前)或r2(N後)，後面就可以接著之前寫的，

# 先前有改檔名的，可以都以後墜的形式替換即可，要改的地方可能有三五個

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
