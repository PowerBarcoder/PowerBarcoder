import csv
import os
import sys
import traceback

print(f"[INFO] Start to parse csv in {sys.argv[2]}!")

input_path = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.txt"
demultiplex_untrimmed_result_path = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/untrimmed"
demultiplex_trimmed_result_path = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/trimmed"
demultiplex_filtered_result_path = sys.argv[1] + sys.argv[2] + "_result/demultiplexResult/filtered"
denoise_pair_path = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/denoise_pairs.txt"
blast_result_path = sys.argv[1] + sys.argv[2] + "_result/blastResult/" + sys.argv[2] + "_blastResult.txt"
dada2_denoise_r1_path = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/r1/"
dada2_denoise_r2_path = sys.argv[1] + sys.argv[2] + "_result/denoiseResult/r2/"
dada2_merged_path = sys.argv[1] + sys.argv[2] + "_result/mergeResult/dada2/merged/"
dada2_10N_cat_path = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/nCatR1R2/"
merger_merged_path = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/merged/"
output_path = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.csv"


def parsingDenoisePairIntoDict():
    maps = {}
    try:
        # Open the log.txt file for reading with the appropriate encoding
        with open(denoise_pair_path, 'r', encoding='iso-8859-1') as file:
            content = file.readlines()
            # Process each line in the content
            for line in content:
                linePair = line.strip().split(',')
                key, value = linePair[0], linePair[1]
                maps[key] = value
    except Exception as e:
        print(f"Error decoding file: {e}")
    # example:  'rbcLN_fVGF_br16_rECL_br06': 'Deparia_edentula_Wade3820_KTHU2093'
    return maps


def parsingFastqReadsNumber(path:str, prefix:str, file_name:str, rwho:str):
    """
    demultiplex_untrimmed_result_path: "rbcLN_fVGF_br01_rECL_br01_r1.fq"
    demultiplex_trimmed_result_path: "trim_rbcLN_fVGF_br01_rECL_br01_r1.fq"
    demultiplex_filtered_result_path: "filtered_trim_rbcLN_fVGF_br01_rECL_br01_r1.fq"
    """
    with open(path + "/" + prefix + file_name + "_" + rwho +".fq", "r") as f:
        # calculate the number of lines
        num_lines = sum(1 for line in f)
        fastq_reads_number = num_lines / 4
    return fastq_reads_number


def parsingBlastResultIntoDict():
    data_dict = {}
    with open(blast_result_path, 'r', encoding='iso-8859-1') as file:
        for line in file:
            columns = line.strip().split('\t')
            key = columns[0]
            value = [columns[1], columns[2], columns[12]]
            data_dict[key] = value
    return data_dict


def parsingFileListIntoSet(pipline_step: str):
    with open(input_path, 'r', encoding='iso-8859-1') as file:
        content = file.readlines()
        file_set = set()
        record_state = False
        # Process each line in the content
        for line in content:
            if pipline_step in line:
                record_state = True
            elif "--------------------------------------------------------------------------------" in line:
                record_state = False
            if record_state:
                file_set.add(line.strip())
    return file_set


def parsingMergedFileFastaWithHighestAbundanceIntoList(filename_set: set, sample_name: str):
    header = ""
    sequence = ""
    filtered_elements = [
        element for element in filename_set if sample_name in element
    ]

    if filtered_elements:
        highest_abundance_element = max(filtered_elements, key=lambda x: float(x.split("_")[-3]))
        # print("Highest abundance element:", highest_abundance_element)
        with open(merger_merged_path + highest_abundance_element, 'r', encoding='iso-8859-1') as file:
            content = file.readlines()
            # Process each line in the content
            for line in content:
                if line.startswith(">"):
                    header = line.strip()
                else:
                    sequence = line.strip()
    else:
        # print(f"No elements found for {sample_name}")
        header = "N/A"
        sequence = "N/A"
    return [header, sequence]


def parsingOverallInfoIntoList(pipline_step: str):
    with open(input_path, 'r', encoding='iso-8859-1') as file:
        content = file.readlines()
        file_name, num_seqs, sum_len, min_len, max_len, avgQ, errQ = "", "", "", "", "", "", ""
        record_state = False
        # Process each line in the content
        for line in content:
            if pipline_step in line:
                record_state = True
                file_name = pipline_step
            elif "--------------------------------------------------------------------------------" in line:
                record_state = False
            if record_state:
                parameter_list = line.split(" ")
                if len(parameter_list) == 2:
                    avgQ = parameter_list[0].strip()
                    errQ = parameter_list[1].strip()
                elif len(parameter_list) == 4:
                    num_seqs = parameter_list[0].strip()
                    sum_len = parameter_list[1].strip()
                    min_len = parameter_list[2].strip()
                    max_len = parameter_list[3].strip()
        data = [file_name, num_seqs, sum_len, min_len, max_len, avgQ, errQ]
    return data


# prepare the abundance info for "DADA2 denoise r1","DADA2 denoise r2","DADA2 merge","DADA2 10N concat"
def processAbundanceFile(file_path):
    sequence_info = [0, 0.0, 0]
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

    return sequence_info


def parsingAllDataIntoCsv(destination: str):
    overall_info_step_list = [
        "Raw data r1",
        "Raw data r2",
        "Fastp quality trim r1",
        "Fastp quality trim r2",
        "Cutadapt demultiplex by locus primer r1",
        "Cutadapt demultiplex by locus primer r2"
    ]

    file_set_parameter_list = [
        "Cutadapt demultiplex by sample barcode r1",
        "Cutadapt demultiplex by sample barcode r2",
        "Cutadapt trim the primer sites r1",
        "Cutadapt trim the primer sites r2",
        "DADA2 filter r1",
        "DADA2 filter r2",
        "DADA2 denoise r1",
        "DADA2 denoise r2",
        "DADA2 merge",
        "DADA2 10N concat",
        "Merger blast r1",
        "Merger blast r2",
        "Merger merge"
    ]

    steps = [
        ("Cutadapt demultiplex by sample barcode", "r1"),
        ("", "r2"),
        ("Cutadapt trim the primer sites", "r1"),
        ("", "r2"),
        ("DADA2 filter", "r1"),
        ("", "r2"),
        ("DADA2 denoise", "r1"),
        ("", "r2"),
        ("DADA2 merge", "-"),
        ("DADA2 10N concat", "-"),
        ("Merger blast", "r1"),
        ("Merger blast", "r2"),
        ("Merger merge", "-")
    ]  # Create the illusion of merged cells

    with open(destination, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # TODO
        # 7. on-target (mapping, bwa)
        #     (  )這是最後一步，mapping reads/total reads，以後再詳細討論

        # Write overall info header
        writer.writerow(['File', 'num_seqs', 'sum_len', 'min_len', 'max_len', 'avgQ', 'errQ'])
        # Write overall info data
        for step in overall_info_step_list:
            overallInfoList = parsingOverallInfoIntoList(step)
            writer.writerow(overallInfoList)
        writer.writerow(['', '', '', '', '', '', ''])
        writer.writerow(['', '', '', '', '', '', ''])

        # Write file list info header
        writer.writerow(['', '']
                        + [step[0] for step in steps]
                        + ['Highest Abundance ASV', '-', '-', '-', '-', '-', '-', '-', '-']
                        + ['DADA2 denoise r1', '-', '-']
                        + ['DADA2 denoise r2', '-', '-']
                        + ['DADA2 merge', '-', '-']
                        + ['DADA2 10N concat', '-', '-']
                        )
        writer.writerow(['Sample Name', 'Barcode']
                        + [step[1] for step in steps]
                        + ['header', 'sequence', 'length', 'ambiguous sites number', 'lowercase sites number',
                           'BLAST subjectID', 'BLAST identity', 'BLAST qstart-qend', 'Identical to DADA2 merge']
                        + ['ASV count', 'best ASV proportion', 'best ASV number']
                        + ['ASV count', 'best ASV proportion', 'best ASV number']
                        + ['ASV count', 'best ASV proportion', 'best ASV number']
                        + ['ASV count', 'best ASV proportion', 'best ASV number']
                        )

        # Write file list info data
        file_set_list = [parsingFileListIntoSet(parameter) for parameter in file_set_parameter_list]
        sequence_info_dict = parsingDenoisePairIntoDict()

        # Add each row by iterating the sample we have
        # Write file list info data (part from qc_report.txt)
        for barcode_name, sample_name in sequence_info_dict.items():
            try:
                temp_row = []
                for file_set in file_set_list:
                    file_exist = any(barcode_name in filename or sample_name in filename for filename in file_set)
                    if file_exist:
                        # # 計算以下清單對應檔案的fastq reads number，其他欄位則"V"即可
                        # "Cutadapt demultiplex by sample barcode r1",
                        # "Cutadapt demultiplex by sample barcode r2",
                        # "Cutadapt trim the primer sites r1",
                        # "Cutadapt trim the primer sites r2",
                        # "DADA2 filter r1",
                        # "DADA2 filter r2",
                        if file_set_parameter_list[file_set_list.index(file_set)] == "Cutadapt demultiplex by sample barcode r1":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_untrimmed_result_path, "", barcode_name, "r1"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "Cutadapt demultiplex by sample barcode r2":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_untrimmed_result_path, "", barcode_name, "r2"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "Cutadapt trim the primer sites r1":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_trimmed_result_path, "trim_", barcode_name, "r1"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "Cutadapt trim the primer sites r2":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_trimmed_result_path, "trim_", barcode_name, "r2"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "DADA2 filter r1":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_filtered_result_path, "filtered_trim_", barcode_name, "r1"))
                        elif file_set_parameter_list[file_set_list.index(file_set)] == "DADA2 filter r2":
                            temp_row.append(parsingFastqReadsNumber(demultiplex_filtered_result_path, "filtered_trim_", barcode_name, "r2"))
                        else:
                            temp_row.append("V")

                        # # 抓取merger merge seq的檔名
                        # if file_set_parameter_list[file_set_list.index(file_set)] == "Merger merge":
                        #     merger_merge_file_name = next((element for element in parsingFileListIntoSet("Merger merge") if element.startswith(sample_name)), None)
                        #     # print(found_element)
                    else:
                        temp_row.append("N/A")
                        print(
                            f"[WARNING] File not found: {sample_name} in {file_set_parameter_list[file_set_list.index(file_set)]}")

                # Write file list info data (part from merged file)
                fasta_seq = parsingMergedFileFastaWithHighestAbundanceIntoList(file_set_list[12], sample_name)
                fasta_header = fasta_seq[0]
                fasta_seq = fasta_seq[1]
                fasta_length = len(fasta_seq) if fasta_seq != "N/A" else "N/A"
                ambiguous_sites_number = sum(1 for i in fasta_seq if
                                             i in ["R", "Y", "M", "K", "S", "Q", "N", "r", "y", "m", "k", "s", "q",
                                                   "n"]) if fasta_seq != "N/A" else "N/A"
                lowercase_sites_number = sum(1 for i in fasta_seq if i.islower()) if fasta_seq != "N/A" else "N/A"

                # Write file list info data (part from blastResult.txt)
                # # (we only use the highest abundance seq, fasta_header, which has already been parsed by parsingMergedFileFastaWithHighestAbundanceIntoList())
                merger_merge_file_name = fasta_header.replace(">", "") + ".fas"
                blast_result_dict = parsingBlastResultIntoDict()
                blast_subject_id = blast_result_dict[merger_merge_file_name][0] if fasta_seq != "N/A" else "N/A"
                blast_identity = blast_result_dict[merger_merge_file_name][1] if fasta_seq != "N/A" else "N/A"
                blast_qstart_qend = abs(int(blast_result_dict[merger_merge_file_name][2])) if fasta_seq != "N/A" else "N/A"

                # Write file list info data (part from dada2 merge)
                # # need to check the file exist first
                # # for dada2 seq. we only retrieve the first seq. (highest abundance)
                identical_to_DADA2_merge = "N/A"
                if os.path.exists(dada2_merged_path + sample_name + "_.fas") and os.path.exists(
                        merger_merged_path + fasta_header.replace(">", "") + ".fas"):
                    dada2_merge_seq = "1"
                    merger_merged_seq = "2"
                    with open(dada2_merged_path + sample_name + "_.fas", "r") as dada2_merge_file:
                        for line in dada2_merge_file:
                            if line.startswith(">"):
                                continue
                            else:
                                dada2_merge_seq = line.strip()
                                break
                    with open(merger_merged_path + fasta_header.replace(">", "") + ".fas", "r") as merger_merge_file:
                        for line in merger_merge_file:
                            if line.startswith(">"):
                                continue
                            else:
                                merger_merged_seq = line.strip()
                                break
                    if dada2_merge_seq == merger_merged_seq:
                        identical_to_DADA2_merge = "1"
                    else:
                        identical_to_DADA2_merge = "0"

                abundance_info_list = list()

                # Process DADA2 denoise r1's abundance data
                # # ['Christella', 'arida', 'Lu31801', 'KTHU2029', '01', 'r1', '1.000', 'abundance', '25']
                dada2_denoise_r1_file = dada2_denoise_r1_path + sample_name + "_.fas"
                if os.path.exists(dada2_denoise_r1_file):
                    sequence_info = processAbundanceFile(dada2_denoise_r1_file)
                    abundance_info_list.extend(sequence_info)
                else:
                    abundance_info_list.extend(["N/A", "N/A", "N/A"])

                # Process DADA2 denoise r2's abundance data
                # # ['Christella', 'arida', 'Lu31801', 'KTHU2029', '01', 'r1', '1.000', 'abundance', '25']
                dada2_denoise_r2_file = dada2_denoise_r2_path + sample_name + "_.fas"
                if os.path.exists(dada2_denoise_r2_file):
                    sequence_info = processAbundanceFile(dada2_denoise_r2_file)
                    abundance_info_list.extend(sequence_info)
                else:
                    abundance_info_list.extend(["N/A", "N/A", "N/A"])

                # Process DADA2 merge's abundance data
                # # ['Christella', 'arida', 'Lu31801', 'KTHU2029', '01', 'r1', '1.000', 'abundance', '25']
                dada2_merged_file = dada2_merged_path + sample_name + "_.fas"
                if os.path.exists(dada2_merged_file):
                    sequence_info = processAbundanceFile(dada2_merged_file)
                    abundance_info_list.extend(sequence_info)
                else:
                    abundance_info_list.extend(["N/A", "N/A", "N/A"])

                # Process DADA2 10N cat's abundance data
                # # ['Christella', 'arida', 'Lu31801', 'KTHU2029', '01', '1.000', 'abundance', '24']
                dada2_10N_cat_file = dada2_10N_cat_path + sample_name + "_.fas"
                if os.path.exists(dada2_10N_cat_file):
                    sequence_info = processAbundanceFile(dada2_10N_cat_file)
                    abundance_info_list.extend(sequence_info)
                else:
                    abundance_info_list.extend(["N/A", "N/A", "N/A"])

                # Write file list info data (finally we write the row here)
                writer.writerow([sample_name, barcode_name]
                                + temp_row
                                + [fasta_header, fasta_seq, fasta_length, ambiguous_sites_number, lowercase_sites_number,
                                   blast_subject_id, blast_identity, blast_qstart_qend, identical_to_DADA2_merge]
                                + abundance_info_list
                                )
            except Exception as e:
                print("Error occurred when processing sample: " + sample_name +" in qcReport")
                print(e)

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
            v_count_list.append(str(len(column_values) - v_count)+"/"+str((len(column_values))))
    # # Write the updated data back to the CSV file
    with open(destination, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Total success', '-']
                        + v_count_list
                        + ['-', '-', '-', '-', '-', '-', '-', '-', '-']
                        + ['-', '-', '-']
                        + ['-', '-', '-']
                        + ['-', '-', '-']
                        + ['-', '-', '-']
                        )

    return "Csv generated!"


try:
    print(parsingAllDataIntoCsv(output_path))
except Exception as e:
    print(f"[ERROR] Something went wrong when parsing csv in {sys.argv[2]}!")
    print(traceback.print_exc())

print(f"[INFO] End of parsing csv in {sys.argv[2]}!")
