#!/usr/bin/python
# -*- coding: utf-8 -*-
from Miseq import Miseq
import subprocess
from subprocess import PIPE
from FastaUnit import FastaUnit
from os import listdir
from os.path import isfile, isdir, join
import sys
from os import path
import time

print("merge2nd.py is running on loci: "+sys.argv[3])

# nonmerge的
loadpath=sys.argv[2]+sys.argv[3]+"_demultiplex/denoice_best/nonmerged/deGapMergeSeq/"
# dada2 merge的
loadpath2=sys.argv[2]+sys.argv[3]+"_demultiplex/denoice_best/nonmerged/deGapMergeSeq/"
mergepath=sys.argv[2]+sys.argv[3]+"_demultiplex/denoice_best/mergeResult/"

# 取得所有檔案與子目錄名稱
files = listdir(loadpath)

# 創建要處理的清單
candidate_list=set()

# 以迴圈處理
for filename in files:
  if ("tempAlign.fasta" in filename) or ("temp.fasta" in filename):#跳過中繼檔，有必要之後可以每run完刪除一次
    continue  
#   print(filename) 
  # 產生檔案的絕對路徑
  fullpath = join(loadpath, filename)
  # 判斷 fullpath 是檔案還是目錄
  if isfile(fullpath) and (filename!="temp.fasta"):
    # print("檔案：", filename)
    filename_trim=str(filename)
    # filename_trim=filename_trim.replace("_r1.al","")
    # filename_trim=filename_trim.replace("_r2.al","")
    candidate_list.add(filename_trim)

# 開始成對處理r1及r2
for filename in candidate_list:
    try:
        #  把alignment好的r1跟r2讀進來變單行
        r1_fastaUnit = FastaUnit()
        # r1_loadpath = loadpath+filename+"_r1.al"
        r1_loadpath = loadpath+filename
        r1_fastaUnit.fastaUnit(r1_loadpath)
        r1_seqMap = r1_fastaUnit.seqMap

        r2_fastaUnit = FastaUnit()
        # r2_loadpath = loadpath+filename+"_r2.al"
        r2_loadpath = loadpath+filename
        r2_fastaUnit.fastaUnit(r2_loadpath)
        r2_seqMap = r2_fastaUnit.seqMap

        # 讀兩個.fs進來當r1、ref_r1、r2、ref_r2(20220423)
        r1 = ""
        r1_header_name=""
        ref_r1 = ""
        r2 = ""
        r2_header_name=""
        ref_r2 = ""

        for key, value in r1_seqMap.items():
            if "r1" in key:
                r1 = value
                r1_header_name="_".join(key.split("_")[-5:])
            else:
                ref_r1 = value
        for key, value in r2_seqMap.items():
            if "r2" in key:
                r2 = value
                r2_header_name="_".join(key.split("_")[-5:])
            else:
                ref_r2 = value

        # 方法：取出字典裡最大key值裡面的value
        # 步驟三會用到(現在不會了)
        def keywithmaxval(d):
            v = list(d.values())
            k = list(d.keys())
            return k[v.index(max(v))]

        # 步驟一
        # 先建立物件，再呼叫方法獲得拼接資訊 (這步主要看Miseq.py的邏輯有沒有寫對)
        r1Object = Miseq()
        Miseq.stickSiteFinder(r1Object,filename, r1, ref_r1, "r1")
        r2Object = Miseq()
        Miseq.stickSiteFinder(r2Object,filename, r2, ref_r2, "r2")

        # # 步驟二
        # # 以r1_p2跟r2_p1判斷兩物件是否重疊
        overlape = False
        merge_list = [r1, r2]

        r1_p2 = r1Object.stickSite[1]
        r1_p2_trimed = r1Object.stickSite[1]
        r1_delSite = r1Object.delSite
        for key, value in r1_delSite.items():
            if r1_p2 > key:
                r1_p2_trimed = r1_p2_trimed-value

        r2_p1 = r2Object.stickSite[1]
        r2_p1_trimed = r2Object.stickSite[1]
        r2_delSite = r2Object.delSite
        for key, value in r2_delSite.items():
            if r2_p1 > key:
                r2_p1_trimed = r2_p1_trimed-value

        # 要減一下
        if(r1Object.forword == True) and (r2Object.forword != True):
            if r1_p2_trimed >= r2_p1_trimed:
                # print("overlap1")
                overlape = True
            elif r1_p2_trimed < r2_p1_trimed:
                # print("add Ns1")
                overlape = False
            else:
                print("merge2nd.py 163: something wrong")


        # # 步驟三
        # # 開始拼接，若有重疊才於第四步進行alignment

        if (overlape == False):# 不用拼(跳步驟五)
            pass

        elif(overlape == True):# 要拼
            # 先取出需要align的兩個片段(r1_p1~r1_p2、r2_p1~r2_p2)
            # 獲得ref內的拼接長度

            align_length_in_ref = r1_p2_trimed-r2_p1_trimed

            r1_delSite_in_overlap_seq=0
            for key, value in r1_delSite.items():
                if r1_p2-align_length_in_ref < key+value:
                    r1_delSite_in_overlap_seq=r1_delSite_in_overlap_seq+value

            r2_delSite_in_overlap_seq=0
            for key, value in r2_delSite.items():
                if r2_p1+align_length_in_ref > key:
                    r2_delSite_in_overlap_seq=r2_delSite_in_overlap_seq+value

            modify_index=1
            
            r1_p1=r1_p2-align_length_in_ref-r1_delSite_in_overlap_seq+modify_index
            r2_p2=r2_p1+align_length_in_ref+r2_delSite_in_overlap_seq-modify_index
            
            r1_for_align=r1[r1_p1-1:r1_p2] # print(r1_for_align)
            r2_for_align=r2[r2_p1:r2_p2+1] # print(r2_for_align)

            # 看起來要寫個檔案先存起來 (20230111這步ok)
            aligntext=">r1\n"+r1_for_align+"\n"+">r2\n"+r2_for_align
            with open(loadpath+"mafft/"+filename+"temp.fasta","w",encoding="UTF-8") as file:
                file.write(aligntext)


            # 步驟四(執行alignment)
            # if(ovelap區間的序列內容跟長度完全一樣):
            # 不用align
            if(r1_for_align==r2_for_align):
                # print("序列長一樣，不用alignment")
                r1_overlap = r1_for_align
                r2_overlap = r2_for_align
            # elif(ovelap區間的序列長度一樣):
            # 也不用align
            elif(len(r1_for_align)==len(r2_for_align)):
                # print("序列一樣長，不用alignment")
                r1_overlap = r1_for_align
                r2_overlap = r2_for_align
            # else:
            # 在py裡做shell，先把overlap區段degap，然後r1 r2兩個overlap去align
            else:
                alignment = "mafft --thread 1 --maxiterate 16 --globalpair "+loadpath+"mafft/"+filename+"temp.fasta"  + "> "+loadpath+"mafft/"+filename+"tempAlign.fasta"
                # print(alignment)
                try:
                    subprocess.run(alignment, shell=True, check=True, stdout=PIPE, stderr=PIPE)
                except Exception as e:
                    print("error occured:",e)

                while ((path.exists(loadpath+"mafft/"+filename+"tempAlign.fasta")== False)):
                    print(filename+"tempAlign.fasta未生成，等待一秒")
                    time.sleep(1)

                aligned_fastaUnit = FastaUnit()
                aligned_fastaUnit.fastaUnit(loadpath+"mafft/"+filename+"tempAlign.fasta")
                aligned_seqMap = aligned_fastaUnit.seqMap
                r1_overlap = ""
                r2_overlap = ""

                for key, value in aligned_seqMap.items():
                    if "r1" in key:
                        r1_overlap = value
                    else:
                        r2_overlap = value
        # print(aligned_seqMap) # print(r1_overlap) # print(r2_overlap)

        # # 步驟五
        # # 依alignment結果拼接重疊區塊

        merge_seq=""
        trim_0_overlap_align=""
        trim_1_overlap_align=""

        # 開始判斷並拼接
        if (overlape==False):
            # 沒overlap就補NNNNN   # print("non-overlap",filename)# print("Ns")
            ns_num=abs(r2Object.stickSite[1]-r1Object.stickSite[1])# 原本這樣寫，有問題 ns_num=r1_p2_trimed - r2_p1_trimed-1
            ns_seq="N"*ns_num
            merge_seq=merge_seq+r1[:r1Object.stickSite[1]].upper()+ns_seq+r2[r2Object.stickSite[1]:].upper()
        elif(overlape==True):
            # 有overlap才需要merge # print("overlap")
            overlap_seq=""
            trim_0_overlap_align=r1_overlap
            trim_1_overlap_align=r2_overlap
            overlap_num_align=len(trim_0_overlap_align)
            gapNumInOverlap=0
            for i in range(0,overlap_num_align):
                # print(i+1,"and",j) # print(trim_0_overlap_align[i],trim_1_overlap_align[i])
                if (trim_0_overlap_align[i]=="a" and trim_1_overlap_align[i]=="a") :
                    overlap_seq=overlap_seq+"A"
                elif (trim_0_overlap_align[i]=="t" and trim_1_overlap_align[i]=="t") :
                    overlap_seq=overlap_seq+"T"
                elif (trim_0_overlap_align[i]=="c" and trim_1_overlap_align[i]=="c") :
                    overlap_seq=overlap_seq+"C"
                elif (trim_0_overlap_align[i]=="g" and trim_1_overlap_align[i]=="g") :
                    overlap_seq=overlap_seq+"G"
                elif ((trim_0_overlap_align[i]=="a" and trim_1_overlap_align[i]=="g") or (trim_0_overlap_align[i]=="g" and trim_1_overlap_align[i]=="a")):# R	A/G
                    overlap_seq=overlap_seq+"R"
                elif ((trim_0_overlap_align[i]=="c" and trim_1_overlap_align[i]=="t") or (trim_0_overlap_align[i]=="t" and trim_1_overlap_align[i]=="c")):# Y C/T
                    overlap_seq=overlap_seq+"Y"
                elif ((trim_0_overlap_align[i]=="a" and trim_1_overlap_align[i]=="c") or (trim_0_overlap_align[i]=="c" and trim_1_overlap_align[i]=="a")):# M A/C
                    overlap_seq=overlap_seq+"M"
                elif ((trim_0_overlap_align[i]=="g" and trim_1_overlap_align[i]=="t") or (trim_0_overlap_align[i]=="t" and trim_1_overlap_align[i]=="g")):# K G/T
                    overlap_seq=overlap_seq+"K"
                elif ((trim_0_overlap_align[i]=="g" and trim_1_overlap_align[i]=="c") or (trim_0_overlap_align[i]=="c" and trim_1_overlap_align[i]=="g")):# S G/C
                    overlap_seq=overlap_seq+"S"
                elif ((trim_0_overlap_align[i]=="a" and trim_1_overlap_align[i]=="t") or (trim_0_overlap_align[i]=="t" and trim_1_overlap_align[i]=="a")):# W A/T
                    overlap_seq=overlap_seq+"W"
                elif ((trim_0_overlap_align[i]=="-" ) and (trim_1_overlap_align[i]=="-")):# gap+gap=N
                    overlap_seq=overlap_seq+"N"
                    gapNumInOverlap+=1
                elif ((trim_0_overlap_align[i]=="-" and trim_1_overlap_align[i]!="-")):
                    # gap+ATCG=atcg
                    overlap_seq=overlap_seq+trim_1_overlap_align[i]
                elif ((trim_0_overlap_align[i]!="-" and trim_1_overlap_align[i]=="-")):
                    # ATCG+gap=atcg
                    overlap_seq=overlap_seq+trim_0_overlap_align[i]
                # D G/A/T # V G/A/C # B G/T/C # H A/T/C 兩條序列不會出現
                else:
                    print("出錯了GG")
            # print("overlap_num_align",overlap_num_align)
            # print("overlap_seq",overlap_seq)
            merge_seq=merge_seq+r1[:r1_p1-1].upper()+overlap_seq+r2[r2_p2+1:].upper() # print(merge_seq)
            merge_seq=merge_seq.replace("-","")
            
        # 步驟六：收尾  # print(merge_seq)
        output_filename=filename.replace("_.fas","")
        output_filename=output_filename+"_"+r1_header_name+"_"+r2_header_name

        merge_seq_text=">"+output_filename+"\n"+merge_seq+"\n" #處理mergeseq
        with open(mergepath+filename,"w",encoding="UTF-8") as file:
            file.write(merge_seq_text)

    except Exception as e:
        print(e)
        print("merge2nd.py 319: something wrong.",filename)

print("merge2nd.py is ended on loci: "+sys.argv[3])