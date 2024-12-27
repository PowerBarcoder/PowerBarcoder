"""
This script calls the BlastRef object to parse the results of 00_blastForRef ({loci}_refResult.txt)
into blastResult.txt. After that, it executes the methods below.
"""

import sys
import os
from main.merge.BlastRef import BlastRef
from main.merge.blastRefFilter import blast_ref_filter


def main():
    """
    Main function to execute the blast result parsing and filtering process.
    """
    amplicon_info = sys.argv[1]
    result_data_path = sys.argv[2]
    blast_parsing_mode = sys.argv[3]
    name_of_loci = sys.argv[4]

    print("[INFO] blastResultParser.py is running on loci: " + name_of_loci)

    # 先執行blastRefFilter.py，篩選出需要的序列
    blast_ref_filter(result_data_path, name_of_loci, blast_parsing_mode)

    # 再執行parsing作業，這部分在20231202新增blastRefFilter.py後，雖有重工，但其產出檔案會給後續的qc使用，所以直接保留
    local_blast = BlastRef()
    local_blast.blast_ref(result_data_path, name_of_loci, blast_parsing_mode)

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
        Constructs a tab-separated string of blast result details for a given index.
        
        Args:
            list_index (int): The index of the blast result.

        Returns:
            str: A tab-separated string of blast result details.
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
