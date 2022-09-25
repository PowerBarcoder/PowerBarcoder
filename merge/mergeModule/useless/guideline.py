# 找reference

import glob
import sys
import os
import subprocess
from subprocess import PIPE
import collections


#  1.	 qseqid	 query (e.g., gene) sequence id
#  2.	 sseqid	 subject (e.g., reference genome) sequence id
#  3.	 pident	 percentage of identical matches
#  4.	 length	 alignment length
#  5.	 mismatch	 number of mismatches
#  6.	 gapopen	 number of gap openings
#  7.	 qstart	 start of alignment in query
#  8.	 qend	 end of alignment in query
#  9.	 sstart	 start of alignment in subject
#  10.	 send	 end of alignment in subject
#  11.	 evalue	 expect value
#  12.	 bitscore	 bit score



# shell
# blastn -db Lomariopsis_boninensis -query CRY3.fasta -num_threads 20 -out NOVO_mt_tBLASTn.txt -outfmt 6


NOVO_BLAST = open('NOVO_mt_tBLASTn.txt','r')

for line in NOVO_BLAST:
	seed = line.split('\t')[0]
    # fasta裡面的序列名稱
    # "\t"是tab
	identity = float(line.split('\t')[2])

	length = float(line.split('\t')[3])
    # 改成用8-7比較好

	if identity > 80 and length > 52:

# filter四步
        # identity>90(for rbcl)
            # 存行數 存成陣列(或看存行樹根參數組成的2維陣列會不會快一些)
            # max(list((8-7)/len(r1)))
                # 存行數 存成陣列
                # max(list(identity))
                    # 存行數 存成陣列
                    #sort(max(list(identity)))[0]
                        # 存行數 存成陣列
                        # 得出一條序列當ref，存2號欄位的result seq ID，
                        # 2、3、7、8、9、10建成表匯出

# 從檔案的目錄去抓跟2號欄位一樣的ID，抓出序列後，再下一步
# with("檔名","r")as file:
#     file.read("")
# 寫出來之後
# 要轉的reverse一下
# 下一步讀取r1或r2，
# 與ref存成一個.fs(ref在前，r1或r2在後)
# temp/blast



# 利用subprocess package執行shell指令
    # shell的mafft
    # shell: mafft --thread 10 --maxiterate 16 --globalpair 
    #     ${/home/sktang/powerBC/r1Ref/0514-016_CYH20090514-016_Microlepia_substrigosa_.fas}.fa > ./aligned/${orthogroup}_al.fa
    #         if identity > 80 and length > 52:
		remove = 'rm ./seed/' + seed + '.fasta'
		print(remove)
		try:
			subprocess.run(remove, shell=True, check=True, stdout=PIPE, stderr=PIPE)
		except Exception as e:
			print(e)
# temp/align

import glob
import sys
import os
import subprocess
from subprocess import PIPE
import collections

R1_ref = "Microlepia_substrigosa_CYH20090514-016_0514-016_01_r1.txt"
R2_ref = "Microlepia_substrigosa_CYH20090514-016_0514-016_01_r2.txt"

AligmentR1 = "mafft --thread 10 --maxiterate 16 --globalpair /home/sktang/powerBC/r1Ref/" + R1_ref + "> ./aligned/" + R1_ref + ".al"
AligmentR2 = "mafft --thread 10 --maxiterate 16 --globalpair /home/sktang/powerBC/r2Ref/" + R2_ref + "> ./aligned/" + R2_ref + ".al"

		try:
			subprocess.run(AligmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(AligmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
		except Exception as e:
			print(e)

