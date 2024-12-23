# (!/usr/bin/python)
# -*- coding: utf-8 -*-

"""
這個檔案先呼叫blastref物件，
把00_blastForRef執行的結果(refBlast.txt)parsing成blastResult.txt，
完成後再底下的"方法們"
"""

import sys
from BlastRef import BlastRef
from blastRefFilter import blast_ref_filter

amplicon_info = sys.argv[1]
result_data_path = sys.argv[2]
blast_parsing_mode = sys.argv[3]
name_of_loci = sys.argv[4]

print("[INFO] blastResultParser.py is running on loci: " + name_of_loci)

# 先執行blastRefFilter.py，篩選出需要的序列
blast_ref_filter(result_data_path + name_of_loci, name_of_loci, blast_parsing_mode)

# 再執行parsing作業，這部分在20231202新增blastRefFilter.py後，雖有重工，但其產出檔案會給後續的qc使用，所以直接保留
local_blast = BlastRef()
local_blast.blast_ref(result_data_path + name_of_loci, name_of_loci, blast_parsing_mode)

# 測試用
# local_blast.blast_ref("C:/Users/123/")

# 1. qseqid query (e.g., gene) sequence id
qseqid_list = local_blast.qseqid_list

# 2. sseqid subject (e.g., reference genome) sequence id
sseqid_list = local_blast.sseqid_list

# 3. pident percentage of identical matches
pident_list = local_blast.pident_list

# 4. length alignment length
length_list = local_blast.length_list

# 5. mismatch number of mismatches
mismatch_list = local_blast.mismatch_list

# 6. gapopen number of gap openings
gapopen_list = local_blast.gapopen_list

# 7. qstart start of alignment in query
qstart_list = local_blast.qstart_list

# 8. qend end of alignment in query
qend_list = local_blast.qend_list

# 9. sstart start of alignment in subject
sstart_list = local_blast.sstart_list

# 10. send end of alignment in subject
send_list = local_blast.send_list

# 11. evalue expect value
evalue_list = local_blast.evalue_list

# 12. bitscore bit score
bitscore_list = local_blast.bitscore_list

# 13. qstartMinusQend
qstart_minus_qend_list = local_blast.qstart_minus_qend_list

# 14. sstartMinusSend
sstart_minus_send_list = local_blast.sstart_minus_send_list

# 15. rwho_list(r1或r2)
rwho_list = local_blast.rwho_list


def determine_direction(list_index: int):
    result = str(qseqid_list[list_index]) + '\t' + str(sseqid_list[list_index]) + '\t' + str(pident_list[list_index]) + '\t' + str(
        length_list[list_index]) + '\t' + str(mismatch_list[list_index]) + '\t' + str(gapopen_list[list_index]) + '\t' + str(
        qstart_list[list_index]) + '\t' + str(qend_list[list_index]) + '\t' + str(sstart_list[list_index]) + '\t' + str(send_list[list_index]) + '\t' + str(
        evalue_list[list_index]) + '\t' + str(bitscore_list[list_index])[:-2] + '\t' + str(qstart_minus_qend_list[list_index]) + '\t' + str(
        sstart_minus_send_list[list_index]) + '\t' + str(rwho_list[list_index])
    return result


# 20230206 似乎不需要用 append 了，因為先前已經按 loci 區分了
# 20230206 之前應該是因為迴圈位置的關係，所以才用 append 的
with open(result_data_path + name_of_loci + "_result/blastResult/" + name_of_loci + "_blastResult.txt", "w") as file:
    for i in range(0, len(qseqid_list)):
        # print(determine_direction(i))
        if "\t\t0\t0\t0\t0\t0\t0\t0\t0\t\t\t0\t0\t" not in determine_direction(i):
            file.write(determine_direction(i) + "\n")

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

print("[INFO] blastResultParser.py is ended on loci: " + name_of_loci)
