# 這個檔案先呼叫blastref物件，把blastForRef執行的結果parsing好，完成後再底下的"方法們"

# sktang@Kuo-fern-lab:~/powerBC$ python3 alignment.py

from BlastRef import BlastRef
import subprocess
from subprocess import PIPE
import os
import sys

print("BlastResult.py is running on loci: "+sys.argv[3])

localBlast=BlastRef()

# loadpath="/home/sktang/powerBC/"
loadpath=sys.argv[2]

localBlast.blastRef(loadpath,sys.argv[3])

# 測試用
# localBlast.blastRef("C:/Users/123/")

    #  1.	 qseqid	 query (e.g., gene) sequence id
# print(localBlast.qseqidList)
qseqidList=localBlast.qseqidList
# print(type(qseqidList))

    #  2.	 sseqid	 subject (e.g., reference genome) sequence id
# print(localBlast.sseqidList)
sseqidList=localBlast.sseqidList
# print(type(sseqidList))

    #  3.	 pident	 percentage of identical matches
# print(localBlast.pidentList)
pidentList=localBlast.pidentList
# print(type(pidentList))

    #  4.	 length	 alignment length
# print(localBlast.lengthList)
lengthList=localBlast.lengthList
# print(type(lengthList))

    #  5.	 mismatch	 number of mismatches
# print(localBlast.mismatchList)
mismatchList=localBlast.mismatchList
# print(type(mismatchList))

    #  6.	 gapopen	 number of gap openings
# print(localBlast.gapopenList)
gapopenList=localBlast.gapopenList
# print(type(gapopenList))

    #  7.	 qstart	 start of alignment in query
# print(localBlast.qstartList)
qstartList=localBlast.qstartList
# print(type(qstartList))

    #  8.	 qend	 end of alignment in query
# print(localBlast.qendList)
qendList=localBlast.qendList
# print(type(qendList))

    #  9.	 sstart	 start of alignment in subject
# print(localBlast.sstartList)
sstartList=localBlast.sstartList
# print(type(sstartList))

    #  10.	 send	 end of alignment in subject
# print(localBlast.sendList)
sendList=localBlast.sendList
# print(type(sendList))

    #  11.	 evalue	 expect value
# print(localBlast.evalueList)
evalueList=localBlast.evalueList
# print(type(evalueList))

    #  12.	 bitscore	 bit score
# print(localBlast.bitscoreList)
bitscoreList=localBlast.bitscoreList
# print(type(bitscoreList))

    #  13.   qstartMinusQend
# print(localBlast.qstartMinusQendList)
qstartMinusQendList=localBlast.qstartMinusQendList
# print(type(qstartMinusQendList))

    #  14.   sstartMinusSend
# print(localBlast.sstartMinusSendList)
sstartMinusSendList=localBlast.sstartMinusSendList
# print(type(sstartMinusSendList))

    #  15.   rWhoList(r1或r2)
# print(localBlast.rWhoList)
rWhoList=localBlast.rWhoList
# print(type(rWhoList))

def determineDirection(i):
    result=str(qseqidList[i]) +'\t'+str(sseqidList[i])+'\t'+str(pidentList[i]) +'\t'+str(lengthList[i])+'\t'+str(mismatchList[i])+'\t'+str(gapopenList[i])+'\t'+str(qstartList[i])+'\t'+str(qendList[i])+'\t'+str(sstartList[i])+'\t'+str(sendList[i])+'\t'+str(evalueList[i])+'\t'+str(bitscoreList[i])[:-2] +'\t'+str(qstartMinusQendList[i])+'\t'+str(sstartMinusSendList[i])+'\t'+str(rWhoList[i])
    return result


if(os.path.isdir(loadpath +'blastResult')==False):
    # 沒資料夾就建一個資料夾
    makedir_blastResult = 'mkdir '+ loadpath +'blastResult'
    subprocess.run(makedir_blastResult, shell=True, check=True, stdout=PIPE, stderr=PIPE)


for i in range(0,len(qseqidList)):
    # print(determineDirection(i))
    with open(loadpath+"blastResult/"+"blastResult.txt","a") as file:
        file.write(determineDirection(i)+"\n")
        pass

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


print("BlastResult.py is ended on loci: "+sys.argv[3])