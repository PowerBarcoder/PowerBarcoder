"""
@file blastResultParser.py
@brief This script calls primary_blast_ref_filter and secondary_blast_ref_filter to parse the results of 00_blastForRef.
step as follows:
1. {loci}_refResult.txt -> primary_blast_ref_filter filter 1 -> {loci}_refResult_intersection.txt
2. {loci}_refResult_intersection.txt -> primary_blast_ref_filter filter 2~4 -> {loci}_refResult_filtered.txt
3. {loci}_refResult_filtered.txt -> secondary_blast_ref_filter -> {loci}_blastResult.txt
"""

import sys
import os
from main.merge.blast.secondary_blast_ref_filter import BlastRef
from main.merge.blast.primary_blast_ref_filter import primary_blast_ref_filter


def main():
    """
    @brief Main function to execute the blast result parsing and filtering process.
    @param amplicon_info: The path to the amplicon information.
    @param result_data_path: The path to the result data.
    @param blast_parsing_mode: The mode for parsing the BLAST results.
    @param name_of_loci: The name of the loci.
    @return: None
    @exception Exception: If an error occurs during the process.
    """
    amplicon_info = sys.argv[1]
    result_data_path = sys.argv[2]
    blast_parsing_mode = sys.argv[3]
    name_of_loci = sys.argv[4]

    print("[INFO] blastResultParser.py is running on loci: " + name_of_loci)

    # 先執行primary_blast_ref_filter.py，篩選出需要的序列
    primary_blast_ref_filter(result_data_path, name_of_loci, blast_parsing_mode)

    # 再執行parsing作業，這部分在20231202新增primary_blast_ref_filter.py後，雖有重工，但其產出檔案會給後續的qc使用，所以直接保留
    local_blast = BlastRef()
    local_blast.secondary_blast_ref_filter(result_data_path, name_of_loci, blast_parsing_mode)

    # Retrieve lists from the BlastRef object
    qseqid_list = local_blast.qseqid_list
    sseqid_list = local_blast.sseqid_list
    pident_list = local_blast.pident_list
    length_list = local_blast.length_list
    mismatch_list = local_blast.mismatch_list
    gapopen_list = local_blast.gapopen_list
    qstart_list = local_blast.qstart_list
    qend_list = local_blast.qend_list
    sstart_list = local_blast.sstart_list
    send_list = local_blast.send_list
    evalue_list = local_blast.evalue_list
    bitscore_list = local_blast.bitscore_list
    qstart_minus_qend_list = local_blast.qstart_minus_qend_list
    sstart_minus_send_list = local_blast.sstart_minus_send_list
    rwho_list = local_blast.rwho_list

    def determine_direction(list_index: int) -> str:
        """
        @brief Constructs a tab-separated string of blast result details for a given index.
        @param list_index: The index of the blast result.
        @return: A tab-separated string of blast result details.
        """
        return '\t'.join([
            str(qseqid_list[list_index]), str(sseqid_list[list_index]), str(pident_list[list_index]),
            str(length_list[list_index]), str(mismatch_list[list_index]), str(gapopen_list[list_index]),
            str(qstart_list[list_index]), str(qend_list[list_index]), str(sstart_list[list_index]),
            str(send_list[list_index]), str(evalue_list[list_index]), str(bitscore_list[list_index])[:-2],
            str(qstart_minus_qend_list[list_index]), str(sstart_minus_send_list[list_index]),
            str(rwho_list[list_index])
        ])

    output_file_path = os.path.join(result_data_path,
                                    f"{name_of_loci}_result/blastResult/{name_of_loci}_blastResult.txt")
    with open(output_file_path, "w") as file:
        for i in range(len(qseqid_list)):
            if "\t\t0\t0\t0\t0\t0\t0\t0\t0\t\t\t0\t0\t" not in determine_direction(i):
                file.write(determine_direction(i) + "\n")

    print("[INFO] blastResultParser.py is ended on loci: " + name_of_loci)


if __name__ == '__main__':
    main()
