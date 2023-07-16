# -*- coding: utf-8 -*-

"""
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

outputLoadpath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/"
localBlastLoadpath = sys.argv[2]

# localblast完的序列
fastaFileDir = localBlastLoadpath + sys.argv[3] + "_result/blastResult/"
fastaFileName = sys.argv[3] + "_blastResult.txt"
fastaFile = fastaFileDir + fastaFileName


def align_sequence(qseqid, forward):
    # we need to avoid the situation that the filename with special characters, so we add "'" around the path string
    try:
        # r1r2分開blast
        if forward == "r1":
            AlignmentR1 = "mafft --thread 10 --localpair " + "'" + outputLoadpath + "r1Ref/" + qseqid + "'" + "> " + "'" + outputLoadpath + "aligned/" + qseqid + "'"
            subprocess.run(AlignmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        elif forward == "r2":
            AlignmentR2 = "mafft --thread 10 --localpair " + "'" + outputLoadpath + "r2Ref/" + qseqid + "'" + "> " + "'" + outputLoadpath + "aligned/" + qseqid + "'"
            subprocess.run(AlignmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        # r1r2 cat起來blast
        elif forward == "rWho":
            AlignmentR1 = "mafft --thread 10 --localpair " + "'" + outputLoadpath + "r1Ref/" + qseqid + "'" + "> " + "'" + outputLoadpath + "aligned/" + qseqid.replace(".fas","_r1.fas") + "'"
            AlignmentR2 = "mafft --thread 10 --localpair " + "'" + outputLoadpath + "r2Ref/" + qseqid + "'" + "> " + "'" + outputLoadpath + "aligned/" + qseqid.replace(".fas","_r2.fas") + "'"
            subprocess.run(AlignmentR1, shell=True, check=True, stdout=PIPE, stderr=PIPE)
            subprocess.run(AlignmentR2, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        else:
            print("[ERROR] forward is not r1,r2 or rWho")
        print("[INFO] aligned: " + qseqid)
    except Exception as e:
        print("[ERROR] failed to aligned with error message", e)


with open(fastaFile, "r") as file:
    lines = file.readlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for line in lines:
            line = line.strip()
            qseqid = line.split("\t")[0] # 第一個放qseqid
            forward = line.split("\t")[-1] # 最後一個放forward
            futures.append(executor.submit(align_sequence, qseqid, forward))
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
# 3. (V)換行在merger.py內處理，呼叫fastaUnit()處理即可

print("[INFO] alignmenter.py is ended on loci: " + sys.argv[3])
