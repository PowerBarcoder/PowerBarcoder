import csv
import re
import sys

print(f"[INFO] Start to parse csv in {sys.argv[2]}!")

denoise_pair_path = sys.argv[1]+sys.argv[2]+"_result/denoiseResult/denoise_pairs.txt"
input_path = sys.argv[1]+sys.argv[2]+"_result/qcResult/qcReport.txt"
output_path = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.csv"
merged_path = sys.argv[1] + sys.argv[2] + "_result/mergeResult/merger/merged/"

def parsingDenoisePairIntoDict():
    # Open the log.txt file for reading
    with open(denoise_pair_path, 'r') as file:
        content = file.readlines()
        maps = {}
        # Process each line in the content
        for line in content:
            linePair = line.strip().split(',')
            key, value = linePair[0], linePair[1]
            maps[key] = value
    # example:  'rbcLN_fVGF_br16_rECL_br06': 'Deparia_edentula_Wade3820_KTHU2093'
    return maps


def parsingFileListIntoSet(pipline_step:str):
    with open(input_path, 'r') as file:
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


def parsingMergedFileFastaWithHighestAbundanceIntoList(filename_set:set, sample_name:str):
    header = ""
    sequence = ""
    filtered_elements = [
        element for element in filename_set if sample_name in element
    ]

    if filtered_elements:
        highest_abundance_element = max(filtered_elements, key=lambda x: float(x.split("_")[-3]))
        # print("Highest abundance element:", highest_abundance_element)
        with open(merged_path + highest_abundance_element, 'r') as file:
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


def parsingOverallInfoIntoList(pipline_step:str):
    with open(input_path, 'r') as file:
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
                if len(parameter_list)==2:
                    avgQ = parameter_list[0].strip()
                    errQ = parameter_list[1].strip()
                elif len(parameter_list)==4:
                    num_seqs = parameter_list[0].strip()
                    sum_len = parameter_list[1].strip()
                    min_len = parameter_list[2].strip()
                    max_len = parameter_list[3].strip()
        data = [file_name, num_seqs, sum_len, min_len, max_len, avgQ, errQ]
    return data


def parsingAllDataIntoCsv():

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

    file_set_list = []
    for parameter in file_set_parameter_list:
        file_set_list.append(parsingFileListIntoSet(parameter))

    sequence_info_dict = parsingDenoisePairIntoDict()

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
    ] # 營造出合併儲存格的假象

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
            # DADA2 filter 之前的項目:
            # Merger merge: ambiguous sites number (越少越好)
            # Merger blast: BLAST identity, qstart - qend
            # DADA2 denoise 之後的項目:
            # ASV number （越少越好）, evenness （越不平均越好）
            # best 的ASV 的 abundance 跟 proportion

        # overall info
        writer.writerow(['File', 'num_seqs', 'sum_len', 'min_len', 'max_len', 'avgQ', 'errQ'])
        for i in overall_info_step_list:
            overallInfoList = parsingOverallInfoIntoList(i)
            writer.writerow(overallInfoList)
        writer.writerow(['', '', '', '', '', '', ''])

        # file list info
        writer.writerow(['', ''] + [step[0] for step in steps] + ['Highest Abundance Merged header', 'Highest Abundance Merged sequence'])
        writer.writerow(['Sample Name', 'Barcode'] + [step[1] for step in steps] + ['-', '-'])

        for barcode_name, sample_name in sequence_info_dict.items():
            temp_row = []
            for file_set in file_set_list:
                file_exist = any(barcode_name in filename or sample_name in filename for filename in file_set)
                if file_exist:
                    temp_row.append("V")
                else:
                    temp_row.append("N/A")
                    print(f"[WARNING] File not found: {sample_name} in {file_set_parameter_list[file_set_list.index(file_set)]}")
            fasta_seq = parsingMergedFileFastaWithHighestAbundanceIntoList(file_set_list[12],sample_name)
            writer.writerow([sample_name, barcode_name] + temp_row + [fasta_seq[0], fasta_seq[1]])

    return "Csv generated!"

print(parsingAllDataIntoCsv())

print(f"[INFO] End of parsing csv in {sys.argv[2]}!")
