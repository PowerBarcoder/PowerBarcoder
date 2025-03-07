# -*- coding: utf-8 -*-

"""
@file alignmentPretreater.py
@brief Prepare r1Ref & r2Ref for alignment.
"""

import sys
import traceback

POSITIVE_DIRECTION = "positive"
NEGATIVE_DIRECTION = "negative"


def qseqid_file(target_output_loadpath, r_who, file_name):
    """
    Generate the path for the target sequence file.

    :param target_output_loadpath: The base path for the output.
    :type target_output_loadpath: str
    :param r_who: The direction of the sequence (r1, r2, or rWho).
    :type r_who: str
    :param file_name: The name of the file.
    :type file_name: str
    :return: The full path of the target sequence file.
    :rtype: str
    """
    target_qseqid_file_dir = target_output_loadpath + r_who + "/"
    target_qseqid_file_name = file_name
    target_qseqid_file = target_qseqid_file_dir + target_qseqid_file_name
    return target_qseqid_file


def negative_test(a, b):
    """
    Determine the direction based on the given values.

    :param a: The first value.
    :type a: tuple
    :param b: The second value.
    :type b: tuple
    :return: The direction (positive or negative).
    :rtype: str
    """
    if ((a[0] == "-") and (b[0] == "-")) or ((a[0] != "-") and (b[0] != "-")):
        return POSITIVE_DIRECTION
    elif ((a[0] != "-") and (b[0] == "-")) or ((a[0] == "-") and (b[0] != "-")):
        return NEGATIVE_DIRECTION


def reverse_complement(seq):
    """
    Return the reverse complement of the given sequence, ignoring gaps.

    :param seq: The input sequence.
    :type seq: str
    :return: The reverse complement of the sequence.
    :rtype: str
    """
    seq = seq.replace(' ', '')  # Remove space
    seq = seq.replace('\n', '')  # Remove LF
    seq = seq[::-1]  # Reverse the sequence
    basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N', 'R': 'Y', 'Y': 'R', 'M': 'K', 'K': 'M',
                      'S': 'S', 'W': 'W', 'H': 'D', 'B': 'V'}  # Make a dictionary for complement
    letters = list(seq)  # Turn the sequence into a list
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters) + '\n'  # Turn the list into a string


def create_ref_file(r_who, r_who_row_list):
    """
    Write two sequences into a single file.

    :param r_who: The direction of the sequence (r1, r2, or rWho).
    :type r_who: str
    :param r_who_row_list: The list of rows for the sequence.
    :type r_who_row_list: list
    """
    with open(output_loadpath + r_who + "Ref/" + qseqid, "w") as ref_file:
        final_row_list = r_who_row_list + target_row_list
        ref_file.writelines(final_row_list)


print("[INFO] alignmentPretreater.py is running on loci: " + sys.argv[4])

# loadpath="/home/sktang/powerBC/"
local_blast_loadpath = sys.argv[3]
output_loadpath = sys.argv[3] + sys.argv[4] + "_result/mergeResult/merger/"

# localblast完的序列檔案
fasta_file_dir = local_blast_loadpath + sys.argv[4] + "_result/blastResult/"
fasta_file_name = sys.argv[4] + "_blastResult.txt"
fasta_file = fasta_file_dir + fasta_file_name

# ref
# sseqid_file_dir="/home/lykuo/lab_data/NGS_data/miseq/LIB810_S9/"
sseqid_file_dir = sys.argv[1]
# sseqid_file_name="fermalies_rbcL.fasta"
sseqid_file_name = sys.argv[2]

sseqid_file = sseqid_file_dir + sseqid_file_name

r1_row_list = []
r2_row_list = []
target_row_list = []

try:
    with open(fasta_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if not line.strip():
                break
            line = line.replace("\n", "")
            line_split = line.split("\t")
            qseqid = line_split[0]
            sseqid = line_split[1]
            sign = negative_test(line_split[12], line_split[13])
            forward = line_split[14]

            # 已獲得所有資訊，開始分四狀況來寫alignment了
            # 0514-016_CYH20090514-016_Microlepia_substrigosa_.fas
            # MH319942_Dennstaedtiaceae_Histiopteris_incisa
            # positive
            # r1
            try:
                # r1r2分開blast
                qseqid_file_str = qseqid_file(output_loadpath, forward, qseqid)
                if forward == "r1":
                    r1_row_list = []
                    with open(qseqid_file_str, "r") as q_r1_file:
                        lines = q_r1_file.readlines()
                        r1_row_list += lines
                elif forward == "r2":
                    r2_row_list = []
                    with open(qseqid_file_str, "r") as q_r2_file:
                        lines = q_r2_file.readlines()
                        r2_row_list += lines
                # r1r2 cat起來blast
                elif forward == "rWho":
                    # 待測序列r1製作
                    qseqid_file_str = qseqid_file(output_loadpath, "r1", qseqid.replace(".fas", "_r1.fas"))
                    r1_row_list = []
                    with open(qseqid_file_str, "r") as q_r1_file:
                        lines = q_r1_file.readlines()
                        r1_row_list += lines

                    # 待測序列r2製作
                    qseqid_file_str = qseqid_file(output_loadpath, "r2", qseqid.replace(".fas", "_r2.fas"))
                    r2_row_list = []
                    with open(qseqid_file_str, "r") as q_r2_file:
                        lines = q_r2_file.readlines()
                        r2_row_list += lines
                else:
                    print("forward error in alignmentPretreater.py 118: " + qseqid_file_str)

            except Exception as e:
                print("[ERROR] An exception happen in " + sys.argv[4] + "： " + qseqid + " before alignment")
                print(traceback.print_exc())
                continue

            # ref seq製作
            target_row_list = []
            target_row_number = int(-1)
            with open(sseqid_file, "r") as s_file:
                lines = s_file.readlines()
                for target_line in lines:
                    target_row_number += 1
                    if target_line.find(sseqid) != -1:
                        break
                target_row_list += (lines[target_row_number:target_row_number + 2])

            # if else判斷方向(多行的fasta之後再處理成一行的)

            # 2022年舊版
            # if ((sign=="negative")and(forward=="r1")):
            #     target_row_list[1]=reverse_complement(target_row_list[1])
            #     r2_row_list[1]=reverse_complement(r2_row_list[1])
            # elif ((sign=="positive")and(forward=="r1")):
            #     r2_row_list[1]=reverse_complement(r2_row_list[1])
            # elif ((sign=="negative")and(forward=="r2")):
            #     r2_row_list[1]=reverse_complement(r2_row_list[1])
            # elif ((sign=="positive")and(forward=="r2")):
            #     target_row_list[1]=reverse_complement(target_row_list[1])
            #     r2_row_list[1]=reverse_complement(r2_row_list[1])

            # 20230206-10N新版 TODO 需要用trnLF測試正確性            
            if sign == NEGATIVE_DIRECTION:
                target_row_list[1] = reverse_complement(target_row_list[1])
            elif sign == POSITIVE_DIRECTION:
                pass

            # # r1r2分開blast
            if forward == "r1":
                create_ref_file("r1", r1_row_list)
            elif forward == "r2":
                create_ref_file("r2", r2_row_list)
            # # r1r2 cat起來blast
            elif forward == "rWho":
                create_ref_file("r1", r1_row_list)
                create_ref_file("r2", r2_row_list)
            else:
                print("forward error in alignmentPretreater.py 183: " + qseqid_file_str)

except Exception as e:
    print("[ERROR] An exception happen in " + sys.argv[4] + " before alignment")
    print(traceback.print_exc())

print("[INFO] alignmentPretreater.py is ended on loci: " + sys.argv[4])

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


# 20230214
# 判讀方向從4整情況改為2種情況，
# 因為r1跟r2已經是定向了，
# 所以只需要在sign=="negative"時，把ref反轉即可
