import csv
import sys

print(f"[INFO] Start to parse csv in {sys.argv[2]}!")

denoise_pair_path = sys.argv[1]+sys.argv[2]+"_result/denoiseResult/denoise_pairs.txt"
load_path = sys.argv[1]+sys.argv[2]+"_result/qcResult/"
output_path = sys.argv[1] + sys.argv[2] + "_result/qcResult/qcReport.csv"

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
    with open(load_path+"qcReport.txt", 'r') as file:
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


def parsingAllDataIntoCsv():
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
        writer.writerow(['', ''] + [step[0] for step in steps])
        writer.writerow(['Sample Name', 'Barcode'] + [step[1] for step in steps])

        for barcode_name, sample_name in sequence_info_dict.items():
            temp_row = []
            for file_set in file_set_list:
                file_exist = any(barcode_name in filename or sample_name in filename for filename in file_set)
                if file_exist:
                    temp_row.append("V")
                else:
                    temp_row.append("N/A")
                    print(f"[WARNING] File not found: {sample_name} in {file_set_parameter_list[file_set_list.index(file_set)]}")
            writer.writerow([sample_name, barcode_name] + temp_row)

    return "Csv generated!"

print(parsingAllDataIntoCsv())

print(f"[INFO] End of parsing csv in {sys.argv[2]}!")
