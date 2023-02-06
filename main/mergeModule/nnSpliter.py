# (!/usr/bin/python)

# -*- coding: utf-8 -*-
import re
from os import listdir
from os.path import isfile, join
import sys

print("nnSpliter.py is running on loci: "+sys.argv[4])

# TODO 拆分10N file into 2 seperated files
# TODO
#   As is
#       input  單序列 (r1)
#       output 雙序列 (r1 ref) aligned在一個fasta內
#
#   To be
#       input  單序列 (r1) N*10
#       output ???(還需要alignment嗎)


loadpath=sys.argv[3]+sys.argv[4]+"_demultiplex/denoice_best/nonmerged/"
r1_outputLoadpath=sys.argv[3]+sys.argv[4]+"_demultiplex/denoice_best/nonmerged/r1/"
r2_outputLoadpath=sys.argv[3]+sys.argv[4]+"_demultiplex/denoice_best/nonmerged/r2/"
# outputLoadpath=sys.argv[2]+sys.argv[3]+"_demultiplex/denoice_best/nonmerged/nnSplited/"
# loadpath="C:\\Users\\kwz50\\powerbarcoder\\PowerBarcoder\\debug\\"

# sample data
target="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCTNNNNNNNNNNAGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"
r1="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCT"
r2="AGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"
filename="Teratophyllum_koordersii_Liu9823_KTHU2241_01_1.000_abundance_121_10Ncat"


# 取得所有檔案與子目錄名稱
files = listdir(loadpath)
# 創建要處理的清單
candidate_list=set()
# 以迴圈處理
for filename in files:
    if ("tempAlign.fasta" in filename) or ("temp.fasta" in filename):#跳過中繼檔，有必要之後可以每run完刪除一次
        continue
    # 產生檔案的絕對路徑
    fullpath = join(loadpath, filename)
    # 判斷 fullpath 是檔案還是目錄
    if isfile(fullpath) and (filename!="temp.fasta"):
        print("檔案：", filename)
        filename_trim=str(filename)
        # filename_trim=filename_trim.replace("_r1.al","")
        # filename_trim=filename_trim.replace("_r2.al","")
        # candidate_list.add(filename_trim)
#   elif isdir(fullpath):
#     print("目錄：", filename)
# print (candidate_list)




def nn_spliter(target,r1,r2,filename):
    pattern_for_split = r'NNNNNNNNNN'
    result=re.split(pattern_for_split,target,maxsplit=1)
    if (len(result[0])==len(r1) or len(result[0])==len(r2)) and (len(result[1])==len(r1) or len(result[1])==len(r2)):
        return result
    else:
        print("Incorrect Ns split in ",filename)

print(nn_spliter(target,r1,r2,filename))

# result1="AAGCTGGTGTCAAAGATTACCGACTGACCTACTACACCCCCGAATACAAGACCAAAGATACCGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCAGCTGAAGAAGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACTGTATGGACAGATGGATTGACCAATCTTGACCGTTACAAGGGCCGATGCTACGACATTGAACCCGTCGCTGGGGAAGAGAACCAGTATATCGCGTATGTAGCT"
# result2="AGCTTATCCTTTGGATCTATTCGAAGAAGGTTCTGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTCTTCGGATTTAAGGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATCCCTCCTGCTTATTCTAAAACTTTTATCGGACCGCCTCATGGTATTCAGGTCGAAAGGGATAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAGAATTATGGTAGAGCCGTCTAT"

# print("merge.py is ended on loci: "+sys.argv[3])


# 目的地
# /home2/barcoder_test/RUN_sk_20230103/PowerBarcoder/result/rbcLC_demultiplex/denoice_best/nonmerged/r2
# 目標是做成像這樣的內容
# >Diplopterygium_brevipinnulum_Wade4608_KTHU2019_01_r2_0.240_abundance_25
# AGTCCCAGCGTGAACATGATCTCCACCGGACATACGTAATGCTTTTGCTAATACACGGAAATGCATACCGTGATTTTTCTGTCTATCGATGACAGCATGCATTGCACGGTGAATGTGAAGAAGCAGCCCATTATCTCGACAATAGAAGGCCAAGGTAGTATTTGCGGTAAACCCTCCGGTCAGATAGTCATGCATTACAATTGGTGCCCCCAATTCTCTAGCAAAACGGGCCCTTTTCAACATTTCTTCACACGTACCTGCAGTAG
