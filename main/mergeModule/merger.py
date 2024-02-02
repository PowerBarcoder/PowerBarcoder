#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import sys
import time
import traceback
from os import listdir
from os import path
from os.path import isfile, join
from subprocess import PIPE

from FastaUnit import FastaUnit
from Miseq import Miseq


def get_overlap_seq(trim_0, trim_1):
    if trim_0 == trim_1:
        return trim_0.upper()  # Use the same letter and make it uppercase
    elif {trim_0, trim_1} == {'a', 'g'}:
        return "R"
    elif {trim_0, trim_1} == {'c', 't'}:
        return "Y"
    elif {trim_0, trim_1} == {'a', 'c'}:
        return "M"
    elif {trim_0, trim_1} == {'g', 't'}:
        return "K"
    elif {trim_0, trim_1} == {'g', 'c'}:
        return "S"
    elif {trim_0, trim_1} == {'a', 't'}:
        return "W"
    elif trim_0 == trim_1 == "-":
        return "N"
    elif trim_0 == "-":
        return trim_1
    elif trim_1 == "-":
        return trim_0
    else:
        raise ValueError("[ERROR] Unexpected alignment: {} and {}".format(trim_0, trim_1))


def merge():
    print("[INFO] merger.py is running on loci: " + sys.argv[3])

    ######################################
    # 運作流程
    # r1跟其align序列ref_r1比對，獲得r1_p2及其他點位資訊
    # r2跟其align序列ref_r2比對，獲得r2_p1及其他點位資訊
    # 用r1_p2及r2_p1判斷是否overlap
    # 若有overlap，將兩overlap序列做alignment後取consensus
    # 拼接r1[0:重疊區前]+overlap+r2[重疊區後:]，trim完，打印結果並存到"/home/sktang/powerBC/mergeSeq/"
    ######################################

    # 指定要列出的檔案目錄
    loadpath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/aligned/"
    mergepath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/rawMerged/"
    degapMergepath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/merged/"

    # 取得所有檔案與子目錄名稱
    files = listdir(loadpath)

    # 創建要處理的清單
    candidate_list = set()

    # 以迴圈處理
    for filename in files:
        if ("tempAlign.fasta" in filename) or ("temp.fasta" in filename):  # 跳過中繼檔，有必要之後可以每run完刪除一次
            continue
        #   print(filename)
        # 產生檔案的絕對路徑
        fullpath = join(loadpath, filename)
        # 判斷 fullpath 是檔案還是目錄
        if isfile(fullpath) and (filename != "temp.fasta"):
            # print("檔案：", filename)
            filename_trim = str(filename)
            filename_trim = filename_trim.replace("_r1.fas", "")
            filename_trim = filename_trim.replace("_r2.fas", "")
            candidate_list.add(filename_trim)

    # 開始成對處理r1及r2
    for filename in candidate_list:
        try:
            #  把alignment好的r1跟r2讀進來變單行
            r1_loadpath = loadpath + filename + "_r1.fas"  # r1_loadpath = loadpath+0514-016_CYH20090514-016_Microlepia_substrigosa_.fas_r1.al
            r2_loadpath = loadpath + filename + "_r2.fas"  # r2_loadpath = "C:/Users/kwz50/aligned/0514-016_CYH20090514-016_Microlepia_substrigosa_.fas_r2.al"

            # 若因為沒有blast到東西，那這對就不要往下做了，直接換下一對ASV
            if not path.exists(r1_loadpath):
                print("[INFO] " + r1_loadpath + " not found, skip this pair")
                continue
            if not path.exists(r2_loadpath):
                print("[INFO] " + r2_loadpath + " not found, skip this pair")
                continue

            r1_fasta_unit = FastaUnit()
            r2_fasta_unit = FastaUnit()

            r1_fasta_unit.fasta_unit(r1_loadpath)
            r2_fasta_unit.fasta_unit(r2_loadpath)

            r1_seq_map = r1_fasta_unit.seq_map
            r2_seq_map = r2_fasta_unit.seq_map

            # 讀兩個.fs進來當r1、ref_r1、r2、ref_r2(20220423)
            r1 = ""
            r1_header_name = ""
            ref_r1 = ""
            r2 = ""
            r2_header_name = ""
            ref_r2 = ""

            for key, value in r1_seq_map.items():
                if "r1" in key:
                    r1 = value
                    r1_header_name = "_".join(key.split("_")[-5:])
                else:
                    ref_r1 = value
            for key, value in r2_seq_map.items():
                if "r2" in key:
                    r2 = value
                    r2_header_name = "_".join(key.split("_")[-5:])
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
            # TODO 在r1,r2分開blast後，需檢查ref_r1與ref_r2是否為一樣的序列
            r1Object = Miseq()
            Miseq.stick_site_finder(r1Object, filename, r1, ref_r1, "r1")
            r2Object = Miseq()
            Miseq.stick_site_finder(r2Object, filename, r2, ref_r2, "r2")
            # print(r1Object.show()) # forword: True, stick_site(r1_p2,r2_p1): 237, F_Rtrim: deprecated_parameter, del_site: {22: 7, 234: 2}, inSite: {45: 6, 230: 3, 237: 96}
            # print(r2Object.show()) # forword: False, stick_site(r1_p2,r2_p1): 221, F_Rtrim: deprecated_parameter, del_site: {227: 2, 326: 168}, inSite: {0: 221}

            # # 步驟二
            # # 以r1_p2跟r2_p1判斷兩物件是否重疊
            overlape = False
            merge_list = [r1, r2]

            r1_p2 = r1Object.stick_site[1]
            r1_p2_trimed = r1Object.stick_site[1]
            r1_del_site = r1Object.del_site
            for key, value in r1_del_site.items():
                if r1_p2 > key:
                    r1_p2_trimed = r1_p2_trimed - value
            # print (r1_p2_trimed)

            r2_p1 = r2Object.stick_site[1]
            r2_p1_trimed = r2Object.stick_site[1]
            r2_del_site = r2Object.del_site
            for key, value in r2_del_site.items():
                if r2_p1 > key:
                    r2_p1_trimed = r2_p1_trimed - value
            # print(r2_p1_trimed)

            # 要減一下
            if (r1Object.forword == True) and (r2Object.forword != True):
                if r1_p2_trimed >= r2_p1_trimed:
                    # print("overlap1")
                    overlape = True
                elif r1_p2_trimed < r2_p1_trimed:
                    # print("add Ns1")
                    overlape = False
                else:
                    print("[WARNING] merger.py 163: something wrong")

            # # 步驟三
            # # 開始拼接，若有重疊才於第四步進行alignment

            if not overlape:  # 不用拼(跳步驟五)
                pass

            elif overlape:  # 要拼
                # 先取出需要align的兩個片段(r1_p1~r1_p2、r2_p1~r2_p2)
                # 獲得ref內的拼接長度

                align_length_in_ref = r1_p2_trimed - r2_p1_trimed

                r1_del_site_in_overlap_seq = 0
                for key, value in r1_del_site.items():
                    if r1_p2 - align_length_in_ref < key + value:
                        r1_del_site_in_overlap_seq = r1_del_site_in_overlap_seq + value

                r2_del_site_in_overlap_seq = 0
                for key, value in r2_del_site.items():
                    if r2_p1 + align_length_in_ref > key:
                        r2_del_site_in_overlap_seq = r2_del_site_in_overlap_seq + value

                modify_index = 1

                r1_p1 = r1_p2 - align_length_in_ref - r1_del_site_in_overlap_seq + modify_index
                r2_p2 = r2_p1 + align_length_in_ref + r2_del_site_in_overlap_seq - modify_index

                r1_for_align = r1[r1_p1 - 1:r1_p2]  # print(r1_for_align)
                r2_for_align = r2[r2_p1:r2_p2 + 1]  # print(r2_for_align)

                # 10N： r1_for_align跟r2_for_align要先degap
                # 20230206 我決定在這邊做degap(所以下一行多加了".replace("-","")")
                aligntext = ">r1\n" + r1_for_align.replace("-", "") + "\n" + ">r2\n" + r2_for_align.replace("-", "")
                with open(loadpath + "mafft/" + filename + "temp.fasta", "w", encoding="iso-8859-1") as file:
                    file.write(aligntext)

                # 步驟四(執行alignment)
                if r1_for_align == r2_for_align:
                    """if(ovelap區間的序列內容跟長度完全一樣):不用align"""
                    r1_overlap = r1_for_align
                    r2_overlap = r2_for_align
                else:  # 在py裡做shell，然後r1 r2兩個overlap去align
                    alignment = "mafft --thread 1 --localpair " + "'" + loadpath + "mafft/" + filename + "temp.fasta" + "'" + "> " + "'" + loadpath + "mafft/" + filename + "tempAlign.fasta" + "'"
                    # print(alignment)
                    try:
                        subprocess.run(alignment, shell=True, check=True, stdout=PIPE, stderr=PIPE)
                    except Exception as e:
                        print("[WARNING] error occured:", e)

                    while not path.exists(loadpath + "mafft/" + filename + "tempAlign.fasta"):
                        print("[WARNING]" + filename + "tempAlign.fasta未生成，等待一秒")
                        time.sleep(1)

                    aligned_fasta_unit = FastaUnit()
                    aligned_fasta_unit.fasta_unit(loadpath + "mafft/" + filename + "tempAlign.fasta")
                    aligned_seq_map = aligned_fasta_unit.seq_map
                    r1_overlap = ""
                    r2_overlap = ""

                    for key, value in aligned_seq_map.items():
                        if "r1" in key:
                            r1_overlap = value
                        else:
                            r2_overlap = value
            # print(aligned_seq_map) # print(r1_overlap) # print(r2_overlap)

            # # 步驟五
            # # 依alignment結果拼接重疊區塊

            merge_seq = ""
            trim_0_overlap_align = ""
            trim_1_overlap_align = ""

            # 開始判斷並拼接
            if not overlape:
                # 沒overlap就補NNNNN   # print("non-overlap",filename)# print("Ns")
                ns_num = abs(
                    r2Object.stick_site[1] - r1Object.stick_site[1])  # 原本這樣寫，有問題 ns_num=r1_p2_trimed - r2_p1_trimed-1
                ns_seq = "N" * ns_num
                merge_seq = merge_seq + r1[:r1Object.stick_site[1]].upper() + ns_seq + r2[
                                                                                       r2Object.stick_site[1]:].upper()
            elif overlape:
                # 有overlap才需要merge # print("overlap")
                overlap_seq = ""
                trim_0_overlap_align = r1_overlap
                trim_1_overlap_align = r2_overlap
                overlap_num_align = len(trim_0_overlap_align)
                gapNumInOverlap = 0
                for i in range(0, overlap_num_align):
                    overlap_seq = get_overlap_seq(trim_0_overlap_align[i], trim_1_overlap_align[i])
                    if overlap_seq == "N":
                        gapNumInOverlap += 1
                # print("overlap_num_align",overlap_num_align)
                # print("overlap_seq",overlap_seq)
                merge_seq = merge_seq + r1[:r1_p1 - 1].upper() + overlap_seq + r2[
                                                                               r2_p2 + 1:].upper()  # print(merge_seq)
                # merge_seq=merge_seq.replace("-","")

            # 步驟六：收尾  # print(merge_seq)
            output_filename = filename.replace(".fas", "")

            # (deprecated 20230611)(retained 20230624，為了方便除錯，還是留著看gap在哪)
            merge_seq_text = ">" + output_filename + "\n" + merge_seq + "\n"  # 處理mergeseq
            with open(mergepath + filename + ".fas", "w", encoding="iso-8859-1") as file:
                file.write(merge_seq_text)

            de_gap_merge_seq = merge_seq.replace("N", "").replace("-", "")  # 處理degapmergeseq
            de_gap_merge_seq_text = ">" + output_filename + "\n" + de_gap_merge_seq + "\n"
            with open(degapMergepath + filename + ".fas", "w", encoding="iso-8859-1") as file:
                file.write(de_gap_merge_seq_text)

        except Exception as unknown_exception:
            print(f"{unknown_exception.__class__.__name__}: {unknown_exception}")
            print(traceback.print_exc())
            print("[WARNING] merger.py 319: something wrong.", filename)

    print("[INFO] merger.py is ended on loci: " + sys.argv[3])


if __name__ == "__main__":
    merge()
