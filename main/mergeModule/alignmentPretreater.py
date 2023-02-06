# -*- coding: utf-8 -*-

import sys

# 製造待測序列路徑的方法
def qseqidFile(outputLoadpath,rWho,fileName):
    qseqidFileDir=outputLoadpath+rWho+"/"
    qseqidFileName=fileName
    qseqidFile=qseqidFileDir+qseqidFileName
    return qseqidFile

"""
# 先定義一個判斷正負的方法
2022年的做法是看12跟13相乘：
相乘為正就是positive，為負就是negative
20230206-10N：(沒很懂，但好像跟之前的概念一樣)
用 subject start 與 end 相減 正值或負值
再與（query start 與 end 相減）相乘決定 是否方向一至
"""
def negativeTest(a,b):
    if ((a[0]=="-")and(b[0]=="-"))or ((a[0]!="-")and(b[0]!="-")):
        return "positive"
    elif ((a[0]!="-")and(b[0]=="-")) or ((a[0]=="-")and(b[0]!="-")):
        return "negative"

# 反轉序列的方法
def ReverseComplement(seq):
    # """Return reverse complement fastaID_seq_dic, ignore gaps"""
    seq = seq.replace(' ','') #Remove space
    seq = seq.replace('\n','') #Remove LF
    seq = seq[::-1] #Reverse the fastaID_seq_dic
    basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N', 'R': 'Y', 'Y':'R', 'M': 'K', 'K': 'M', 'S': 'S', 'W': 'W', 'H': 'D', 'B': 'V'} #Make a dictionary for complement
    letters = list(seq) #Turn the fastaID_seq_dic into a list
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)+'\n' #Turn the list into a string

# 兩條序列匯出成一檔的方法
def createRefFile(rWho,rWhoRowList):
    with open (outputLoadpath+rWho+"Ref/"+qseqid,"w") as RefFile:
        finalRowList=rWhoRowList+targetRowList
        # print(finalRowList) #TODO 20230206 這邊r1開頭就少n了
        RefFile.writelines(finalRowList)
        # print(RefFile.read())

print("[INFO] alignmentPretreater.py is running on loci: "+sys.argv[4])

# loadpath="/home/sktang/powerBC/"
localBlastLoadpath=sys.argv[3]
outputLoadpath=sys.argv[3]+sys.argv[4]+"_demultiplex/denoice_best/nonmerged/"


# localblast完的序列檔案
fastaFileDir=localBlastLoadpath+"blastResult/"
fastaFileName=sys.argv[4]+"_blastResult.txt"
fastaFile=fastaFileDir+fastaFileName
# print(fastaFile)

# ref
# sseqidFileDir="/home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/"
sseqidFileDir=sys.argv[1]
# sseqidFileName="fermalies_rbcL.fasta"
sseqidFileName=sys.argv[2]

sseqidFile=sseqidFileDir+sseqidFileName

r1RowList=[]
r2RowList=[]
targetRowList=[]

with open(fastaFile,"r")as file:
    lines=file.readlines()
    for line in lines:
        # print (line)
        line=line.replace("\n","")
        lineSplit=line.split("\t")
        # print(lineSplit)
        qseqid=lineSplit[0]
        sseqid=lineSplit[1]
        sign=negativeTest(lineSplit[12],lineSplit[13])
        forword=lineSplit[14]
        # print(qseqid+" "+sseqid+" "+sign+" "+forword)

        # 已獲得所有資訊，開始分四狀況來寫alignment了
        # 0514-016_CYH20090514-016_Microlepia_substrigosa_.fas 
        # MH319942_Dennstaedtiaceae_Histiopteris_incisa 
        # positive 
        # r1

        # 待測序列r1製作
        qseqidFileStr=qseqidFile(outputLoadpath,"r1",qseqid)
        # print(qseqidFile(loadpath,forword,qseqid))
        r1RowList=[]
        with open (qseqidFileStr,"r") as qR1File:
            lines=qR1File.readlines()
            # print(lines)
            r1RowList+=lines
            # print(r1RowList)

        # 待測序列r2製作
        qseqidFileStr=qseqidFile(outputLoadpath,"r2",qseqid)
        # print(qseqidFile(loadpath,forword,qseqid))
        r2RowList=[]
        with open (qseqidFileStr,"r") as qR2File:
            lines=qR2File.readlines()
            # print(lines)
            r2RowList+=lines
            # print(r2RowList)

        # ref seq製作
        targetRowList=[]
        targetRowNumber=int(-1)
        with open (sseqidFile,"r")as sFile :
            lines=sFile.readlines()
            for line in lines:
                targetRowNumber+=1
                if line.find(sseqid)!=-1:
                    break
            targetRowList+=(lines[targetRowNumber:targetRowNumber+2])    
            # print(targetRowList)


        # if else判斷方向(多行的fasta之後再處理成一行的)

        # 2022年舊版
        # if ((sign=="negative")and(forword=="r1")):
        #     targetRowList[1]=ReverseComplement(targetRowList[1])
        #     r2RowList[1]=ReverseComplement(r2RowList[1])
        # elif ((sign=="positive")and(forword=="r1")):
        #     r2RowList[1]=ReverseComplement(r2RowList[1])
        # elif ((sign=="negative")and(forword=="r2")):
        #     r2RowList[1]=ReverseComplement(r2RowList[1])
        # elif ((sign=="positive")and(forword=="r2")):
        #     targetRowList[1]=ReverseComplement(targetRowList[1])
        #     r2RowList[1]=ReverseComplement(r2RowList[1])

        # 20230206-10N新版
        if ((sign=="negative")):
            targetRowList[1]=ReverseComplement(targetRowList[1])
            print(fastaFile)
        elif ((sign=="positive")):
            pass



        createRefFile("r1",r1RowList)
        createRefFile("r2",r2RowList)


print("[INFO] alignmentPretreater.py is ended on loci: "+sys.argv[4])

# 4.讀ref.fas
# 5.讀r1.fas
# 6.迭代queryname，用裡面的參數13及16、15(r1r2)判斷方向
# 7.找出當前迭代字串(queryname)的fas檔
# ------------------------------------------------
# 8.負的&&r1，轉ref
# 9.把rwho-1跟轉好的ref存成fas
# 10.把轉好的rwho-2跟轉好的ref存成fas
# ------------------------------------------------
# 8.正的&&r1，ref不轉
# 9.把rwho-1跟ref存成fas
# 10.把轉好的rwho-2跟ref存成fas
# ------------------------------------------------
# 8.負的&&r2，ref不轉
# 9.把rwho-1跟ref存成fas
# 10.把轉好的rwho-2跟ref存成fas
# ------------------------------------------------
# 8.正的&&r2，ref轉
# 9.把rwho-1跟ref轉存成fas
# 10.把轉好的rwho-2跟ref轉存成fas
# ------------------------------------------------
# 11.就可以alignment
