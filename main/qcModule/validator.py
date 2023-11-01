import os
from Bio import Align
from Bio import Seq
from Bio import SeqIO
import sys

# BASE_URL = 'C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738_test/trnLF_result/'
BASE_URL = sys.argv[1] + sys.argv[2] + "_result/"
input_r1_path = f'{BASE_URL}denoiseResult/r1/'
input_r2_path = f'{BASE_URL}denoiseResult/r2/'
input_ref_path = f'{BASE_URL}mergeResult/merger/r1Ref/'
input_dada2_path = f'{BASE_URL}mergeResult/dada2/merged/'
input_merger_path = f'{BASE_URL}mergeResult/merger/merged/'
output_denoise_path = f'{BASE_URL}qcResult/validator/denoise/'
output_merge_path = f'{BASE_URL}qcResult/validator/merge/'
output_all_path = f'{BASE_URL}qcResult/validator/all/'


def reverse_complement_pairwise_alignment(query_seq: str, target_seq: str):
    # print(f'query_seq: {query_seq.seq}')
    # print(f'target_seq: {target_seq.seq}')

    # Perform sequence alignment
    aligner = Align.PairwiseAligner(scoring="blastn")  # 直接用blastn的，方便

    # forward_alignment
    forward_alignment = aligner.align(query_seq, target_seq)
    forward_alignment_query_sequence = (forward_alignment[0].format("fasta")).splitlines()[1]
    # print(f'forward_alignment_query_sequence: {forward_alignment_query_sequence}')
    forward_score = longest_ATCG_sequence(forward_alignment_query_sequence)

    # reverse_complement_alignment
    reverse_complement_alignment = aligner.align(str(Seq.Seq(query_seq).reverse_complement()), target_seq)
    reverse_complement_alignment_query_sequence = (reverse_complement_alignment[0].format("fasta")).splitlines()[1]
    # print(f'reverse_complement_alignment_query_sequence: {reverse_complement_alignment_query_sequence}')
    reverse_complement_score = longest_ATCG_sequence(reverse_complement_alignment_query_sequence)

    # Determine which alignment has a higher score
    if forward_score >= reverse_complement_score:
        alignment_score = forward_score
        alignment_sequence = query_seq
    else:
        alignment_score = reverse_complement_score
        alignment_sequence = str(Seq.Seq(query_seq).reverse_complement())

    # print(f'isReversed: {reverse_complement_score > forward_score}, '
    #       f'forward_score: {forward_score}, '
    #       f'reverse_complement_score: {reverse_complement_score}')
    # print(f'alignment_sequence: {alignment_sequence}')

    return alignment_sequence


def longest_ATCG_sequence(sequence: str):
    longest_length = 0
    current_length = 0
    for char in sequence:
        if char in ['A', 'T', 'C', 'G']:
            current_length += 1
        else:
            current_length = 0
        if current_length > longest_length:
            longest_length = current_length
    return longest_length


def concatenate_files_from_one_folder(folder_path, output_file):
    with open(output_file, 'w') as output:
        for filename in os.listdir(folder_path):
            if filename.endswith('.fas'):  # Change the extension to match the files you want to concatenate
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    output.write(file.read())


def concatenate_files_from_two_files(folder_file1, folder_file2, output_file):
    with open(output_file, 'w') as output:
        if os.path.exists(folder_file1):
            with open(folder_file1, 'r') as file1:
                output.write(file1.read())
        if os.path.exists(folder_file2):
            with open(folder_file2, 'r') as file2:
                output.write(file2.read())


def denoise_alignment():
    """
    align dada2 denoise後的abundance最高的r1,r2
    """

    alignment_file_list = os.listdir(input_r1_path)
    merger_file_list = os.listdir(input_ref_path)

    for alignment_sample_name in alignment_file_list:
        print(f'denoise_alignment: {alignment_sample_name}')
        merger_file_name = ""
        for merger_sample_name in merger_file_list:
            if alignment_sample_name.replace('.fas', '') in merger_sample_name:
                merger_file_name = merger_sample_name
                break

        # Leave the file that can't find the corresponding merger file
        if merger_file_name == "":
            continue

        # Read the input r1 r2 files # 這裡的r1跟r2是abundance最高的那條
        r1SeqRecord = next(SeqIO.parse(input_r1_path + alignment_sample_name, "fasta"))
        r2SeqRecord = next(SeqIO.parse(input_r2_path + alignment_sample_name, "fasta"))

        # Read Ref file
        records = SeqIO.parse(input_ref_path + merger_file_name, "fasta")
        for _ in range(1):  # Skip the first two records
            next(records)
        ref1SeqRecord = next(records)

        # Check and do Reverse complement the r1 and r2 sequences
        r1SeqRecord.seq = reverse_complement_pairwise_alignment(str(r1SeqRecord.seq), str(ref1SeqRecord.seq))
        r2SeqRecord.seq = reverse_complement_pairwise_alignment(str(r2SeqRecord.seq), str(ref1SeqRecord.seq))

        # print(f'r1Fasta: {r1SeqRecord.seq}')
        # print(f'r2Fasta: {r2SeqRecord.seq}')

        # Perform sequence alignment
        aligner2 = Align.PairwiseAligner(scoring="blastn")  # 直接用blastn的，方便
        alignment = aligner2.align(r1SeqRecord.seq, r2SeqRecord.seq)
        # Access the aligned sequences
        aligned_r1 = (alignment[0].format("fasta")).splitlines()[1]
        aligned_r2 = (alignment[0].format("fasta")).splitlines()[3]

        # print(f'aligned_r1: {aligned_r1}')
        # print(f'aligned_r2: {aligned_r2}')

        # # Write the alignment to a file
        output_file = output_denoise_path + alignment_sample_name
        with open(output_file, "w") as handle:
            handle.write(f">dada2 r1 best ASV: {r1SeqRecord.id}\n")
            handle.write(aligned_r1 + "\n")
            handle.write(f">dada2 r2 best ASV: {r2SeqRecord.id}\n")
            handle.write(aligned_r2 + "\n")


def merger_alignment():
    """
    align merger跟dada2的result
    如果ASV分別有5&6，那會有30種alignment結果，這裡只從中挑選成績最好的一組
    成績好壞：兩序列中，最高連續ATCG片段最長的作為該序列代表，跟align對象互比，找到較短的一方做為整組代表
    預設情境：兩序列若很不相似，則單次alignment中，會有一端出現gap很多，意味著該序列跟對象不相似，因此被選為代表後，會比不過其他組alignment
    """

    dada2_file_list = os.listdir(input_dada2_path)
    merger_file_list = os.listdir(input_merger_path)

    for dada2_file_name in dada2_file_list:
        '''
        merger的結果都已經拆分成單獨檔案
            # Alsophila_sp._Wade4916_KTHU1767_01_0.968_abundance_1574.fas    
        dada2的結果都是一個fasta裡有很多序列
            # Alsophila_sp._Wade4916_KTHU1767_.fas
        '''
        print(f'merger_alignment: {dada2_file_name}')
        best_aligned_dada2_seq_list = []
        best_aligned_merger_seq_list = []
        best_aligned_dada2_header_list = []
        best_aligned_merger_header_list = []

        # Read the input dada2 file
        dada2_records = SeqIO.parse(input_dada2_path + dada2_file_name, "fasta")
        dada2_record_list = []
        for record in dada2_records:
            dada2_record_list.append(record)

        # Read the input merger file
        merger_record_list = []
        for merger_file_name in merger_file_list:
            if dada2_file_name.replace('.fas', '') in merger_file_name:
                # Read the input merger file
                merger_records = SeqIO.parse(input_merger_path + merger_file_name, "fasta")
                for record in merger_records:
                    merger_record_list.append(record)

        # print(f'dada2_record_list: {dada2_record_list}')
        # print(f'merger_record_list: {merger_record_list}')

        # Do pairwise alignment between dada2 and merger
        for merger_record in merger_record_list:  # 如：merger有7筆ASV
            """
            10Ncat不須考慮overlap，
            所以下游的merger merge的ASV數量一定大於等於dada2 merge的ASV數量，
            故此處採用以merger merge的ASV為基準，對dada2 merge的ASV做alignment 
            如：7*5而非5*7，outputAll的結果會有7個pairwise alignment的結果          
            """
            best_score = 0
            best_aligned_dada2_seq = ""
            best_aligned_merger_seq = ""
            best_aligned_dada2_header = ""
            best_aligned_merger_header = ""
            for dada2_record in dada2_record_list:  # 如：dada2有5筆ASV
                # Pretreatment for uppercase sequence
                merger_record.seq = merger_record.seq.upper()
                # Perform sequence alignment
                aligner = Align.PairwiseAligner(scoring="blastn")
                alignment = aligner.align(dada2_record.seq, merger_record.seq)
                # Access the aligned sequences
                aligned_dada2 = (alignment[0].format("fasta")).splitlines()[1]
                aligned_merger = (alignment[0].format("fasta")).splitlines()[3]
                # Count the longest ATCG subsequence
                dada2_score = longest_ATCG_sequence(aligned_dada2)
                merger_score = longest_ATCG_sequence(aligned_merger)
                pairwise_score = min(dada2_score, merger_score)
                # print(f'pairwise_score: {pairwise_score}; dada2: {dada2_score}, merger: {merger_score}')
                # Determine which alignment has a higher score
                if pairwise_score > best_score:
                    best_score = pairwise_score
                    best_aligned_dada2_seq = aligned_dada2
                    best_aligned_merger_seq = aligned_merger
                    best_aligned_dada2_header = dada2_record.id
                    best_aligned_merger_header = merger_record.id
            best_aligned_dada2_header_list.append(best_aligned_dada2_header)
            best_aligned_merger_header_list.append(best_aligned_merger_header)
            best_aligned_dada2_seq_list.append(best_aligned_dada2_seq)
            best_aligned_merger_seq_list.append(best_aligned_merger_seq)
            # print(f'best_score: {best_score};')
            # print(f'best_aligned_dada2: {best_aligned_dada2_header};')
            # print(f'best_aligned_merger: {best_aligned_merger_header};')

            # # Write the alignment to a file
        output_file = f'{output_merge_path}{dada2_file_name}'
        with open(output_file, "w") as handle:
            for i in range(len(best_aligned_dada2_seq_list)):
                handle.write(f">merger merge: {best_aligned_merger_header_list[i]}\n")
                handle.write(best_aligned_merger_seq_list[i] + "\n")
                handle.write(f">dada2 merge: {best_aligned_dada2_header_list[i]}\n")
                handle.write(best_aligned_dada2_seq_list[i] + "\n")


def concate_denoise_and_merger():
    output_denoise_file_list = os.listdir(output_denoise_path)
    for i in range(len(output_denoise_file_list)):
        filename = output_denoise_file_list[i]
        concatenate_files_from_two_files(output_denoise_path + filename,
                                         output_merge_path + filename,
                                         output_all_path + filename)


def main():
    denoise_alignment()
    merger_alignment()
    concate_denoise_and_merger()


if __name__ == '__main__':
    print(f"[INFO] Start to validate in {sys.argv[2]}!")
    main()
    print(f"[INFO] End of validation in {sys.argv[2]}!")
