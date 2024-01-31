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
# /home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/rbcLC_result/mergeResult/merger/nCatR1R2/r2
# 目標生出單個r像下面的內容：
# >Diplopterygium_brevipinnulum_Wade4608_KTHU2019_01_r2_0.240_abundance_25
# AGTCCCAGCGTGAACATGATCTCCACCGGACATACGTAATGCTTTTGCTAATACACGGAAATGCATACCGTGATTTTTCTGTCTATCGATGACAGCATGCATTGCACGGTGAATGTGAAGAAGCAGCCCATTATCTCGACAATAGAAGGCCAAGGTAGTATTTGCGGTAAACCCTCCGGTCAGATAGTCATGCATTACAATTGGTGCCCCCAATTCTCTAGCAAAACGGGCCCTTTTCAACATTTCTTCACACGTACCTGCAGTAG
"""

import re
from os import listdir
from os.path import isfile, join
import sys
import linecache
import traceback
from FastaUnit import FastaUnit

print("[INFO] nnSpliter.py is running on loci: " + sys.argv[2])

loadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/nCatR1R2/"
splitPath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/nCatR1R2/forSplit/"
r1_outputLoadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/r1/"
r2_outputLoadpath = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/r2/"

"""
nn_spliter使用時須確認檔案是否為單條序列，因為我們只讀前兩行，不接受多條序列在一個Fasta檔案中
"""


def nn_spliter(loadpath, filename, r1_outputLoadpath, r2_outputLoadpath):
    pattern_for_split = r'NNNNNNNNNN'

    seqHeader = linecache.getline(loadpath + filename, 1).replace("\n", "")
    seqText = linecache.getline(loadpath + filename, 2)

    # print(loadpath+filename)
    # print(seqHeader)
    # print(seqText)
    seqTextSplitted = re.split(pattern_for_split, seqText, maxsplit=1)
    # print(seqTextSplitted)
    seqTextr1 = seqTextSplitted[0]
    seqTextr2 = seqTextSplitted[1]
    with open(r1_outputLoadpath + filename, "w", encoding="iso-8859-1") as r1_file:
        r1_file.write(seqHeader + "_r1" + "\n")
        r1_file.write(seqTextr1 + "\n")  # r1結尾需要多補一個換行
    nCatFastaFile.replace_filename_with_header(r1_outputLoadpath + filename, r1_outputLoadpath, True)
    with open(r2_outputLoadpath + filename, "w", encoding="iso-8859-1") as r2_file:
        r2_file.write(seqHeader + "_r2" + "\n")
        r2_file.write(seqTextr2)
    nCatFastaFile.replace_filename_with_header(r2_outputLoadpath + filename, r2_outputLoadpath, True)


# 取得所有檔案與子目錄名稱
rawFiles = listdir(loadpath)
# 先把fasta file按abundance切分成個別檔案，檔名用流水號編
nCatFastaFile = FastaUnit()
for filename in rawFiles:
    try:
        fullpath = join(loadpath, filename)
        if isfile(fullpath):
            nCatFastaFile.split_multiple_seq_fasta_into_files(fullpath, splitPath)
    except:
        print("[ERROR] Something wrong in " + filename + " when split_multiple_seq_fasta_into_files().")
        print(traceback.print_exc())

# 檔名用header替換
splitFiles = listdir(splitPath)
for filename in splitFiles:
    try:
        fullpath = join(splitPath, filename)
        if isfile(fullpath):
            nCatFastaFile.replace_filename_with_header(fullpath, splitPath, True)
    except:
        print("[ERROR] Something wrong in " + filename + " when replace_filename_with_header().")
        print(traceback.print_exc())

# 取得切分後所有檔案與子目錄名稱
splitFiles = listdir(splitPath)
# 以迴圈處理
processFileNumber = 0
for filename in splitFiles:
    try:
        # 產生檔案的絕對路徑
        fullpath = join(splitPath, filename)
        # 判斷 fullpath 是檔案還是目錄
        if isfile(fullpath) and ('.fas' in filename[-4:]):
            # print("檔案：", filename)
            nn_spliter(splitPath, filename, r1_outputLoadpath, r2_outputLoadpath)  # 切檔
            processFileNumber += 1
        else:  # 20230415 可以考慮把r1,r2,r1ref,r2ref,mergeSeq,deGapMergeSeq,align都先排除
            print("[WARNING]" + filename, "is not a file or the filename is not end with .fas")
    except:
        print("[ERROR] Something wrong in " + filename + " in nnSpliter.py.")
        print(traceback.print_exc())

print("[INFO] " + str(processFileNumber), " files are split.")

print("[INFO] nnSpliter.py is ended on loci: " + sys.argv[2])

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
