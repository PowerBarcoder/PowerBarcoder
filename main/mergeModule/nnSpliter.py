# (!/usr/bin/python)
# -*- coding: utf-8 -*-

"""
AIM 拆分10N file into 2 seperated files
DO
  As is
      單序列 (r1,r2)在DADA2就做好了
  To be
      input  單序列 r1+N*10+r2
      output r1 & r2，要給後面的BeforeAlignment用

# 目的地：
# /home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/rbcLC_result/mergeResult/powerbarcoder/nCatR1R2/r2
# 目標生出單個r像下面的內容：
# >Diplopterygium_brevipinnulum_Wade4608_KTHU2019_01_r2_0.240_abundance_25
# AGTCCCAGCGTGAACATGATCTCCACCGGACATACGTAATGCTTTTGCTAATACACGGAAATGCATACCGTGATTTTTCTGTCTATCGATGACAGCATGCATTGCACGGTGAATGTGAAGAAGCAGCCCATTATCTCGACAATAGAAGGCCAAGGTAGTATTTGCGGTAAACCCTCCGGTCAGATAGTCATGCATTACAATTGGTGCCCCCAATTCTCTAGCAAAACGGGCCCTTTTCAACATTTCTTCACACGTACCTGCAGTAG
"""

import re
from os import listdir
from os.path import isfile, join
import sys
import linecache

print("[INFO] nnSpliter.py is running on loci: " + sys.argv[2])

loadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/powerbarcoder/nCatR1R2/"
r1_outputLoadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/powerbarcoder/r1/"
r2_outputLoadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/powerbarcoder/r2/"


def nn_spliter(loadpath, filename, r1_outputLoadpath, r2_outputLoadpath):
    pattern_for_split = r'NNNNNNNNNN'

    # TODO 這邊之後可能要改，不能只拿前兩行，要去檢查abundance (20230611確認一下是不是在balstResult的篩選條件就已經先按identity選出最像的了)
    seqHeader = linecache.getline(loadpath + filename, 1).replace("\n", "")
    seqText = linecache.getline(loadpath + filename, 2)

    # print(loadpath+filename)
    # print(seqHeader)
    # print(seqText)
    seqTextSplitted = re.split(pattern_for_split, seqText, maxsplit=1)
    # print(seqTextSplitted)
    seqTextr1 = seqTextSplitted[0]
    seqTextr2 = seqTextSplitted[1]
    with open(r1_outputLoadpath + filename, "w", encoding="UTF-8") as r1_file:
        r1_file.write(seqHeader + "_r1" + "\n")
        r1_file.write(seqTextr1 + "\n")  # r1結尾需要多補一個換行

    with open(r2_outputLoadpath + filename, "w", encoding="UTF-8") as r2_file:
        r2_file.write(seqHeader + "_r2" + "\n")
        r2_file.write(seqTextr2)


# 取得所有檔案與子目錄名稱
files = listdir(loadpath)
# 創建要處理的清單
candidate_list = set()
# 以迴圈處理
processFileNumber = 0
for filename in files:
    # 產生檔案的絕對路徑
    fullpath = join(loadpath, filename)
    # 判斷 fullpath 是檔案還是目錄
    if isfile(fullpath) and ('.fas' in filename[-4:]):
        # print("檔案：", filename)
        nn_spliter(loadpath, filename, r1_outputLoadpath, r2_outputLoadpath)  # 切檔
        processFileNumber += 1
    else:  # 20230415 可以考慮把r1,r2,r1ref,r2ref,mergeSeq,deGapMergeSeq,align都先排除
        print("[WARNING]" + filename, "is not a file or the filename is not end with .fas")
print("[INFO]" + str(processFileNumber), " files are split.")

print("[INFO] nnSpliter.py is running on loci: " + sys.argv[2])

# --------------------------------prototype--------------------------------
# # sample data
# target="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCTNNNNNNNNNNAGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"
# r1="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCT"
# r2="AGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"
# filename="Teratophyllum_koordersii_Liu9823_KTHU2241_01_1.000_abundance_121_10Ncat"
# "C:/Users/kwz50/KTHU2241_Liu9823_Teratophyllum_koordersii_.fas"


# def nn_spliter(target,r1,r2,filename):
#     pattern_for_split = r'NNNNNNNNNN'
#     result=re.split(pattern_for_split,target,maxsplit=1)
#     if (len(result[0])==len(r1) or len(result[0])==len(r2)) and (len(result[1])==len(r1) or len(result[1])==len(r2)):
#         return result
#     else:
#         print("Incorrect Ns split in ",filename)

# print(nn_spliter(target,r1,r2,filename))

# result1="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCT"
# result2="AGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"
