import csv
import hashlib
import os
import sys
import traceback
from main.qc.constants import OVERALL_INFO_STEP_LIST, FILE_SET_PARAMETER_LIST, STEPS


def init():
    global INPUT_PATH, DEMULTIPLEX_UNTRIMMED_PATH, DEMULTIPLEX_TRIMMED_PATH, DEMULTIPLEX_FILTERED_PATH, DENOISE_PAIR_PATH, BLAST_RESULT_PATH, DADA2_DENOISE_R1_PATH, DADA2_DENOISE_R2_PATH, DADA2_MERGED_PATH, DADA2_10N_CAT_PATH, MERGER_MERGED_PATH, OUTPUT_PATH, SEGMENTATION, BEST_ASV_INFO_COLUMN_NAMES
    INPUT_PATH = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.txt"
    DEMULTIPLEX_UNTRIMMED_PATH = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/untrimmed"
    DEMULTIPLEX_TRIMMED_PATH = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/trimmed"
    DEMULTIPLEX_FILTERED_PATH = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/filtered"
    DENOISE_PAIR_PATH = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/denoise_pairs.txt"
    BLAST_RESULT_PATH = sys.argv[1] + sys.argv[2] + "_result/blastResult/" + sys.argv[2] + "_blastResult.txt"
    DADA2_DENOISE_R1_PATH = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/r1/"
    DADA2_DENOISE_R2_PATH = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/r2/"
    DADA2_MERGED_PATH = sys.argv[1] + sys.argv[2] + "_result/mergeResult/dada2/merged/"
    DADA2_10N_CAT_PATH = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/nCatR1R2/"
    MERGER_MERGED_PATH = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/merged/"
    OUTPUT_PATH = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.csv"
    SEGMENTATION = "--------------------------------------------------------------------------------"
    BEST_ASV_INFO_COLUMN_NAMES = ['ASV count', 'best ASV proportion', 'best ASV number', 'hash value']


def parsing_denoise_pair_into_dict(path: str):
    maps = {}
    try:
        # Open the log.txt file for reading with the appropriate encoding
        with open(path, 'r', encoding='iso-8859-1') as file:
            content = file.readlines()
            # Process each line in the content
            for line in content:
                line_pair = line.strip().split(',')
                key, value = line_pair[0], line_pair[1]
                maps[key] = value
    except Exception as unknown_exception:
        print(f"Error decoding file: {unknown_exception}")
    # example:  'rbcLN_fVGF_br16_rECL_br06': 'Deparia_edentula_Wade3820_KTHU2093'
    return maps


def parsing_fastq_reads_number(path: str, prefix: str, file_name: str, rwho: str):
    """
    DEMULTIPLEX_UNTRIMMED_PATH: "rbcLN_fVGF_br01_rECL_br01_r1.fq"
    DEMULTIPLEX_TRIMMED_PATH: "trim_rbcLN_fVGF_br01_rECL_br01_r1.fq"
    DEMULTIPLEX_FILTERED_PATH: "filtered_trim_rbcLN_fVGF_br01_rECL_br01_r1.fq"
    """
    with open(path + "/" + prefix + file_name + "_" + rwho + ".fq", "r") as f:
        # calculate the number of lines
        num_lines = sum(1 for _ in f)
        fastq_reads_number = num_lines / 4
    return fastq_reads_number


def parsing_blast_result_into_dict():
    data_dict = {}
    with open(BLAST_RESULT_PATH, 'r', encoding='iso-8859-1') as file:
        for line in file:
            # TODO 如果r1 r2 blast到的最好的序列不一樣，那會有覆蓋問題，而且你不知道是誰覆蓋誰
            columns = line.strip().split('\t')
            key = columns[0].replace("_r1.fas", "").replace("_r2.fas", "").replace(".fas", "") + ".fas"
            value = [columns[1], columns[2], columns[12]]
            data_dict[key] = value
    return data_dict


def parsing_file_list_into_set(pipeline_step: str):
    with open(INPUT_PATH, 'r', encoding='iso-8859-1') as file:
        content = file.readlines()
        file_set = set()
        record_state = False
        # Process each line in the content
        for line in content:
            if pipeline_step in line:
                record_state = True
            elif SEGMENTATION in line:
                record_state = False
            if record_state:
                file_set.add(line.strip())
    return file_set


def parsing_merged_file_fasta_with_highest_abundance_into_list(filename_set: set, sample_name: str):
    header = ""
    sequence = ""
    filtered_elements = [
        element for element in filename_set if sample_name in element
    ]

    if filtered_elements:
        highest_abundance_element = max(filtered_elements, key=lambda x: float(x.split("_")[-3]))
        # print("Highest abundance element:", highest_abundance_element)
        if not os.path.exists(MERGER_MERGED_PATH + highest_abundance_element):
            return ["N/A", "N/A"]
        with open(MERGER_MERGED_PATH + highest_abundance_element, 'r', encoding='iso-8859-1') as file:
            content = file.readlines()
            # Process each line in the content
            for line in content:
                if line.startswith(">"):
                    header = line.strip()
                else:
                    sequence = line.strip()
    else:
        # print(f"No elements found for {sample_name}")
        return ["N/A", "N/A"]
    return [header, sequence]


def parsing_overall_info_into_list(pipeline_step: str):
    with open(INPUT_PATH, 'r', encoding='iso-8859-1') as file:
        content = file.readlines()
        file_name, num_seqs, sum_len, min_len, max_len, avg_q, err_q = "", "", "", "", "", "", ""
        record_state = False
        # Process each line in the content
        for line in content:
            if pipeline_step in line:
                record_state = True
                file_name = pipeline_step
            elif SEGMENTATION in line:
                record_state = False
            if record_state:
                parameter_list = line.split(" ")
                if len(parameter_list) == 2:
                    avg_q = parameter_list[0].strip()
                    err_q = parameter_list[1].strip()
                elif len(parameter_list) == 4:
                    num_seqs = parameter_list[0].strip()
                    sum_len = parameter_list[1].strip()
                    min_len = parameter_list[2].strip()
                    max_len = parameter_list[3].strip()
        data = [file_name, num_seqs, sum_len, min_len, max_len, avg_q, err_q]
    return data


# prepare the abundance info for "DADA2 denoise r1","DADA2 denoise r2","DADA2 merge","DADA2 10N concat"
def process_abundance_file(file_path):
    sequence_info = [0, 0.0, 0, 0]  # [ASV count, best ASV proportion, best ASV number, hash value]
    abundance_count = []
    best_asv_abundance_proportion = []
    best_asv_abundance_number = []

    with open(file_path, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            header = lines[i].strip()[1:]
            header_words = header.split("_abundance_")  # 用這個切最保險
            # print(header_words)
            abundance_count.append(int(header_words[1]))
            best_asv_abundance_proportion.append(float(header_words[0].split("_")[-1]))
            best_asv_abundance_number.append(int(header_words[1]))

    sequence_info[0] = len(abundance_count)
    sequence_info[1] = max(best_asv_abundance_proportion)
    sequence_info[2] = max(best_asv_abundance_number)

    # 計算best seq. hash，須獨立拿出讀，不然readlines讀完指針就已經讀到底了，後面hash等於拿空的東西去算
    line_number = 2
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            if i + 1 == line_number:
                line = line.strip()
                line_hash = hashlib.md5(line.encode()).hexdigest()
                break
    sequence_info[3] = line_hash

    return sequence_info


def parsing_all_data_into_csv(destination: str):
    overall_info_step_list = OVERALL_INFO_STEP_LIST
    file_set_parameter_list = FILE_SET_PARAMETER_LIST
    steps = STEPS

    with open(destination, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # TODO
        # 7. on-target (mapping, bwa)
        #     (  )這是最後一步，mapping reads/total reads，以後再詳細討論

        # Write file list info header
        writer.writerow(['', '']
                        + [step[0] for step in steps]
                        + ['Highest Abundance ASV'] + _get_dash_list(8)
                        + ['DADA2 denoise r1'] + _get_dash_list(3)
                        + ['DADA2 denoise r2'] + _get_dash_list(3)
                        + ['DADA2 merge'] + _get_dash_list(3)
                        + ['DADA2 10N concat'] + _get_dash_list(3)
                        )
        writer.writerow(['Barcode', 'Sample Name']
                        + [step[1] for step in steps]
                        + ['header', 'sequence', 'length', 'ambiguous sites number', 'lowercase sites number',
                           'BLAST subjectID', 'BLAST identity', 'BLAST qstart-qend', 'Identical to DADA2 merge']
                        + BEST_ASV_INFO_COLUMN_NAMES
                        + BEST_ASV_INFO_COLUMN_NAMES
                        + BEST_ASV_INFO_COLUMN_NAMES
                        + BEST_ASV_INFO_COLUMN_NAMES
                        )

        # Write file list info data
        file_set_list = [parsing_file_list_into_set(parameter) for parameter in file_set_parameter_list]
        sequence_info_dict = parsing_denoise_pair_into_dict(DENOISE_PAIR_PATH)

        # Add each row by iterating the sample we have
        # Write file list info data (part from qc_report.txt)
        # Step 1: Write barcode and sample name column
        for barcode_name, sample_name in sorted(sequence_info_dict.items()):
            try:
                temp_row = []
                for file_set in file_set_list:
                    file_exist = any(barcode_name in filename
                                     or sample_name in filename
                                     for filename in file_set)
                    # Step 2: Write temp_row column: from "Cutadapt demultiplex by sample barcode r1" to "Merger merge"
                    if file_exist:
                        # # 計算以下清單對應檔案的fastq reads number，其他欄位則"V"即可
                        # "Cutadapt demultiplex by sample barcode r1",
                        # "Cutadapt demultiplex by sample barcode r2",
                        # "Cutadapt trim the primer sites r1",
                        # "Cutadapt trim the primer sites r2",
                        # "DADA2 filter r1",
                        # "DADA2 filter r2",
                        if file_set_parameter_list[
                            file_set_list.index(file_set)] == "Cutadapt demultiplex by sample barcode r1":
                            temp_row.append(
                                parsing_fastq_reads_number(DEMULTIPLEX_UNTRIMMED_PATH, "", barcode_name, "r1"))
                        elif file_set_parameter_list[
                            file_set_list.index(file_set)] == "Cutadapt demultiplex by sample barcode r2":
                            temp_row.append(
                                parsing_fastq_reads_number(DEMULTIPLEX_UNTRIMMED_PATH, "", barcode_name, "r2"))
                        elif file_set_parameter_list[
                            file_set_list.index(file_set)] == "Cutadapt trim the primer sites r1":
                            temp_row.append(
                                parsing_fastq_reads_number(DEMULTIPLEX_TRIMMED_PATH, "trim_", barcode_name,
                                                           "r1"))
                        elif file_set_parameter_list[
                            file_set_list.index(file_set)] == "Cutadapt trim the primer sites r2":
                            temp_row.append(
                                parsing_fastq_reads_number(DEMULTIPLEX_TRIMMED_PATH, "trim_", barcode_name,
                                                           "r2"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "DADA2 filter r1":
                            temp_row.append(parsing_fastq_reads_number(DEMULTIPLEX_FILTERED_PATH,
                                                                       "filtered_trim_",
                                                                       barcode_name, "r1"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "DADA2 filter r2":
                            temp_row.append(parsing_fastq_reads_number(DEMULTIPLEX_FILTERED_PATH,
                                                                       "filtered_trim_",
                                                                       barcode_name, "r2"))
                        else:
                            temp_row.append("V")

                        # # 抓取merger merge seq的檔名
                        # if file_set_parameter_list[file_set_list.index(file_set)] == "Merger merge":
                        #     merger_merge_file_name = next((element for element in parsing_file_list_into_set("Merger merge") if element.startswith(sample_name)), None)
                        #     # print("found_element)
                    else:
                        temp_row.append("N/A")
                        print(
                            f"[WARNING] File not found: {sample_name} in {file_set_parameter_list[file_set_list.index(file_set)]}")

                # Step 3: Write "Highest Abundance ASV" column: from "header" to "Identical to DADA2 merge"
                # Write file list info data (part from merged file)
                fasta_seq = parsing_merged_file_fasta_with_highest_abundance_into_list(file_set_list[12], sample_name)
                fasta_header = fasta_seq[0]
                fasta_seq = fasta_seq[1]
                fasta_length = len(fasta_seq) if fasta_seq != "N/A" else "N/A"
                ambiguous_sites_number = sum(1 for i in fasta_seq if
                                             i in ["R", "Y", "M", "K", "S", "W", "N", "r", "y", "m", "k", "s", "w",
                                                   "n"]) if fasta_seq != "N/A" else "N/A"
                lowercase_sites_number = sum(1 for i in fasta_seq if i.islower()) if fasta_seq != "N/A" else "N/A"

                # Write file list info data (part from blastResult.txt)
                # # (we only use the highest abundance seq, fasta_header, which has already been parsed by parsingMergedFileFastaWithHighestAbundanceIntoList())
                merger_merge_file_name = fasta_header.replace(">", "") + ".fas"
                blast_result_dict = parsing_blast_result_into_dict()
                blast_subject_id = blast_result_dict.get(merger_merge_file_name)[0] if fasta_seq != "N/A" else "N/A"
                blast_identity = blast_result_dict.get(merger_merge_file_name)[1] if fasta_seq != "N/A" else "N/A"
                blast_qstart_qend = abs(
                    int(blast_result_dict.get(merger_merge_file_name)[2])) if fasta_seq != "N/A" else "N/A"

                # Write file list info data (part from dada2 merge)
                # # need to check the file exist first
                # # for dada2 seq. we only retrieve the first seq. (highest abundance)
                identical_to_dada2_merge = "N/A"
                merger_merged_file_list = os.listdir(MERGER_MERGED_PATH)
                if os.path.exists(DADA2_MERGED_PATH + sample_name + "_.fas") and os.path.exists(
                        MERGER_MERGED_PATH + fasta_header.replace(">", "") + ".fas"):
                    # dada2_merge_seq = "1"
                    merger_merged_seq = "2"
                    # check all merger merged files with each ASV seq. from dada2 merged file
                    identical_to_dada2_merge = list()
                    for file in merger_merged_file_list:
                        if sample_name in file:
                            # sample : Adiantum_hispidulum_CYH20090701.011_KTHU2052
                            # file : Adiantum_hispidulum_CYH20090701.011_KTHU2052_01_0.973_abundance_110.fas
                            with open(MERGER_MERGED_PATH + fasta_header.replace(">", "") + ".fas",
                                      "r") as merger_merge_file:
                                for line in merger_merge_file:
                                    if line.startswith(">"):
                                        continue
                                    else:
                                        merger_merged_seq = line.strip()
                                        break
                                with open(DADA2_MERGED_PATH + sample_name + "_.fas",
                                          "r") as dada2_merge_file:  # dada2 merged file has multiple seq.
                                    for line in dada2_merge_file:
                                        dada2_merge_seq = line.strip()
                                        if dada2_merge_seq.upper() == merger_merged_seq.upper():
                                            # print(f"[INFO] {dada2_merge_seq} is identical to {merger_merged_seq} in {file}")
                                            abundant = file.split(sample_name)[1].split("_")[1].replace("01",
                                                                                                        "1").replace(
                                                "02", "2").replace("03", "3").replace("04", "4").replace("05",
                                                                                                         "5").replace(
                                                "06", "6").replace("07", "7").replace("08", "8").replace("09", "9")
                                            identical_to_dada2_merge.append(int(abundant))
                                            break
                    if len(identical_to_dada2_merge) > 0:  # sort the list and convert to string
                        """
                        這裡是"最高abundance的merger ASV"與"所有dada2 merge的ASV"做配對，如果序列相同，就寫入list
                        """
                        identical_to_dada2_merge_str = list(str(e) for e in sorted(identical_to_dada2_merge))
                        identical_to_dada2_merge = ','.join(identical_to_dada2_merge_str)
                    else:
                        identical_to_dada2_merge = "N/A"

                # Step 4 : Write "Abundance info" column: from "DADA2 denoise r1" to "DADA2 10N concat"
                # start writing abundance info
                abundance_info_list = list()
                # Process DADA2 denoise r1's abundance data
                abundance_info_list.extend(process_dada2_abundance_data(DADA2_DENOISE_R1_PATH, sample_name))
                # Process DADA2 denoise r2's abundance data
                abundance_info_list.extend(process_dada2_abundance_data(DADA2_DENOISE_R2_PATH, sample_name))
                # Process DADA2 merge's abundance data
                abundance_info_list.extend(process_dada2_abundance_data(DADA2_MERGED_PATH, sample_name))
                # Process DADA2 10N cat's abundance data
                abundance_info_list.extend(process_dada2_abundance_data(DADA2_10N_CAT_PATH, sample_name))

                # Step 5 : Write all columns to the csv file
                # Write file list info data (finally we write the row here)
                writer.writerow([barcode_name, sample_name]
                                + temp_row
                                + [fasta_header, fasta_seq, fasta_length, ambiguous_sites_number,
                                   lowercase_sites_number,
                                   blast_subject_id, blast_identity, blast_qstart_qend, identical_to_dada2_merge]
                                + abundance_info_list
                                )
            except Exception as unknown_exception:
                print(f"Error occurred when processing sample: {sample_name} in qcReport, {unknown_exception}")
                print(traceback.print_exc())

    # Step 6 : Write successful rate info in the last row
    # Write successful rate info in the last row
    with open(destination, 'r', encoding='iso-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        v_count_list = []
        # Iterate over each column except the first one (headers)
        for column_index in range(2, 15):
            column_values = [row[column_index] for row in rows[11:]]  # From the first data row
            v_count = column_values.count('N/A')
            # Add the count to the last row
            v_count_list.append(str(len(column_values) - v_count) + "/" + str((len(column_values))))
        identical_to_dada2_merge_count = len([row[23] for row in rows[11:] if (row[23] != 'N/A') and (row[23] != '')])
    # # Write the updated data back to the CSV file
    with open(destination, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Total success', '-']
                        + v_count_list
                        + _get_dash_list(8) + [str(identical_to_dada2_merge_count)]
                        + _get_dash_list(4)
                        + _get_dash_list(4)
                        + _get_dash_list(4)
                        + _get_dash_list(4)
                        )

    return "Csv generated!"


def _get_dash_list(number: int) -> list:
    return ["-"] * number


def process_dada2_abundance_data(dada2_path, sample_name):
    """
    Process DADA2 abundance data.

    Parameters:
    - dada2_path: The path to the DADA2 file.
    - sample_name: The sample name.

    Returns:
    - A list containing abundance information.
    """
    dada2_file = dada2_path + sample_name + "_.fas"
    if os.path.exists(dada2_file):
        # ['Christella', 'arida', 'Lu31801', 'KTHU2029', '01', 'r1', '1.000', 'abundance', '25']
        return process_abundance_file(dada2_file)
    else:
        return ["N/A", "N/A", "N/A", "N/A"]


def main():
    print(f"[INFO] Start to parse csv in {sys.argv[2]}!")
    try:
        print(parsing_all_data_into_csv(OUTPUT_PATH))
    except Exception as unknown_exception:
        print(f"[ERROR] Something went wrong when parsing csv in {sys.argv[2]}, {unknown_exception}")
        print(traceback.print_exc())
    print(f"[INFO] End of parsing csv in {sys.argv[2]}!")


if __name__ == "__main__":
    init()
    main()
