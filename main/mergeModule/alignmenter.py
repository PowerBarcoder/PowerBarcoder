# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE
import os
import sys

print("[INFO] alignmenter.py is running on loci: "+sys.argv[3])

# 執行："python3 alignmenter.py"，用"python alignmenter.py"會報錯，要把run改成call

# loadpath="/home/sktang/powerBC/"
outputLoadpath=sys.argv[2]+sys.argv[3]+"_demultiplex/denoice_best/nonmerged/"

              # /home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/aligned

localBlastLoadpath=sys.argv[2]

# localblast完的序列
fastaFileDir=localBlastLoadpath+"blastResult/"
fastaFileName=sys.argv[3]+"_blastResult.txt"
fastaFile=fastaFileDir+fastaFileName
# print(fastaFile)

# # # 測試用路徑，上機時註解
# loadpath="C:/Users/kwz50/"
# fastaFile=loadpath+"blastResult.txt"
# sseqidFile=loadpath+"fermalies_rbcL.fasta"

with open(fastaFile,"r")as file:
    lines=file.readlines()
    for line in lines:
        # print (line)
        line=line.replace("\n","")
        lineSplit=line.split("\t")
        # print(lineSplit)
        qseqid=lineSplit[0]
        # sseqid=lineSplit[1]
        # sign=negativeTest(lineSplit[12],lineSplit[13])
        # forword=lineSplit[14]
        # print(qseqid+" "+sseqid+" "+sign+" "+forword)

        print("[INFO] aligning: "+qseqid) #20230104 mafft多執行續應在單檔多序列下處理才會有顯著的效能提升
        # 都寫絕對路徑，因為執行路徑可能會變
        AligmentR1 = "mafft --thread 10 --maxiterate 16 --globalpair "+ outputLoadpath +"r1Ref/" + qseqid + "> "+outputLoadpath+"aligned/" + qseqid +"_r1"+ ".al"
        # print(AligmentR1)
        AligmentR2 = "mafft --thread 10 --maxiterate 16 --globalpair "+ outputLoadpath +"r2Ref/" + qseqid + "> "+outputLoadpath+"aligned/" + qseqid +"_r2"+ ".al"
        # print(AligmentR2)
                    # mafft --thread 10 --maxiterate 16 --globalpair /home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/r1Ref/KTHU2241_Liu9823_Teratophyllum_koordersii_.fas> ./aligned/KTHU2241_Liu9823_Teratophyllum_koordersii_.fas_r1.al
                    # mafft --thread 10 --maxiterate 16 --globalpair /home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/trnLF_demultiplex/denoice_best/nonmerged/r1Ref/Co262_Lu30199_Nephrolepis_sp._.fas> /home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/trnLF_demultiplex/denoice_best/nonmerged/aligned/Co262_Lu30199_Nephrolepis_sp._.fas_r1.al                                              
        try:
            subprocess.run(AligmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(AligmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            print("[ERROR] ",e)

# 考慮不從blastResult再讀一次檔，可以合併到BeforeAlignment底下
# mafft的結果要變單行且皆為大寫

print("[INFO] alignmenter.py is ended on loci: "+sys.argv[3])