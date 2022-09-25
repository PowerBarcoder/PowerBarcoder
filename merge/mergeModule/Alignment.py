# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE
import os

print("Alignment.py is running")

# 執行："python3 Alignment.py"，用"python Alignment.py"會報錯，要把run改成call

# loadpath="/home/sktang/powerBC/"
outputLoadpath="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/"

              # /home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/aligned

localBlastLoadpath="/home/lykuo/lab_data/NGS_data/miseq/test_LIB720/"

# localblast完的序列
fastaFileDir=localBlastLoadpath+"blastResult/"
fastaFileName="blastResult.txt"
fastaFile=fastaFileDir+fastaFileName
# print(fastaFile)

# # # 測試用路徑，上機時註解
# loadpath="C:/Users/kwz50/"
# fastaFile=loadpath+"blastResult.txt"
# sseqidFile=loadpath+"fermalies_rbcL.fasta"


if(os.path.isdir(outputLoadpath +'aligned')==False):
    # 沒資料夾就建一個資料夾
    makedir_aligned = 'mkdir '+ outputLoadpath +'aligned'
    subprocess.run(makedir_aligned, shell=True, check=True, stdout=PIPE, stderr=PIPE)


if(os.path.isdir(outputLoadpath +'mergeSeq')==False):
    # 沒資料夾就建一個資料夾
    makedir_mergeSeq = 'mkdir '+ outputLoadpath +'mergeSeq'
    subprocess.run(makedir_mergeSeq, shell=True, check=True, stdout=PIPE, stderr=PIPE)


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

        print(qseqid)
        # 都寫絕對路徑，因為執行路徑可能會變
        AligmentR1 = "mafft --thread 10 --maxiterate 16 --globalpair "+ outputLoadpath +"r1Ref/" + qseqid + "> "+outputLoadpath+"/aligned/" + qseqid +"_r1"+ ".al"
        # print(AligmentR1)
        AligmentR2 = "mafft --thread 10 --maxiterate 16 --globalpair "+ outputLoadpath +"r2Ref/" + qseqid + "> "+outputLoadpath+"/aligned/" + qseqid +"_r2"+ ".al"
        # print(AligmentR2)
                    # mafft --thread 10 --maxiterate 16 --globalpair /home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/r1Ref/KTHU2241_Liu9823_Teratophyllum_koordersii_.fas> ./aligned/KTHU2241_Liu9823_Teratophyllum_koordersii_.fas_r1.al
        try:
            subprocess.run(AligmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(AligmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            print(e)

# 考慮不從blastResult再讀一次檔，可以合併到BeforeAlignment底下
# mafft的結果要變單行且皆為大寫