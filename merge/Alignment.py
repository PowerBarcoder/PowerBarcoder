# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE


loadpath="/home/sktang/powerBC/"

# localblast完的序列
fastaFileDir=loadpath+"blastResult/"
fastaFileName="blastResult.txt"
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

        qseqid = qseqid=lineSplit[0]

        AligmentR1 = "mafft --thread 10 --maxiterate 16 --globalpair "+loadpath+"r1Ref/" + qseqid + "> ./aligned/" + qseqid + ".al"
        print(AligmentR1)
        AligmentR2 = "mafft --thread 10 --maxiterate 16 --globalpair "+loadpath+"r2Ref/" + qseqid + "> ./aligned/" + qseqid + ".al"
        print(AligmentR2)

        try:
            subprocess.run(AligmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(AligmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        except Exception as e:
            print(e)

# 考慮不從blastResult再讀一次檔，可以合併到BeforeAlignment底下
# mafft的結果要變單行且皆為大寫