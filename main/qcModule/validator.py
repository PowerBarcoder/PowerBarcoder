import os
from Bio import Align, Seq, SeqIO
import sys

BASE_URL = sys.argv[1] + sys.argv[2] + "_result/"
input_r1_path = f'{BASE_URL}denoiseResult/r1/'
input_r2_path = f'{BASE_URL}denoiseResult/r2/'
input_ref_path = f'{BASE_URL}mergeResult/merger/r1Ref/'
input_dada2_path = f'{BASE_URL}mergeResult/dada2/merged/'
input_merger_path = f'{BASE_URL}mergeResult/merger/merged/'
output_denoise_path = f'{BASE_URL}qcResult/validator/denoise/'
output_merge_path = f'{BASE_URL}qcResult/validator/merge/'
output_all_path = f'{BASE_URL}qcResult/validator/all/'
output_best_path = f'{BASE_URL}qcResult/validator/best/'


def reverse_complement_pairwise_alignment(query_seq: str, target_seq: str):
    """
    Performs pairwise alignment between query_seq and target_seq.
    Returns the sequence with the longest ATCG subsequence.

    :param query_seq: Query sequence to align.
    :param target_seq: Target sequence to align against.
    :return: Alignment sequence with the longest ATCG subsequence.
    """
    aligner = Align.PairwiseAligner(scoring="blastn")

    forward_alignment = aligner.align(query_seq, target_seq)
    forward_alignment_query_sequence = (forward_alignment[0].format("fasta")).splitlines()[1]
    forward_score = longest_atcg_sequence(forward_alignment_query_sequence)

    reverse_complement_alignment = aligner.align(str(Seq.Seq(query_seq).reverse_complement()), target_seq)
    reverse_complement_alignment_query_sequence = (reverse_complement_alignment[0].format("fasta")).splitlines()[1]
    reverse_complement_score = longest_atcg_sequence(reverse_complement_alignment_query_sequence)

    if forward_score >= reverse_complement_score:
        alignment_sequence = query_seq
    else:
        alignment_sequence = str(Seq.Seq(query_seq).reverse_complement())

    return alignment_sequence


def longest_atcg_sequence(sequence: str):
    """
    Returns the length of the longest consecutive ATCG subsequence in the given sequence.

    :param sequence: Input sequence.
    :return: Length of the longest consecutive ATCG subsequence.
    """
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
    """
    Concatenates files from a single folder into a single output file.

    :param folder_path: Path to the folder containing files to concatenate.
    :param output_file: Output file to store the concatenated content.
    """
    with open(output_file, 'w') as output:
        for filename in os.listdir(folder_path):
            if filename.endswith('.fas'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    output.write(file.read())


def concatenate_files_from_two_files(folder_file1, folder_file2, output_file):
    """
    Concatenates content from two files into a single output file.

    :param folder_file1: Path to the first file.
    :param folder_file2: Path to the second file.
    :param output_file: Output file to store the concatenated content.
    """
    with open(output_file, 'w') as output:
        if os.path.exists(folder_file1):
            with open(folder_file1, 'r') as file1:
                output.write(file1.read())
        if os.path.exists(folder_file2):
            with open(folder_file2, 'r') as file2:
                output.write(file2.read())


def concatenate_files_from_multiple_files(file_paths, output_file):
    """
    Concatenates content from multiple files into a single output file.

    :param file_paths: List of paths to input files.
    :param output_file: Output file to store the concatenated content.
    """
    with open(output_file, 'w') as output:
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    output.write(file.read())
            else:
                print(f'[WARNING] {file_path} does not exist!')


def denoise_alignment():
    """
    Aligns the dada2 denoise output sequences and writes the results to files.
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

        # Read the input r1 r2 files # 這裡的r1跟r2是abundance最高的那條
        r1_seq_record = next(SeqIO.parse(input_r1_path + alignment_sample_name, "fasta"))
        r2_seq_record = next(SeqIO.parse(input_r2_path + alignment_sample_name, "fasta"))

        # if merger的ref存在，我們就檢查r1 r2方向有沒有正確，沒有ref就算了
        if merger_file_name != "":
            records = SeqIO.parse(input_ref_path + merger_file_name, "fasta")
            for _ in range(1):
                next(records)
            ref1_seq_record = next(records)

            # Check and do Reverse complement the r1 and r2 sequences
            r1_seq_record.seq = reverse_complement_pairwise_alignment(
                str(r1_seq_record.seq), str(ref1_seq_record.seq)
            )
            r2_seq_record.seq = reverse_complement_pairwise_alignment(
                str(r2_seq_record.seq), str(ref1_seq_record.seq)
            )

        # Perform sequence alignment
        aligner2 = Align.PairwiseAligner(scoring="blastn")  # 直接用blastn的，方便
        alignment = aligner2.align(r1_seq_record.seq, r2_seq_record.seq)
        aligned_r1 = (alignment[0].format("fasta")).splitlines()[1]
        aligned_r2 = (alignment[0].format("fasta")).splitlines()[3]

        output_file = output_denoise_path + alignment_sample_name
        with open(output_file, "w") as handle:
            handle.write(f">dada2 r1 best ASV: {r1_seq_record.id}\n")
            handle.write(aligned_r1 + "\n")
            handle.write(f">dada2 r2 best ASV: {r2_seq_record.id}\n")
            handle.write(aligned_r2 + "\n")


def merger_alignment():
    """
    Aligns the merger and dada2 result sequences and writes the results to files.
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
        dada2_record_list = [record for record in dada2_records]

        # Read the input merger file
        merger_record_list = []
        for merger_file_name in merger_file_list:
            if dada2_file_name.replace('.fas', '') in merger_file_name:
                merger_records = SeqIO.parse(input_merger_path + merger_file_name, "fasta")
                merger_record_list.extend(list(merger_records))

        for merger_record in merger_record_list:
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
            for dada2_record in dada2_record_list:
                merger_record.seq = merger_record.seq.upper()
                aligner = Align.PairwiseAligner(scoring="blastn")
                alignment = aligner.align(dada2_record.seq, merger_record.seq)
                aligned_dada2 = (alignment[0].format("fasta")).splitlines()[1]
                aligned_merger = (alignment[0].format("fasta")).splitlines()[3]
                dada2_score = longest_atcg_sequence(aligned_dada2)
                merger_score = longest_atcg_sequence(aligned_merger)
                pairwise_score = min(dada2_score, merger_score)

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

        output_file = f'{output_merge_path}{dada2_file_name}'
        with open(output_file, "w") as handle:
            for i in range(len(best_aligned_dada2_seq_list)):
                handle.write(f">merger merge: {best_aligned_merger_header_list[i]}\n")
                handle.write(best_aligned_merger_seq_list[i] + "\n")
                handle.write(f">dada2 merge: {best_aligned_dada2_header_list[i]}\n")
                handle.write(best_aligned_dada2_seq_list[i] + "\n")


def concatenate_denoise_and_merger():
    """
    Concatenates denoise and merger results into a single output file.
    """
    output_denoise_file_list = os.listdir(output_denoise_path)
    for i in range(len(output_denoise_file_list)):
        filename = output_denoise_file_list[i]

        file_paths = [output_denoise_path + filename, output_merge_path + filename]
        merge_align_path = f'{BASE_URL}mergeResult/merger/aligned/'
        merger_align_file_list = os.listdir(merge_align_path)

        for merger_align_file_name in merger_align_file_list:
            if filename.replace('.fas', '') in merger_align_file_name and 'r1' in merger_align_file_name:
                file_paths.append(merge_align_path + merger_align_file_name)
            if filename.replace('.fas', '') in merger_align_file_name and 'r2' in merger_align_file_name:
                file_paths.append(merge_align_path + merger_align_file_name)

        concatenate_files_from_multiple_files(file_paths, output_all_path + filename)


def extract_best_denoise_and_merger():
    """
    We check the file in /mergeResult/dada2/merged/ and /mergeResult/merger/merged/ directory.
    Extract the best denoise or merger results into the directory.
    If dada2 merged file exists, we extract the first occurrence of the line (header) and its next line (seq.).
    If merger merged file exists, we also extract the first occurrence of the line (header) and its next line (seq.).
    If both dada2 merged file and merger merged file exist, we only choose the dada2 merged sequence.
    If only merger merged file exists, we choose the merger merge sequence.
    If both does not exist, we do not extract the content.
    :return:
    """

    input_dada2_file_list = os.listdir(input_dada2_path)
    for filename in input_dada2_file_list:
        with open(input_dada2_path + filename, 'r') as file:
            lines = file.readlines()
            dada2_merge_content = [lines[0], lines[1]]
        with open(output_best_path + filename, 'w') as new_file:
            print(f'[INFO] extract_best_dada2: {filename}')
            new_file.write(dada2_merge_content[0].replace(">",">dada2 merged: "))
            new_file.write(dada2_merge_content[1])

    output_best_file_list = set(os.listdir(output_best_path))
    input_merger_file_list = os.listdir(input_merger_path)
    for filename in input_merger_file_list:
        with open(input_merger_path + filename, 'r') as file:
            lines = file.readlines()
            merger_merge_content = [lines[0], lines[1]]
        trimmed_filename = "_".join(filename.split("_")[:-4]) + "_.fas"
        if trimmed_filename not in output_best_file_list:
            with open(output_best_path + trimmed_filename, 'w') as new_file:
                print(f'[INFO] extract_best_merger: {trimmed_filename}')
                new_file.write(merger_merge_content[0].replace(">",">merger merged: "))
                new_file.write(merger_merge_content[1])


def main():
    """
    Main function to execute denoise alignment, merger alignment, and concatenation them together.
    """
    print(f"[INFO] Start to validate in {sys.argv[2]}!")
    denoise_alignment()
    merger_alignment()
    concatenate_denoise_and_merger()
    extract_best_denoise_and_merger()
    print(f"[INFO] End of validation in {sys.argv[2]}!")


if __name__ == '__main__':
    main()
