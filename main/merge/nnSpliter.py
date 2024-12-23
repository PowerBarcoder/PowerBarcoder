#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
aim 拆分10N file into 2 separated files
do
  as is
      單序列 (r1,r2)在DADA2就做好了
  to be
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
from FastaUnit import FastaUnit, replace_filename_with_header, split_multiple_seq_fasta_into_files

print("[INFO] nnSpliter.py is running on loci: " + sys.argv[2])

main_load_path = sys.argv[1]
loci_name = sys.argv[2]
LOAD_PATH = main_load_path + loci_name + "_result/mergeResult/merger/nCatR1R2/"
SPLIT_PATH = main_load_path + loci_name + "_result/mergeResult/merger/nCatR1R2/forSplit/"
R1_OUTPUT_LOAD_PATH = main_load_path + loci_name + "_result/mergeResult/merger/r1/"
R2_OUTPUT_LOAD_PATH = main_load_path + loci_name + "_result/mergeResult/merger/r2/"

"""
nn_spliter使用時須確認檔案是否為單條序列，因為我們只讀前兩行，不接受多條序列在一個Fasta檔案中
"""


def nn_spliter(load_path, target_filename, r1_output_load_path, r2_output_load_path):
    pattern_for_split = r'NNNNNNNNNN'

    try:
        seq_header = linecache.getline(load_path + target_filename, 1).replace("\n", "")
        seq_text = linecache.getline(load_path + target_filename, 2)

        # print(load_path+target_filename)
        # print(seq_header)
        # print(seq_text)
        seq_text_splitted = re.split(pattern_for_split, seq_text, maxsplit=1)
        # print(seq_text_splitted)
        seq_text_r1 = seq_text_splitted[0]
        seq_text_r2 = seq_text_splitted[1]
        with open(r1_output_load_path + target_filename, "w", encoding="iso-8859-1") as r1_file:
            r1_file.write(seq_header + "_r1" + "\n")
            r1_file.write(seq_text_r1 + "\n")  # r1結尾需要多補一個換行
        replace_filename_with_header(r1_output_load_path + target_filename, r1_output_load_path, True)
        with open(r2_output_load_path + target_filename, "w", encoding="iso-8859-1") as r2_file:
            r2_file.write(seq_header + "_r2" + "\n")
            r2_file.write(seq_text_r2)
        replace_filename_with_header(r2_output_load_path + target_filename, r2_output_load_path, True)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {target_filename}")
        print(traceback.print_exc())
    except Exception as unknown_exception:
        print(f"[ERROR] Something went wrong with {target_filename}: {str(unknown_exception)}")
        print(traceback.print_exc())


# 取得所有檔案與子目錄名稱
raw_files = listdir(LOAD_PATH)
# 先把fasta file按abundance切分成個別檔案，檔名用流水號編
nCat_fasta_file = FastaUnit()
for filename in raw_files:
    try:
        full_path = join(LOAD_PATH, filename)
        if isfile(full_path):
            split_multiple_seq_fasta_into_files(full_path, SPLIT_PATH)
    except Exception as e:
        print(f"[ERROR] Something wrong in {filename} when split_multiple_seq_fasta_into_files(): {str(e)}")

# 檔名用header替換
split_files = listdir(SPLIT_PATH)
for filename in split_files:
    try:
        full_path = join(SPLIT_PATH, filename)
        if isfile(full_path):
            replace_filename_with_header(full_path, SPLIT_PATH, True)
    except Exception as e:
        print(f"[ERROR] Something wrong in {filename} when replace_filename_with_header(): {str(e)}")

# 取得切分後所有檔案與子目錄名稱
split_files = listdir(SPLIT_PATH)
# 以迴圈處理
process_file_number = 0
for filename in split_files:
    try:
        # 產生檔案的絕對路徑
        full_path = join(SPLIT_PATH, filename)
        # 判斷 full_path 是檔案還是目錄
        if isfile(full_path) and ('.fas' in filename[-4:]):
            # print("檔案：", filename)
            nn_spliter(SPLIT_PATH, filename, R1_OUTPUT_LOAD_PATH, R2_OUTPUT_LOAD_PATH)  # 切檔
            process_file_number += 1
        else:  # 20230415 可以考慮把r1,r2,r1ref,r2ref,mergeSeq,deGapMergeSeq,align都先排除
            print("[WARNING]" + filename, "is not a file or the filename is not end with .fas")
    except Exception as e:
        print(f"[ERROR] Something wrong in {filename} in nnSpliter.py: {str(e)}")
        print(traceback.print_exc())

print("[INFO] " + str(process_file_number), " files are split.")

print("[INFO] nnSpliter.py is ended on loci: " + sys.argv[2])


