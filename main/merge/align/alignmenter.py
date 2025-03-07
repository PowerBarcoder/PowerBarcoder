# -*- coding: utf-8 -*-

"""
@file alignmenter.py
@brief Aligns sequences using MAFFT based on BLAST results.

We read the file {{locus}}_blastResult.txt to get the list of readsID,
for each read, we aligned them with MAFFT.

The input files are in
{{locus}}_result/mergeResult/merger/r1Ref/ and
{{locus}}_result/mergeResult/merger/r2Ref/,
and the file name is {{readsID}}.

The output files are in {{locus}}_result/mergeResult/merger/aligned/,
and the file name is {{readsID}}_r1.al and {{readsID}}_r2.al.
"""

import concurrent.futures
import subprocess
from subprocess import PIPE
import sys

print("[INFO] alignmenter.py is running on loci: " + sys.argv[3])

output_loadpath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/"
local_blast_loadpath = sys.argv[2]

# localblast完的序列
fasta_file_dir = local_blast_loadpath + sys.argv[3] + "_result/blastResult/"
fasta_file_name = sys.argv[3] + "_blastResult.txt"
fasta_file = fasta_file_dir + fasta_file_name

"""
@brief Aligns the sequence using MAFFT.
@param qseqid: The query sequence ID.
@param forward: The direction of the sequence (r1, r2, or rwho).
@return: None
@exception Exception: If alignment fails.
"""
def align_sequence(qseqid: str, forward: str):
    # we need to avoid the situation that the filename with special characters, so we add "'" around the path string
    try:
        # r1r2分開blast
        if forward == "r1":
            alignment_r1 = "mafft --thread 10 --localpair " + "'" + output_loadpath + "r1Ref/" + qseqid + "'" + "> " + "'" + output_loadpath + "aligned/" + qseqid + "'"
            subprocess.run(alignment_r1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        elif forward == "r2":
            alignment_r2 = "mafft --thread 10 --localpair " + "'" + output_loadpath + "r2Ref/" + qseqid + "'" + "> " + "'" + output_loadpath + "aligned/" + qseqid + "'"
            subprocess.run(alignment_r2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        # r1r2 cat起來blast
        elif forward == "rwho":
            alignment_r1 = "mafft --thread 10 --localpair " + "'" + output_loadpath + "r1Ref/" + qseqid + "'" + "> " + "'" + output_loadpath + "aligned/" + qseqid.replace(
                ".fas", "_r1.fas") + "'"
            alignment_r2 = "mafft --thread 10 --localpair " + "'" + output_loadpath + "r2Ref/" + qseqid + "'" + "> " + "'" + output_loadpath + "aligned/" + qseqid.replace(
                ".fas", "_r2.fas") + "'"
            subprocess.run(alignment_r1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(alignment_r2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        else:
            print("[ERROR] forward is not r1,r2 or rWho")
        print("[INFO] aligned: " + qseqid)
    except Exception as e:
        print("[ERROR] failed to aligned with error message", e)


with open(fasta_file, "r") as file:
    lines = file.readlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for line in lines:
            line = line.strip()
            target_qseqid = line.split("\t")[0]  # 第一個放qseqid
            target_forward = line.split("\t")[-1]  # 最後一個放forward
            futures.append(executor.submit(align_sequence, target_qseqid, target_forward))
        concurrent.futures.wait(futures)

# [2023-04-20][test] 635 reads in AMD Ryzen 5 5600U with Radeon Graphics, 32GB RAM
# 迴圈處理, 45秒
# [2023-04-20 14:11:46][INFO] alignmenter.py is running on loci: rbcLN
# [2023-04-20 14:12:31][INFO] alignmenter.py is ended on loci: rbcLN
# coroutine處理, 18秒
# [2023-04-20 14:20:14][INFO] alignmenter.py is running on loci: rbcLN
# [2023-04-20 14:20:32][INFO] alignmenter.py is ended on loci: rbcLN


# [2023-04-20] mafft的結果要變單行且皆為大寫
# 1. (X)可用"--keeplowercase" 保留小寫,但其他全都維持大寫
# 2. (V)在merger.py內全轉大寫即可
# 3. (V)換行在merger.py內處理，呼叫fasta_unit()處理即可

print("[INFO] alignmenter.py is ended on loci: " + sys.argv[3])
