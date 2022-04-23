from typing import List
from Miseq import Miseq
import subprocess
from subprocess import PIPE
from BlastRef import BlastRef
from FastaUnit import FastaUnit
# 會遇到bug的情況1：in、del與snp連續，即中間沒有被無變異點位隔開時，r1&ref_r1之間的點位計算會出錯(去Miseq.py改)
# 會遇到bug的情況2：只有一個位點的indel偵測不到，r1&ref_r1之間的點位計算會出錯(去Miseq.py改)
######################################
# 本腳本步驟：針對alignment完的序列merge
# 輸入序列為ref,r1,ref_r1,r2,ref_r2，共五條(看起來ref這裡用不到)
# 輸入格式要求1：align後兩條序列頭尾要切齊
# 輸入格式要求2：indel位置以"-"表示
# 輸入格式要求3：fasta內序列不得斷行，奇數行為header，偶數行為sequence(可用NCBI_00_20211007_05read_fasta_by_line_testo.py製作)
######################################
#運作流程
#r1跟其align序列ref_r1比對，獲得r1_p2及其他點位資訊
#r2跟其align序列ref_r2比對，獲得r2_p1及其他點位資訊
#用r1_p2及r2_p1判斷是否overlap
#若有overlap，分別從trim_r1及trim_r2分別取出序列長度及序列內容，再將兩overlap序列做alignment後取consensus
#拼接trim_r1[0:重疊區前]+overlap+trim_r2[重疊區後:]，並打印出結果
######################################

#  把alignment好的r1跟r2讀進來變單行(20220423)
r1_fastaUnit=FastaUnit()
r1_loadpath="C:/Users/kwz50/aligned/0514-016_CYH20090514-016_Microlepia_substrigosa_.fas_r1.al"
r1_fastaUnit.fastaUnit(r1_loadpath)
r1_seqMap=r1_fastaUnit.seqMap
        
r2_fastaUnit=FastaUnit()
r2_loadpath="C:/Users/kwz50/aligned/0514-016_CYH20090514-016_Microlepia_substrigosa_.fas_r2.al"
r2_fastaUnit.fastaUnit(r2_loadpath)
r2_seqMap=r2_fastaUnit.seqMap

# 讀兩個.fs進來當r1、ref_r1、r2、ref_r2(20220423)
r1=""
ref_r1=""
r2=""
ref_r2=""

for key, value in r1_seqMap.items():
    if "r1" in key:
        r1=value
    else:
        ref_r1=value
for key, value in r2_seqMap.items():
    if "r2" in key:
        r2=value
    else:
        ref_r2=value

# print(r1)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------tagagctgtctatgaatgccttcgtggtggacttgatttcacaaaagatgatgagaacgtaaattcccaaccattcatgcgttggagggatcgtttcttattcgtggcagaagctcttttcaaatcccaggctgaaacaggcgaaattaagggacattacttaaatgccaccgcaggtacatgtgaagagatgttgaagagagctgtttttgctagagaattgggtgcaccaattgtcatgcacgactacctgaccggagggttca-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# print(ref_r1)
# atgtcaccacaaacggagactaaagcaggtgctggattcaaagctggtgttaaagattatcgattgacctattacactcccgaatataagaccaaagacactgatattttagcagccttccgaatgaccccacaacctggagtaccagctgaggaagccggagctgcggtagctgcggaatcctccacgggtacatggaccactgtatggacagatgggcttaccagtctcgatcgttacaagggccggtgctacgatatcgaacccgtcgctggagaagaaaaccagtatattgcatatgtagcttatcccttggatctattcgaagaaggttctgtaaccaatttgttcacttcaattgtaggtaatgttttcggattcaaggccctacgcgctctacgcctagaagaccttcgaattccccccgcttattctaaaactttcattggaccgcctcacggtattcaggtcgaaagggataaactgaacaaatatggacgtcccttattggggtgtacaatcaagccaaaattgggcttgtctgctaagaattatggtagagccgtctatgaatgccttcgtggtggacttgatttcacaaaagacgatgaaaacgtaaattcccaaccattcatgcgttggagagatcgcttcttattcgtagcagaagctcttttcaaatcccaggctgaaacaggtgaaatcaagggacattacttaaatgccactgcaggtacgtgtgaagaaatgatgaagagagctgtttttgctagagaattgggtgcaccaattgtcatgcatgactacctgaccgggggatttaccgcaaataccagcttagcttattattgcagagacaatgggctgcttcttcatattcaccgtgcaatgcatgctgtcatcgatagacaacgaaatcatggtatgcacttccgtgtattggccaaagcgttacgcatgtccggcggagaccacatccacgccggaaccgtagtaggcaaactagagggggagcgagacgtcaccttgggttttgtcgatttgcttcgcgatgattacatcgaaaaagatcgtagccgcggcatctatttcacgcaggattgggtatctatgccgggtgtactccccgtagcttcagggggtatccacgtctggcacatgcccgccctaaccgaaatcttcggggacgattctgtcttacagttcggtggcggaactttgggacatccctggggaaatgcgcccggtgccgtagctaaccgagtcgcattagaagcttgtgtacaagctcgtaatgagggccgcgacctcgctcgtgaaggtaatgagatcattcgtgaagcttctaagtggagtccggaattggctgctgcatgcgaaatatggaaagccatcaaatttgagttcgagacaatcgatacgttgtaa
# print(r2)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ccaccgcaggtacatgtgaagagatgttgaagagagctgtttttgctagagaattgggtgcaccaattgtcatgcacgactacctgaccggagggttcaccgcaaataccagcttagcttatcactgcagagacaatgggctacttcttcatattcaccgcgcgatgcatgctgtcattgatagacaacgaaatcacggtatgcatttccgcgtattggctaaagcattacgcatgtccggcggagatcatatccatgccggaact------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# print(ref_r2)
# atgtcaccacaaacggagactaaagcaggtgctggattcaaagctggtgttaaagattatcgattgacctattacactcccgaatataagaccaaagacactgatattttagcagccttccgaatgaccccacaacctggagtaccagctgaggaagccggagctgcggtagctgcggaatcctccacgggtacatggaccactgtatggacagatgggcttaccagtctcgatcgttacaagggccggtgctacgatatcgaacccgtcgctggagaagaaaaccagtatattgcatatgtagcttatcccttggatctattcgaagaaggttctgtaaccaatttgttcacttcaattgtaggtaatgttttcggattcaaggccctacgcgctctacgcctagaagaccttcgaattccccccgcttattctaaaactttcattggaccgcctcacggtattcaggtcgaaagggataaactgaacaaatatggacgtcccttattggggtgtacaatcaagccaaaattgggcttgtctgctaagaattatggtagagccgtctatgaatgccttcgtggtggacttgatttcacaaaagacgatgaaaacgtaaattcccaaccattcatgcgttggagagatcgcttcttattcgtagcagaagctcttttcaaatcccaggctgaaacaggtgaaatcaagggacattacttaaatgccactgcaggtacgtgtgaagaaatgatgaagagagctgtttttgctagagaattgggtgcaccaattgtcatgcatgactacctgaccgggggatttaccgcaaataccagcttagcttattattgcagagacaatgggctgcttcttcatattcaccgtgcaatgcatgctgtcatcgatagacaacgaaatcatggtatgcacttccgtgtattggccaaagcgttacgcatgtccggcggagaccacatccacgccggaaccgtagtaggcaaactagagggggagcgagacgtcaccttgggttttgtcgatttgcttcgcgatgattacatcgaaaaagatcgtagccgcggcatctatttcacgcaggattgggtatctatgccgggtgtactccccgtagcttcagggggtatccacgtctggcacatgcccgccctaaccgaaatcttcggggacgattctgtcttacagttcggtggcggaactttgggacatccctggggaaatgcgcccggtgccgtagctaaccgagtcgcattagaagcttgtgtacaagctcgtaatgagggccgcgacctcgctcgtgaaggtaatgagatcattcgtgaagcttctaagtggagtccggaattggctgctgcatgcgaaatatggaaagccatcaaatttgagttcgagacaatcgatacgttgtaa
















# # 全部做完試trnL-F

# # trim

# r1=    "AAGCTGGTGTTAAAGATTATCGATTGACCTATTACACTCCCGAAT------CTAAAGACACTGATATCTTAGCAGCCTCCCGCATGACCCCACAACCCGGAGTACCTGCCGAGGAAGCAGGAGCTGCGGTAGCTGCGGAATCCTCAGATGGACTTACCAGTCTCGATCGGTACAAGGGCCGATGCTACGATATCGAACCCGTCGCTGGAGAGGAAAACCAGTATATTGCA---GTAG------------------------------------------------------------------------------------------------"
# ref_r1="AAGCTGGTGTTAAAGATTATCG-------TATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATG--GCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC"

# ref_ori="AAGCTGGTGTTAAAGATTATCGTATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATGGCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC"

# r2=           "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------CCCCCCCCCCTTATCCCCTGGATCTATTCGAGGAAGGTTCCGTTACTAATTTGTTCACTTCCATTGTAGGTAATGTTTTCGGATTTAAGGCCCTACGCGCTTTACGCCTAGAAGACCTTCGAATTCCCCCTGCCTATTCCAAAACTTTCATTGGACCACCTCATGGTATTCAGGTCGAAAGAGACAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTGGGCTTGTCCGCTAAGAATTATGGTAGAGCTGTCT"
# ref_r2=       "AAGCTGGTGTTAAAGATTATCGTATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATG--GCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# # 方法：取出字典裡最大key值裡面的value
# # 步驟三會用到
# def keywithmaxval(d):
#      v=list(d.values())
#      k=list(d.keys())
#      return k[v.index(max(v))]


# # main方法
# # 步驟一
# # 先建立物件，再呼叫方法獲得拼接資訊，再印出來看看有沒有對
# r1Object=Miseq()
# Miseq.stickSiteFinder(r1Object,r1,ref_r1)
# r2Object=Miseq()
# Miseq.stickSiteFinder(r2Object,r2,ref_r2)
# print(r1Object.show())
# # forword: True, stickSite: 166, F_Rtrim: 96, del: {45: 6, 173: 96}, in: {22: 7}
# print(r2Object.show())
# # forword: False, stickSite: 164, F_Rtrim: 163, del: {0: 163}, in: {262: 168}


# # 應當在判斷overlap之前，就取得r1_p2跟r2_p1
# # 這步可從Miseq獲得
# # stickSite：r1_p2：228，從237+7+2(r1最後一個del加上sigma的in)來的
# # stickSite：r2_p1：222，從221+1(r2第一個del加1)來的
# # 再來，用stickSite判斷是否重疊，即步驟二

# # 步驟二
# # 以r1_p2跟r2_p1判斷兩物件拼接方向
# overlape=False
# if(r1Object.forword==True)and(r2Object.forword!=True) :
#     if r1Object.stickSite>=r2Object.stickSite:
#         # print("overlap1")
#         merge_list=[r1,r2]
#         F_Rtrim=[r1Object.F_Rtrim,r2Object.F_Rtrim]
#         overlape=True
#     elif r1Object.stickSite<r2Object.stickSite:
#         # print("add Ns1")
#         merge_list=[r1,r2]
#         F_Rtrim=[r1Object.F_Rtrim,r2Object.F_Rtrim]
#         overlape=False
# elif(r2Object.forword==True)and(r1Object.forword!=True) :
#     if r2Object.stickSite>=r1Object.stickSite:
#         # print("overlap2")
#         merge_list=[r2,r1]
#         F_Rtrim=[r2Object.F_Rtrim,r1Object.F_Rtrim]
#         overlape=True
#     elif r2Object.stickSite<r1Object.stickSite:
#         # print("add Ns2")
#         merge_list=[r2,r1]
#         F_Rtrim=[r2Object.F_Rtrim,r1Object.F_Rtrim]
#         overlape=False
# else:
#     print("甚麼情況?不用merge了吧")


# # 判斷完overlap之後，真的overlap時，
# # 需要算出按trim過的r1跟r2獲得應overlap的序列(trim_X_overlap)，即步驟三

# # 步驟三
# # 開始拼接，若有重疊則進行alignment
# merge_seq=""
# # 拼接前先把r1 r2 trim好
# trim_0=merge_list[0].replace("-","")
# trim_1=merge_list[1].replace("-","")

# # 不用拼
# if (overlape==False):
#     pass

# # 要拼
# elif(overlape==True):
#     # print("overlap")
#     # 有overlap才需要merge
#     overlap_num=abs(r1Object.stickSite-r2Object.stickSite)+1

#     # 用overlap_num分別計算兩序列的重疊區塊之鹼基數
#     # 先算頭
#     if (merge_list[0]==r1):
#         overlap_num_r1=overlap_num

#         r1StartSite=r1Object.stickSite

#         # print(r1Object.inSite)
#         for i in (r1Object.inSite):
#             # print(r1Object.inSite[i])
#             # print((keywithmaxval(r1Object.delSite)-overlap_num),(i+r1Object.inSite[i]),keywithmaxval(r1Object.delSite))
#             if((keywithmaxval(r1Object.delSite)-overlap_num)<(i+r1Object.inSite[i])<keywithmaxval(r1Object.delSite)):
#                 overlap_num_r1=overlap_num_r1+r1Object.inSite[i]
#         # print(r1Object.delSite)
#         for i in (r1Object.delSite):
#             # print(r1Object.delSite[i])
#             # print((keywithmaxval(r1Object.delSite)-overlap_num),(i+r1Object.inSite[i]),keywithmaxval(r1Object.delSite))
#             if((keywithmaxval(r1Object.delSite)-overlap_num)<(i+r1Object.delSite[i])<keywithmaxval(r1Object.delSite)):
#                 overlap_num_r1=overlap_num_r1-r1Object.delSite[i]
#         print("r1在頭",overlap_num_r1)
#         trim_0_overlap=trim_0[len(trim_0)-overlap_num_r1:]
#         print(trim_0_overlap)
#     elif(merge_list[0]==r2):
#         overlap_num_r2=overlap_num
        
#         r2StartSite=keywithmaxval(r2Object.delSite)
#         for i in (r2Object.inSite):
#             r2StartSite=r2StartSite-r2Object.inSite[i]
            
#         # print(r2Object.inSite)
#         for i in (r2Object.inSite):
#             # print(r2Object.inSite[i])
#             # print((keywithmaxval(r2Object.delSite)-overlap_num),(i+r2Object.inSite[i]),keywithmaxval(r2Object.delSite))
#             if((keywithmaxval(r2Object.delSite)-overlap_num)<(i+r2Object.inSite[i])<keywithmaxval(r2Object.delSite)):
#                 overlap_num_r2=overlap_num_r2+r2Object.inSite[i]
#         # print(r2Object.delSite)
#         for i in (r2Object.delSite):
#             # print(r2Object.delSite[i])
#             # print((keywithmaxval(r2Object.delSite)-overlap_num),(i+r2Object.inSite[i]),keywithmaxval(r2Object.delSite))
#             if((keywithmaxval(r2Object.delSite)-overlap_num)<(i+r2Object.delSite[i])<keywithmaxval(r2Object.delSite)):
#                 overlap_num_r2=overlap_num_r2-r2Object.delnSite[i]
#         print("r2在頭",overlap_num_r2)
#         trim_0_overlap=trim_0[len(trim_0)-overlap_num_r2:]
#         print(trim_0_overlap)

#     # 再算尾
#     if (merge_list[1]==r1):
#         overlap_num_r1=overlap_num
#         # print(r1Object.inSite)
#         for i in (r1Object.inSite):
#             # print(r1Object.inSite[i])
#             # print(0,(i-r1Object.F_Rtrim),overlap_num))
#             if(0<(i-r1Object.F_Rtrim)<overlap_num):
#                 overlap_num_r1=overlap_num_r1+r1Object.inSite[i]
#         # print(r1Object.delSite)
#         for i in (r1Object.delSite):
#             # print(r1Object.delSite[i])
#             # print(0,(i-r1Object.F_Rtrim),overlap_num))
#             if(0<(i-r1Object.F_Rtrim)<overlap_num):
#                 overlap_num_r1=overlap_num_r1-r1Object.delnSite[i]
#         print("r1在尾",overlap_num_r1)
#         trim_1_overlap=trim_1[:overlap_num_r1]
#         print(trim_1_overlap)
#     elif(merge_list[1]==r2):
#         overlap_num_r2=overlap_num
#         # print(r2Object.inSite)
#         for i in (r2Object.inSite):
#             # print(r2Object.inSite[i])
#             # print(0,(i-r2Object.F_Rtrim),overlap_num)
#             if(0<(i-r2Object.F_Rtrim)<overlap_num):
#                 overlap_num_r2=overlap_num_r2+r2Object.inSite[i]
#         # print(r2Object.delSite)
#         for i in (r2Object.delSite):
#             # print(r2Object.delSite[i])
#             # print(0,(i-r2Object.F_Rtrim),overlap_num)
#             if(0<(i-r2Object.F_Rtrim)<overlap_num):
#                 overlap_num_r2=overlap_num_r2-r2Object.delnSite[i]
#         print("r2在尾",overlap_num_r2)
#         trim_1_overlap=trim_1[:overlap_num_r2]
#         print(trim_1_overlap)


# # 步驟四(執行alignment)
# # if(ovelap區間的序列內容跟長度完全一樣):
# # 不用align
# if(trim_0_overlap==trim_1_overlap):
#     pass
# # elif(ovelap區間的序列長度一樣):
# # 也不用align
# elif(len(trim_0_overlap)==len(trim_1_overlap)):
#     pass
# # else:
# # 在py裡做shell，先把overlap區段degap，然後r1 r2兩個overlap去align
# else:
#     alignment = 'your alignment shell script'
#     print(alignment)
#     try:
#         subprocess.run(alignment, shell=True, check=True, stdout=PIPE, stderr=PIPE)
#     except Exception as e:
#         print("error occured:",e)


# # 步驟五
# # 依alignment結果拼接重疊區塊
# # 接MAFFT前先用其他軟體跑的結果當例子
# # CAGTAG---
# # CCCCCCCCC
# trim_0_overlap_align="CAGTAG---"
# trim_1_overlap_align="CCCCCCCCC"

# merge_seq=""

# # 開始判斷並拼接
# if (overlape==False):
#     # print("Ns")
#     ns_num=abs(r1Object.stickSite-r2Object.stickSite)-1
#     ns_seq="N"*ns_num
#     print("ns_seq",ns_seq)
#     print("ns_num",ns_num)
#     merge_seq=merge_seq+trim_0+ns_seq+trim_1
# elif(overlape==True):
#     # print("overlap")
#     # 有overlap才需要merge
#     overlap_seq=""
#     overlap_num_align=len(trim_0_overlap_align)
#     gapNumInOverlap=0
#     for i in range(0,overlap_num_align):
#         # print(i+1,"and",j)
#         # print(trim_0_overlap_align[i],trim_1_overlap_align[i])
#         if (trim_0_overlap_align[i]=="A" and trim_1_overlap_align[i]=="A") :
#             overlap_seq=overlap_seq+"A"
#         elif (trim_0_overlap_align[i]=="T" and trim_1_overlap_align[i]=="T") :
#             overlap_seq=overlap_seq+"T"
#         elif (trim_0_overlap_align[i]=="C" and trim_1_overlap_align[i]=="C") :
#             overlap_seq=overlap_seq+"C"
#         elif (trim_0_overlap_align[i]=="G" and trim_1_overlap_align[i]=="G") :
#             overlap_seq=overlap_seq+"G"
#         elif ((trim_0_overlap_align[i]=="A" and trim_1_overlap_align[i]=="G") or (trim_0_overlap_align[i]=="G" and trim_1_overlap_align[i]=="A")):# R	A/G
#             overlap_seq=overlap_seq+"R"
#         elif ((trim_0_overlap_align[i]=="C" and trim_1_overlap_align[i]=="T") or (trim_0_overlap_align[i]=="T" and trim_1_overlap_align[i]=="C")):# Y C/T
#             overlap_seq=overlap_seq+"Y"
#         elif ((trim_0_overlap_align[i]=="A" and trim_1_overlap_align[i]=="C") or (trim_0_overlap_align[i]=="C" and trim_1_overlap_align[i]=="A")):# M A/C
#             overlap_seq=overlap_seq+"M"
#         elif ((trim_0_overlap_align[i]=="G" and trim_1_overlap_align[i]=="T") or (trim_0_overlap_align[i]=="T" and trim_1_overlap_align[i]=="G")):# K G/T
#             overlap_seq=overlap_seq+"K"
#         elif ((trim_0_overlap_align[i]=="G" and trim_1_overlap_align[i]=="C") or (trim_0_overlap_align[i]=="C" and trim_1_overlap_align[i]=="G")):# S G/C
#             overlap_seq=overlap_seq+"S"
#         elif ((trim_0_overlap_align[i]=="A" and trim_1_overlap_align[i]=="T") or (trim_0_overlap_align[i]=="T" and trim_1_overlap_align[i]=="A")):# W A/T
#             overlap_seq=overlap_seq+"W"
#         # D G/A/T # V G/A/C # B G/T/C # H A/T/C 兩條序列不會出現
#         elif ((trim_0_overlap_align[i]=="-" ) or (trim_1_overlap_align[i]=="-")):# N A/G/C/T/-
#             overlap_seq=overlap_seq+"N"
#             gapNumInOverlap+=1

#             # gap+gap=N
#             # gap+ATCG=atcg

#         else:
#             print("出錯了GG")
#     print("overlap_num_align",overlap_num_align)
#     print("overlap_seq",overlap_seq)
#     merge_seq=merge_seq+trim_0[0:len(trim_0)-(overlap_num-gapNumInOverlap)]+overlap_seq+trim_1[overlap_num-gapNumInOverlap:]

# print(merge_seq)

# # print("總長："+str(len(ref_str_final))+"，重疊位點="+str(overlap))

# # print(r1Object)
# # {'forword': True, 'stickSiteFinder': 166, 'F_Rtrim': 96, 'del': {45: 6, 173: 96}, 'in': {22: 7}}
# # True表示放ref頭端，拼接點(r1_p2)在166，因為是從頭，所以trim尾部，後面就是indel的位置跟長度
# # print(r2Object)
# # {'forword': False, 'stickSiteFinder': 164, 'F_Rtrim': 163, 'del': {0: 163}, 'in': {262: 168}}
# # False表示放ref尾端，拼接點(r2_p1)在164，因為是從尾，所以trim頭部，後面就是indel的位置跟長度

