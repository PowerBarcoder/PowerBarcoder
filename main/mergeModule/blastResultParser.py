# (!/usr/bin/python)
# -*- coding: utf-8 -*-

"""
這個檔案先呼叫blastref物件，
把00_blastForRef執行的結果(refBlast.txt)parsing成blastResult.txt，
完成後再底下的"方法們"
"""

import sys
from BlastRef import BlastRef
from blastRefFilter import blastRefFilter

ampliconInfo = sys.argv[1]
resultDataPath = sys.argv[2]
blast_parsing_mode = sys.argv[3]
nameOfLoci = sys.argv[4]

print("[INFO] blastResultParser.py is running on loci: " + nameOfLoci)

# 先執行blastRefFilter.py，篩選出需要的序列
blastRefFilter(resultDataPath + nameOfLoci, nameOfLoci, blast_parsing_mode)

# 再執行parsing作業，這部分在20231202新增blastRefFilter.py後，雖有重工，但其產出檔案會給後續的qc使用，所以直接保留
localBlast = BlastRef()
localBlast.blast_ref(resultDataPath + nameOfLoci, nameOfLoci, blast_parsing_mode)

# 測試用
# localBlast.blast_ref("C:/Users/123/")

#  1.	 qseqid	 query (e.g., gene) sequence id
# print(localBlast.qseqid_list)
qseqid_list = localBlast.qseqid_list
# print(type(qseqid_list))

#  2.	 sseqid	 subject (e.g., reference genome) sequence id
# print(localBlast.sseqid_list)
sseqid_list = localBlast.sseqid_list
# print(type(sseqid_list))

#  3.	 pident	 percentage of identical matches
# print(localBlast.pident_list)
pident_list = localBlast.pident_list
# print(type(pident_list))

#  4.	 length	 alignment length
# print(localBlast.length_list)
length_list = localBlast.length_list
# print(type(lengthList))

#  5.	 mismatch	 number of mismatches
# print(localBlast.mismatch_list)
mismatch_list = localBlast.mismatch_list
# print(type(mismatch_list))

#  6.	 gapopen	 number of gap openings
# print(localBlast.gapopen_list)
gapopen_list = localBlast.gapopen_list
# print(type(gapopen_list))

#  7.	 qstart	 start of alignment in query
# print(localBlast.qstart_list)
qstart_list = localBlast.qstart_list
# print(type(qstart_list))

#  8.	 qend	 end of alignment in query
# print(localBlast.qend_list)
qend_list = localBlast.qend_list
# print(type(qend_list))

#  9.	 sstart	 start of alignment in subject
# print(localBlast.sstart_list)
sstart_list = localBlast.sstart_list
# print(type(sstart_list))

#  10.	 send	 end of alignment in subject
# print(localBlast.send_list)
send_list = localBlast.send_list
# print(type(send_list))

#  11.	 evalue	 expect value
# print(localBlast.evalue_list)
evalue_list = localBlast.evalue_list
# print(type(evalue_list))

#  12.	 bitscore	 bit score
# print(localBlast.bitscore_list)
bitscore_list = localBlast.bitscore_list
# print(type(bitscore_list))

#  13.   qstartMinusQend
# print(localBlast.qstart_minus_qend_list)
qstart_minus_qend_list = localBlast.qstart_minus_qend_list
# print(type(qstart_minus_qend_list))

#  14.   sstartMinusSend
# print(localBlast.sstart_minus_send_list)
sstart_minus_send_list = localBlast.sstart_minus_send_list
# print(type(sstart_minus_send_list))

#  15.   rwho_list(r1或r2)
# print(localBlast.rwho_list)
rwho_list = localBlast.rwho_list


# print(type(rwho_list))

def determineDirection(i):
    result = str(qseqid_list[i]) + '\t' + str(sseqid_list[i]) + '\t' + str(pident_list[i]) + '\t' + str(
        length_list[i]) + '\t' + str(mismatch_list[i]) + '\t' + str(gapopen_list[i]) + '\t' + str(
        qstart_list[i]) + '\t' + str(qend_list[i]) + '\t' + str(sstart_list[i]) + '\t' + str(send_list[i]) + '\t' + str(
        evalue_list[i]) + '\t' + str(bitscore_list[i])[:-2] + '\t' + str(qstart_minus_qend_list[i]) + '\t' + str(
        sstart_minus_send_list[i]) + '\t' + str(rwho_list[i])
    return result


# 20230206 似乎不需要用append了，因為先前已經按loci區分了
# 20230206 之前應該是因為迴圈位置的關係，所以才用append的
with open(resultDataPath + nameOfLoci + "_result/blastResult/" + nameOfLoci + "_blastResult.txt", "w") as file:
    for i in range(0, len(qseqid_list)):
        # print(determineDirection(i))
        if "\t\t0\t0\t0\t0\t0\t0\t0\t0\t\t\t0\t0\t" not in determineDirection(i):
            file.write(determineDirection(i) + "\n")

# column info：
# str(qseqid_list[i]) +'\t'+
# str(sseqid_list[i])+'\t'+
# str(pident_list[i]) +'\t'+
# str(length_list[i])+'\t'+
# str(mismatch_list[i])+'\t'+
# str(gapopen_list[i])+'\t'+
# str(qstart_list[i])+'\t'+
# str(qend_list[i])+'\t'+
# str(sstart_list[i])+'\t'+
# str(send_list[i])+'\t'+
# str(evalue_list[i])+'\t'+
# str(bitscore_list[i])[:-2] +'\t'+
# str(qstart_minus_qend_list[i])+'\t'+
# str(sstart_minus_send_list[i])+'\t'+
# str(rwho_list[i])


print("[INFO] blastResultParser.py is ended on loci: " + nameOfLoci)
