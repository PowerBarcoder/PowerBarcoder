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

"""
@file merger.py
@brief This script performs the merging process for the specified loci.
"""

def get_files(loadpath):
    """
    @brief Get a list of candidate files from the specified load path.
    @param loadpath: The path to load files from.
    @return: A set of candidate file names.
    """
    files = listdir(loadpath)
    candidate_list = set()

    for filename in files:
        if ("tempAlign.fasta" in filename) or ("temp.fasta" in filename):
            continue
        fullpath = join(loadpath, filename)
        if isfile(fullpath) and (filename != "temp.fasta"):
            filename_trim = str(filename)
            filename_trim = filename_trim.replace("_r1.fas", "")
            filename_trim = filename_trim.replace("_r2.fas", "")
            candidate_list.add(filename_trim)

    return candidate_list


def write_to_file(output_filename, merge_seq):
    """
    @brief Write the merged sequence to the output files (步驟六：收尾寫檔).
    @param output_filename: The name of the output file.
    @param merge_seq: The merged sequence.
    """
    mergepath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/rawMerged/"
    degap_merge_path = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/merged/"

    merge_seq_text = ">" + output_filename + "\n" + merge_seq + "\n"
    with open(mergepath + output_filename + ".fas", "w", encoding="utf-8") as file:
        file.write(merge_seq_text)

    de_gap_merge_seq = merge_seq.replace("N", "").replace("-", "")
    de_gap_merge_seq_text = ">" + output_filename + "\n" + de_gap_merge_seq + "\n"
    with open(degap_merge_path + output_filename + ".fas", "w", encoding="utf-8") as file:
        file.write(de_gap_merge_seq_text)


def get_sequence_from_map(seq_map, keyword):
    """
    @brief Get the sequence and reference sequence from the sequence map based on the keyword.
    @param seq_map: The sequence map.
    @param keyword: The keyword to search for.
    @return: A tuple containing the sequence and reference sequence.
    """
    seq = ""
    ref_seq = ""
    for key, value in seq_map.items():
        if keyword in key:
            seq = value
        else:
            ref_seq = value
    return seq, ref_seq


def merger():
    """
    @brief Perform the merging process for the specified loci.
    @exception Exception: If an error occurs during the merging process.
    """
    print("[INFO] merger.py is running on loci: " + sys.argv[3])

    ######################################
    # 運作流程
    # r1跟其align序列ref_r1比對，獲得r1_p2及其他點位資訊
    # r2跟其align序列ref_r2比對，獲得r2_p1及其他點位資訊
    # 用r1_p2及r2_p1判斷是否overlap
    # 若有overlap，將兩overlap序列做alignment後取consensus
    # 拼接r1[0:重疊區前]+overlap+r2[重疊區後:]，trim完，打印結果並存到"/home/sktang/powerBC/mergeSeq/"
    ######################################

    loadpath = sys.argv[2] + sys.argv[3] + "_result/mergeResult/merger/aligned/"
    candidate_list = get_files(loadpath)

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

            r1, ref_r1 = get_sequence_from_map(r1_seq_map, "r1")
            r2, ref_r2 = get_sequence_from_map(r2_seq_map, "r2")

            # 步驟一
            # 先建立Miseq物件，再呼叫方法獲得拼接資訊
            r1_object = Miseq()
            Miseq.stick_site_finder(r1_object, filename, r1, ref_r1, "r1")
            r2_object = Miseq()
            Miseq.stick_site_finder(r2_object, filename, r2, ref_r2, "r2")
            # print(r1_object.show()) # forword: True, stick_site(r1_p2,r2_p1): 237, F_Rtrim: deprecated_parameter, del_site: {22: 7, 234: 2}, inSite: {45: 6, 230: 3, 237: 96}
            # print(r2_object.show()) # forword: False, stick_site(r1_p2,r2_p1): 221, F_Rtrim: deprecated_parameter, del_site: {227: 2, 326: 168}, inSite: {0: 221}

            # # 步驟二
            # # 以r1_p2跟r2_p1判斷兩物件是否重疊
            overlape = False

            r1_p2 = r1_object.stick_site[1]
            r1_p2_trimed = r1_object.stick_site[1]
            r1_del_site = r1_object.del_site
            for key, value in r1_del_site.items():
                if r1_p2 > key:
                    r1_p2_trimed = r1_p2_trimed - value
            # print (r1_p2_trimed)

            r2_p1 = r2_object.stick_site[1]
            r2_p1_trimed = r2_object.stick_site[1]
            r2_del_site = r2_object.del_site
            for key, value in r2_del_site.items():
                if r2_p1 > key:
                    r2_p1_trimed = r2_p1_trimed - value
            # print(r2_p1_trimed)

            # 要減一下
            if (r1_object.forword == True) and (r2_object.forword != True):
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
            # Initialize variables with default values
            r1_overlap = ""
            r2_overlap = ""
            r1_p1 = 0
            r2_p2 = 0

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

                # 看起來要寫個檔案先存起來 (20230111這步ok)

                # 10N： r1_for_align跟r2_for_align要先degap
                # 20230206 我決定在這邊做degap(所以下一行多加了".replace("-","")")
                aligntext = ">r1\n" + r1_for_align.replace("-", "") + "\n" + ">r2\n" + r2_for_align.replace("-", "")
                with open(loadpath + "mafft/" + filename + "temp.fasta", "w", encoding="utf-8") as file:
                    file.write(aligntext)

                # 步驟四(執行alignment)
                if r1_for_align == r2_for_align:
                    # print("序列長得一模一樣，不用alignment")
                    r1_overlap = r1_for_align
                    r2_overlap = r2_for_align
                else:  # 在py裡做shell，然後r1 r2兩個overlap去align
                    alignment = "mafft --thread 10 --localpair " + "'" + loadpath + "mafft/" + filename + "temp.fasta" + "'" + "> " + "'" + loadpath + "mafft/" + filename + "tempAlign.fasta" + "'"
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

            # # 步驟五
            # # 依alignment結果拼接重疊區塊

            merge_seq = ""

            # 開始判斷並拼接
            if not overlape:
                # 沒overlap就補NNNNN   # print("non-overlap",filename)# print("Ns")
                ns_num = abs(
                    r2_object.stick_site[1] - r1_object.stick_site[1])  # 原本這樣寫，有問題 ns_num=r1_p2_trimed - r2_p1_trimed-1
                ns_seq = "N" * ns_num
                merge_seq = merge_seq + r1[:r1_object.stick_site[1]].upper() + ns_seq + r2[
                                                                                       r2_object.stick_site[1]:].upper()
            elif overlape:
                # 有overlap才需要merge # print("overlap")
                overlap_seq = ""
                trim_0_overlap_align = r1_overlap
                trim_1_overlap_align = r2_overlap
                overlap_num_align = len(trim_0_overlap_align)
                gap_num_in_overlap = 0
                for i in range(0, overlap_num_align):
                    # print(i+1,"and",j) # print(trim_0_overlap_align[i],trim_1_overlap_align[i])
                    if trim_0_overlap_align[i] == "a" and trim_1_overlap_align[i] == "a":
                        overlap_seq = overlap_seq + "A"
                    elif trim_0_overlap_align[i] == "t" and trim_1_overlap_align[i] == "t":
                        overlap_seq = overlap_seq + "T"
                    elif trim_0_overlap_align[i] == "c" and trim_1_overlap_align[i] == "c":
                        overlap_seq = overlap_seq + "C"
                    elif trim_0_overlap_align[i] == "g" and trim_1_overlap_align[i] == "g":
                        overlap_seq = overlap_seq + "G"
                    elif ((trim_0_overlap_align[i] == "a" and trim_1_overlap_align[i] == "g") or (
                            trim_0_overlap_align[i] == "g" and trim_1_overlap_align[i] == "a")):  # R	A/G
                        overlap_seq = overlap_seq + "R"
                    elif ((trim_0_overlap_align[i] == "c" and trim_1_overlap_align[i] == "t") or (
                            trim_0_overlap_align[i] == "t" and trim_1_overlap_align[i] == "c")):  # Y C/T
                        overlap_seq = overlap_seq + "Y"
                    elif ((trim_0_overlap_align[i] == "a" and trim_1_overlap_align[i] == "c") or (
                            trim_0_overlap_align[i] == "c" and trim_1_overlap_align[i] == "a")):  # M A/C
                        overlap_seq = overlap_seq + "M"
                    elif ((trim_0_overlap_align[i] == "g" and trim_1_overlap_align[i] == "t") or (
                            trim_0_overlap_align[i] == "t" and trim_1_overlap_align[i] == "g")):  # K G/T
                        overlap_seq = overlap_seq + "K"
                    elif ((trim_0_overlap_align[i] == "g" and trim_1_overlap_align[i] == "c") or (
                            trim_0_overlap_align[i] == "c" and trim_1_overlap_align[i] == "g")):  # S G/C
                        overlap_seq = overlap_seq + "S"
                    elif ((trim_0_overlap_align[i] == "a" and trim_1_overlap_align[i] == "t") or (
                            trim_0_overlap_align[i] == "t" and trim_1_overlap_align[i] == "a")):  # W A/T
                        overlap_seq = overlap_seq + "W"
                    elif (trim_0_overlap_align[i] == "-") and (trim_1_overlap_align[i] == "-"):  # gap+gap=N
                        overlap_seq = overlap_seq + "N"
                        gap_num_in_overlap += 1
                    elif trim_0_overlap_align[i] == "-" and trim_1_overlap_align[i] != "-":
                        # gap+ATCG=atcg
                        overlap_seq = overlap_seq + trim_1_overlap_align[i]
                    elif trim_0_overlap_align[i] != "-" and trim_1_overlap_align[i] == "-":
                        # ATCG+gap=atcg
                        overlap_seq = overlap_seq + trim_0_overlap_align[i]  # TODO 研究一下小寫的原因
                    # D G/A/T # V G/A/C # B G/T/C # H A/T/C 兩條序列不會出現
                    else:
                        print("[ERROR] 出錯了GG")
                # print("overlap_num_align",overlap_num_align)
                # print("overlap_seq",overlap_seq)
                merge_seq = merge_seq + r1[:r1_p1 - 1].upper() + overlap_seq + r2[
                                                                               r2_p2 + 1:].upper()  # print(merge_seq)
                # merge_seq=merge_seq.replace("-","")

            # 步驟六：收尾寫檔
            output_filename = filename.replace(".fas", "")
            write_to_file(output_filename, merge_seq)


        except Exception as unknown_exception:
            print(f"{unknown_exception.__class__.__name__}: {unknown_exception}")
            print(traceback.print_exc())
            print("[WARNING] merger.py 319: something wrong.", filename)

    print("[INFO] merger.py is ended on loci: " + sys.argv[3])


if __name__ == "__main__":
    merger() # python3 merger.py '/PowerBarcoder/data/amplicon_data/' '/PowerBarcoder/data/result/202402021655/' 'trnLF'

# # # # 之前的假資料
# # # 全部做完試trnL-F
# # # trim
# # ------------------------------第二組例子(複雜度提高，重疊區域有indel)----------------------------------
# #                                                                                                                                                                                                                                    overlap*********overlap
# r1 =     "AAGCTGGTGTTAAAGATTATCGATTGACCTATTACACTCCCGAAT------CTAAAGACACTGATATCTTAGCAGCCTCCCGCATGACCCCACAACCCGGAGTACCTGCCGAGGAAGCAGGAGCTGCGGTAGCTGCGGAATCCTCAGATGGACTTACCAGTCTCGATCGGTACAAGGGCCGATGCTACGATATCGAACCCGTCGCTGGAGAGGAAAACCAGTATATTGCA---GTAG------------------------------------------------------------------------------------------------"
# ref_r1 = "AAGCTGGTGTTAAAGATTATCG-------TATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATG--GCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC"
# #                             *del 22,7              *in 45,6                                                                                                                                                                                *in 230,3  *del 234,2  *in 237,96
# #                                                                                                                                                                                                                                           VVVVVVVVV   (對r1來說，需取9-3個)

# ref_ori = "AAGCTGGTGTTAAAGATTATCGTATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATGGCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC"
# #                                                                                                                                                                                                                                     VVVVVVV (222-228)

# r2 =     "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------CCCCCCCCCCTTATCCCCTGGATCTATTCGAGGAAGGTTCCGTTACTAATTTGTTCACTTCCATTGTAGGTAATGTTTTCGGATTTAAGGCCCTACGCGCTTTACGCCTAGAAGACCTTCGAATTCCCCCTGCCTATTCCAAAACTTTCATTGGACCACCTCATGGTATTCAGGTCGAAAGAGACAAACTGAACAAATATGGACGTCCTTTATTGGGATGTACAATCAAGCCAAAATTGGGCTTGTCCGCTAAGAATTATGGTAGAGCTGTCT"
# ref_r2 = "AAGCTGGTGTTAAAGATTATCGTATTACACTCCCGAATATAAGACCAAAGACACTGATATCTTAGCAGCCTTCCGAATGACCCCACAACCCGGAGTACCGGCTGAGGAAGCCGGAGCTGCAGTAGCTGCGGAATCCTCAGACGGGCTTACCAGTCTCGATCGCTACAAGGGCCGGTGCTACGATATCGAACCCGTTGCTGGGGAAGAAAACCAGTATATCGCATATG--GCTTATCCCTTGGATCTATTTGAAGAAGGTTCTGTAACCAATCTGTTCACTTCAATTGTAGGTAATGTTTTCGGATTCAAGGCCCTACGCGCTCTAC------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# #              *in 0,221                                                                                                                                                                                                                         *del 227: 2                                                                                         *del 326,168
# #                                                                                                                                                                                                                                      VVVVVVVVV   (對r2來說，因為沒有del，所以取9個)
