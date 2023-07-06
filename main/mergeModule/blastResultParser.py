# (!/usr/bin/python)
# -*- coding: utf-8 -*-

"""
這個檔案先呼叫blastref物件，
把00_blastForRef執行的結果(refBlast.txt)parsing成blastResult.txt，
完成後再底下的"方法們"
"""

import sys
from BlastRef import BlastRef

ampliconInfo = sys.argv[1]
resultDataPath = sys.argv[2]
blast_parsing_mode = sys.argv[3]
nameOfLoci = sys.argv[4]

print("[INFO] blastResultParser.py is running on loci: " + nameOfLoci)

localBlast = BlastRef()

# loadpath="/home/sktang/powerBC/"
# "/home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result20230206_rbcL/"
loadpath = resultDataPath

localBlast.blastRef(loadpath + nameOfLoci + "_result/blastResult/", nameOfLoci, blast_parsing_mode)

# 測試用
# localBlast.blastRef("C:/Users/123/")

#  1.	 qseqid	 query (e.g., gene) sequence id
# print(localBlast.qseqidList)
qseqidList = localBlast.qseqidList
# print(type(qseqidList))

#  2.	 sseqid	 subject (e.g., reference genome) sequence id
# print(localBlast.sseqidList)
sseqidList = localBlast.sseqidList
# print(type(sseqidList))

#  3.	 pident	 percentage of identical matches
# print(localBlast.pidentList)
pidentList = localBlast.pidentList
# print(type(pidentList))

#  4.	 length	 alignment length
# print(localBlast.lengthList)
lengthList = localBlast.lengthList
# print(type(lengthList))

#  5.	 mismatch	 number of mismatches
# print(localBlast.mismatchList)
mismatchList = localBlast.mismatchList
# print(type(mismatchList))

#  6.	 gapopen	 number of gap openings
# print(localBlast.gapopenList)
gapopenList = localBlast.gapopenList
# print(type(gapopenList))

#  7.	 qstart	 start of alignment in query
# print(localBlast.qstartList)
qstartList = localBlast.qstartList
# print(type(qstartList))

#  8.	 qend	 end of alignment in query
# print(localBlast.qendList)
qendList = localBlast.qendList
# print(type(qendList))

#  9.	 sstart	 start of alignment in subject
# print(localBlast.sstartList)
sstartList = localBlast.sstartList
# print(type(sstartList))

#  10.	 send	 end of alignment in subject
# print(localBlast.sendList)
sendList = localBlast.sendList
# print(type(sendList))

#  11.	 evalue	 expect value
# print(localBlast.evalueList)
evalueList = localBlast.evalueList
# print(type(evalueList))

#  12.	 bitscore	 bit score
# print(localBlast.bitscoreList)
bitscoreList = localBlast.bitscoreList
# print(type(bitscoreList))

#  13.   qstartMinusQend
# print(localBlast.qstartMinusQendList)
qstartMinusQendList = localBlast.qstartMinusQendList
# print(type(qstartMinusQendList))

#  14.   sstartMinusSend
# print(localBlast.sstartMinusSendList)
sstartMinusSendList = localBlast.sstartMinusSendList
# print(type(sstartMinusSendList))

#  15.   rWhoList(r1或r2)
# print(localBlast.rWhoList)
rWhoList = localBlast.rWhoList


# print(type(rWhoList))

def determineDirection(i):
    result = str(qseqidList[i]) + '\t' + str(sseqidList[i]) + '\t' + str(pidentList[i]) + '\t' + str(
        lengthList[i]) + '\t' + str(mismatchList[i]) + '\t' + str(gapopenList[i]) + '\t' + str(
        qstartList[i]) + '\t' + str(qendList[i]) + '\t' + str(sstartList[i]) + '\t' + str(sendList[i]) + '\t' + str(
        evalueList[i]) + '\t' + str(bitscoreList[i])[:-2] + '\t' + str(qstartMinusQendList[i]) + '\t' + str(
        sstartMinusSendList[i]) + '\t' + str(rWhoList[i])
    return result


# 20230206 似乎不需要用append了，因為先前已經按loci區分了
# 20230206 之前應該是因為迴圈位置的關係，所以才用append的
with open(loadpath + nameOfLoci + "_result/blastResult/" + nameOfLoci + "_blastResult.txt", "w") as file:
    for i in range(0, len(qseqidList)):
        # print(determineDirection(i))
        if "\t\t0\t0\t0\t0\t0\t0\t0\t0\t\t\t0\t0\t" not in determineDirection(i):
            file.write(determineDirection(i) + "\n")

# column info：
# str(qseqidList[i]) +'\t'+
# str(sseqidList[i])+'\t'+
# str(pidentList[i]) +'\t'+
# str(lengthList[i])+'\t'+
# str(mismatchList[i])+'\t'+
# str(gapopenList[i])+'\t'+
# str(qstartList[i])+'\t'+
# str(qendList[i])+'\t'+
# str(sstartList[i])+'\t'+
# str(sendList[i])+'\t'+
# str(evalueList[i])+'\t'+
# str(bitscoreList[i])[:-2] +'\t'+
# str(qstartMinusQendList[i])+'\t'+
# str(sstartMinusSendList[i])+'\t'+
# str(rWhoList[i])


print("[INFO] blastResultParser.py is ended on loci: " + nameOfLoci)
