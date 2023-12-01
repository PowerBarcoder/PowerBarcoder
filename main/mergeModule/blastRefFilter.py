import os

# Define constants
SSTART_INDEX = 9
SEND_INDEX = 8
IDENTITY_INDEX = 2
SSEQID_INDEX = 1
QSSEQID_INDEX = 0


def blastRefFilter(load_dir, loci_name, blast_parsing_mode):
    # File paths using os.path.join
    input_file_path = os.path.join(load_dir + "_result/blastResult", f"{loci_name}_refResult.txt")
    intersection_file_path = os.path.join(load_dir + "_result/blastResult", f"{loci_name}_refResult_intersection.txt")
    filtered_file_path = os.path.join(load_dir + "_result/blastResult", f"{loci_name}_refResult_filtered.txt")

    print("[INFO] blast_parsing_mode = ", blast_parsing_mode)
    print("[INFO] blastRefFilter.py is running on loci: " + loci_name)

    # Step 1: Read file
    with open(input_file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()
        original_line_count = len(lines)

    # Filter 1: Use sets for r1_set, r2_set, and r1r2_set
    r1_set = set()
    r2_set = set()

    for line in lines:
        if not line.strip():
            break
        text_list = line.split("\t")
        query_rWho = text_list[QSSEQID_INDEX].split("_")[-1]
        query_name = "_".join(text_list[QSSEQID_INDEX].split("_")[:-1])

        if query_rWho == "r1":
            r1_set.add("_".join([query_name, text_list[SSEQID_INDEX]]))
        elif query_rWho == "r2":
            r2_set.add("_".join([query_name, text_list[SSEQID_INDEX]]))

    r1r2_set = r1_set.intersection(r2_set)
    # Output to refResult_intersection.txt
    with open(intersection_file_path, "a") as file:
        # Clean the file
        file.truncate(0)
        file.seek(0)  # Move the cursor to the beginning
        for line in lines:
            if not line.strip():
                break
            text_list = line.split("\t")
            query = "_".join(text_list[QSSEQID_INDEX].rsplit("_", 1)[:-1]) + "_" + text_list[SSEQID_INDEX]
            if query in r1r2_set:
                file.write(line)

    # Filter 2: Use constants for indices
    with open(intersection_file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()

    rWhoRefPairDict = {}

    for line_number in range(0, len(lines)):
        if not lines[line_number].strip():
            break
        text_list = lines[line_number].split("\t")
        query_name = "_".join(text_list[QSSEQID_INDEX].split("_")[:-1])
        sseqid = text_list[SSEQID_INDEX]

        if rWhoRefPairDict.get(query_name) is None:
            rWhoRefPairDict[query_name] = dict()

        if rWhoRefPairDict[query_name].get(sseqid) is None:
            rWhoRefPairDict[query_name][sseqid] = [[], [], [], []]

        if text_list[QSSEQID_INDEX].split("_")[-1] == "r1":
            rWhoRefPairDict[query_name][sseqid][0].append(line_number)
        elif text_list[QSSEQID_INDEX].split("_")[-1] == "r2":
            rWhoRefPairDict[query_name][sseqid][1].append(line_number)

    for key in rWhoRefPairDict.keys():
        for key2 in rWhoRefPairDict[key].keys():
            r1send = int(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[SSTART_INDEX])
            r1start = int(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[SEND_INDEX])
            r2start = int(lines[rWhoRefPairDict[key][key2][1][0]].split("\t")[SEND_INDEX])
            r1_identity = float(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[IDENTITY_INDEX])
            r2_identity = float(lines[rWhoRefPairDict[key][key2][1][0]].split("\t")[IDENTITY_INDEX])

            if r1send - r1start > 0:
                overlap_range = (r1send - r2start) * 1
            elif r1send - r1start < 0:
                overlap_range = (r1send - r2start) * -1
            else:
                overlap_range = 0

            rWhoRefPairDict[key][key2][2].append(overlap_range)
            rWhoRefPairDict[key][key2][3].append(r1_identity * r2_identity)

    # Filter 3: Use constants for indices
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in rWhoRefPairDict.keys():
        overlap_range_list = []  # [218, 217, 216, 216, 217, 215,...]
        for key2 in rWhoRefPairDict[key].keys():
            overlap_range_list.append(rWhoRefPairDict[key][key2][2][0])
        max_overlap_range = max(overlap_range_list)

        # Mark keys for deletion
        for key2 in rWhoRefPairDict[key].keys():
            if rWhoRefPairDict[key][key2][2][0] < max_overlap_range:
                keys_to_delete.append((key, key2))

    # Delete marked keys
    for key, key2 in keys_to_delete:
        del rWhoRefPairDict[key][key2]

    # Filter 4: Use constants for indices
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in rWhoRefPairDict.keys():
        identity_list = []
        for key2 in rWhoRefPairDict[key].keys():
            identity_list.append(rWhoRefPairDict[key][key2][3][0])
        max_identity = max(identity_list)

        # Mark keys for deletion
        for key2 in rWhoRefPairDict[key].keys():
            if rWhoRefPairDict[key][key2][3][0] < max_identity:
                keys_to_delete.append((key, key2))

    # Delete marked keys
    for key, key2 in keys_to_delete:
        del rWhoRefPairDict[key][key2]

    # Write to refResult_filtered.txt
    with open(filtered_file_path, "a") as file:
        # Clean the file
        file.truncate(0)
        file.seek(0)  # Move the cursor to the beginning

        for key in rWhoRefPairDict.keys():
            for key2 in rWhoRefPairDict[key].keys():
                file.write(lines[rWhoRefPairDict[key][key2][0][0]])
                file.write(lines[rWhoRefPairDict[key][key2][1][0]])

    # Count lines
    with open(filtered_file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()
        final_line_count = len(lines)

    print(
        f"[INFO] blastRefFilter.py filtered file from {original_line_count} lines of reads to {final_line_count} lines on loci: {loci_name}"
    )

    return rWhoRefPairDict


if __name__ == '__main__':
    load_dir = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202312011906/trnLF"
    loci_name = "trnLF"
    blast_parsing_mode = "2"
    print(f"execute file directly with path: {load_dir}")
    blastRefFilter(load_dir, loci_name, blast_parsing_mode)
