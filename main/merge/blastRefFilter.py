import os

# Define constants (TODO 添加更多參數，用於計算新的 identity)
SSTART_INDEX = 9
SEND_INDEX = 8
IDENTITY_INDEX = 2
SSEQID_INDEX = 1
QSSEQID_INDEX = 0


def blast_ref_filter(load_dir: str, loci_name: str, blast_parsing_mode: str):
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
    # 過濾步驟 1：根據 r1 和 r2 的標記，將比對結果分別存入兩個集合，並找出兩者的交集
    r1_set = set()
    r2_set = set()

    for line in lines:
        if not line.strip():
            break
        text_list = line.split("\t")
        query_r_who = text_list[QSSEQID_INDEX].split("_")[-1]
        query_name = "_".join(text_list[QSSEQID_INDEX].split("_")[:-1])

        if query_r_who == "r1":
            r1_set.add("_".join([query_name, text_list[SSEQID_INDEX]]))
        elif query_r_who == "r2":
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
    # 過濾步驟 2：根據交集結果，計算每個比對對應的 overlap長度 和 identity 比率，並存入字典。
    # (將共有的序列按ASV_ref的方式分類，整理每筆blast結果在檔案內的行數，並計算該配對的overlap長度、identity乘積，取出最佳者)
    # 計算方法：
    #     # r1 r2方向經過10Ncat後都一致了，不需要rc，
    #     # 按照ref的方向會有兩種情況
    #     # 先用r1 send - r1 sstart判斷方向，>0者，必為正向
    #     # overlapRange = (r1 send - r2 sstart)*1
    #     # 再用r1 send -r1 sstart判斷方向，<0者，乘負號轉正向
    #     # overlapRange = (r1 send - r2 sstart)*-1

    with open(intersection_file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()

    r_who_ref_pair_dict = {}
    """
    example:
    {
        "Pronephrium_parishii_Wade5807_KTHU2139_02_0.398_abundance_840":{
            "Diplazium_fraxinifolium":[
                                        [9430], # r1 line number
                                        [200411], # r2 line number
                                        [185] # overlap length
                                        [9147.859749000001] # r1 identity * r2 identity
                                    ],...
        }
    }
    """

    for line_number in range(0, len(lines)):
        if not lines[line_number].strip():
            break
        text_list = lines[line_number].split("\t")
        query_name = "_".join(text_list[QSSEQID_INDEX].split("_")[:-1])
        sseqid = text_list[SSEQID_INDEX]

        if r_who_ref_pair_dict.get(query_name) is None:
            r_who_ref_pair_dict[query_name] = dict()

        if r_who_ref_pair_dict[query_name].get(sseqid) is None:
            r_who_ref_pair_dict[query_name][sseqid] = [[], [], [], []]

        if text_list[QSSEQID_INDEX].split("_")[-1] == "r1":
            r_who_ref_pair_dict[query_name][sseqid][0].append(line_number)
        elif text_list[QSSEQID_INDEX].split("_")[-1] == "r2":
            r_who_ref_pair_dict[query_name][sseqid][1].append(line_number)

    for key in r_who_ref_pair_dict.keys():
        for key2 in r_who_ref_pair_dict[key].keys():
            r1send = int(lines[r_who_ref_pair_dict[key][key2][0][0]].split("\t")[SSTART_INDEX])
            r1start = int(lines[r_who_ref_pair_dict[key][key2][0][0]].split("\t")[SEND_INDEX])
            r2start = int(lines[r_who_ref_pair_dict[key][key2][1][0]].split("\t")[SEND_INDEX])
            r1_identity = float(lines[r_who_ref_pair_dict[key][key2][0][0]].split("\t")[IDENTITY_INDEX])
            r2_identity = float(lines[r_who_ref_pair_dict[key][key2][1][0]].split("\t")[IDENTITY_INDEX])

            if r1send - r1start > 0:
                overlap_range = (r1send - r2start) * 1
            elif r1send - r1start < 0:
                overlap_range = (r1send - r2start) * -1
            else:
                overlap_range = 0

            r_who_ref_pair_dict[key][key2][2].append(overlap_range)
            r_who_ref_pair_dict[key][key2][3].append(r1_identity * r2_identity) # TODO： 1 - (r1 mismatch + r2 mismatch)/ (abs(r1 qstart-qend)+1 + abs(r2 qstart-qend)+1)

    # Filter 3: Use constants for indices (同ASV名稱的，取出overlap最大者留在dict裡，其他的刪除)
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in r_who_ref_pair_dict.keys():
        overlap_range_list = []  # [218, 217, 216, 216, 217, 215,...]
        for key2 in r_who_ref_pair_dict[key].keys():
            overlap_range_list.append(r_who_ref_pair_dict[key][key2][2][0])
        max_overlap_range = max(overlap_range_list)

        # Mark keys for deletion
        for key2 in r_who_ref_pair_dict[key].keys():
            if r_who_ref_pair_dict[key][key2][2][0] < max_overlap_range:
                keys_to_delete.append((key, key2))

    # Delete marked keys
    for key, key2 in keys_to_delete:
        del r_who_ref_pair_dict[key][key2]

    # Filter 4: Use constants for indices (同ASV名稱的，若overlap最大者超過1個，就取出identity最大者留在dict裡，其他的刪除)
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in r_who_ref_pair_dict.keys():
        identity_list = []
        for key2 in r_who_ref_pair_dict[key].keys():
            identity_list.append(r_who_ref_pair_dict[key][key2][3][0])
        max_identity = max(identity_list)

        # Mark keys for deletion
        for key2 in r_who_ref_pair_dict[key].keys():
            if r_who_ref_pair_dict[key][key2][3][0] < max_identity:
                keys_to_delete.append((key, key2))

    # Delete marked keys
    for key, key2 in keys_to_delete:
        del r_who_ref_pair_dict[key][key2]

    # Write to refResult_filtered.txt
    with open(filtered_file_path, "a") as file:
        # Clean the file
        file.truncate(0)
        file.seek(0)  # Move the cursor to the beginning

        for key in r_who_ref_pair_dict.keys():
            for key2 in r_who_ref_pair_dict[key].keys():
                file.write(lines[r_who_ref_pair_dict[key][key2][0][0]])
                file.write(lines[r_who_ref_pair_dict[key][key2][1][0]])

    # Count lines
    with open(filtered_file_path, encoding='iso-8859-1') as f:
        lines = f.readlines()
        final_line_count = len(lines)

    print(
        f"[INFO] blastRefFilter.py filtered file from {original_line_count} lines of reads to {final_line_count} lines on loci: {loci_name}"
    )

    return r_who_ref_pair_dict


if __name__ == '__main__':
    main_load_dir = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202312011906/trnLF"
    main_loci_name = "trnLF"
    main_blast_parsing_mode = "2"
    print(f"execute file directly with path: {main_load_dir}")
    blast_ref_filter(main_load_dir, main_loci_name, main_blast_parsing_mode)
