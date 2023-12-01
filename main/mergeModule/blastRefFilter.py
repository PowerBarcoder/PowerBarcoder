import os


def blastRefFilter(load_dir, loci_name, blast_parsing_mode):
    print("[INFO] blast_parsing_mode = ", blast_parsing_mode)
    print("[INFO] blastRefFilter.py is running on loci: " + loci_name)





    # Step 1: Read file
    with open(load_dir + "_result/blastResult/" + loci_name + "_refResult.txt", encoding='iso-8859-1') as f:
        lines = f.readlines()

    # Filter 1：取出r1跟r2共有的序列
    r1_set = set()
    r2_set = set()
    for line in lines:
        if not line.strip():
            break
        textList = (line.split("\t"))
        full_query_name = textList[0]  # Abrodictyum_cumingii_ZXC002739_KTHU1461_01_0.557_abundance_59_r1
        query_rWho = full_query_name.split("_")[-1]  # r1
        query_name = "_".join(full_query_name.split("_")[
                              :-1])  # Abrodictyum_cumingii_ZXC002739_KTHU1461_01_0.557_abundance_59 (因為前面已經10Ncat過了，所以前綴必相等)
        sseqid = textList[1]
        if query_rWho == "r1":
            r1_set.add("_".join([query_name, sseqid]))
        elif query_rWho == "r2":
            r2_set.add("_".join([query_name, sseqid]))
    print("r1_set: ", len(r1_set))
    print("r2_set: ", len(r2_set))
    # get the intersection of r1_set and r2_set
    r1r2_set = r1_set.intersection(r2_set)
    print("r1r2_set: ", len(r1r2_set))
    print("r1r2_set: ", list(r1r2_set)[0:10])

    # 取出後重製refResult.txt成只有r1r2共有的序列的refResult_intersection.txt (428516->376341)
    with open(load_dir + "_result/blastResult/" + loci_name + "_refResult_intersection.txt", "a") as file:
        # clean the file
        file.truncate(0)
    with open(load_dir + "_result/blastResult/" + loci_name + "_refResult_intersection.txt", "a") as file:
        for line in lines:
            if not line.strip():
                break
            textList = (line.split("\t"))
            query_name = "_".join(
                textList[0].split("_")[:-1])  # # Abrodictyum_cumingii_ZXC002739_KTHU1461_01_0.557_abundance_59
            sseqid = textList[1]
            query = "_".join([query_name, sseqid])
            if query in r1r2_set:
                file.write(line)

    # Filter 2：將共有的序列按ASV_ref的方式分類，整理每筆blast結果在檔案內的行數，並計算該配對的overlap長度、identity乘積，取出最佳者
    # 計算方法：
    #     # r1 r2方向經過10Ncat後都一致了，不需要rc，
    #     # 按照ref的方向會有兩種情況
    #     # 先用r1 send - r1 sstart判斷方向，>0者，必為正向
    #     # overlapRange = (r1 send - r2 sstart)*1
    #     # 再用r1 send -r1 sstart判斷方向，<0者，乘負號轉正向
    #     # overlapRange = (r1 send - r2 sstart)*-1
    with open(load_dir + "_result/blastResult/" + loci_name + "_refResult_intersection.txt",
              encoding='iso-8859-1') as f:
        lines = f.readlines()

    rWhoRefPairDict = {}
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

    for lineNumber in range(0, len(lines)):
        if not lines[lineNumber].strip():
            break
        textList = (lines[lineNumber].split("\t"))
        query_name = "_".join(textList[0].split("_")[:-1])
        sseqid = textList[1]
        if rWhoRefPairDict.get(query_name) is None:
            rWhoRefPairDict[query_name] = dict()
        if rWhoRefPairDict[query_name].get(sseqid) is None:
            rWhoRefPairDict[query_name][sseqid] = [[], [], [], []]
        if textList[0].split("_")[-1] == "r1":
            rWhoRefPairDict[query_name][sseqid][0].append(lineNumber)
        elif textList[0].split("_")[-1] == "r2":
            rWhoRefPairDict[query_name][sseqid][1].append(lineNumber)
    for key in rWhoRefPairDict.keys():
        for key2 in rWhoRefPairDict[key].keys():
            r1send = int(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[9])
            r1start = int(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[8])
            r2start = int(lines[rWhoRefPairDict[key][key2][1][0]].split("\t")[8])
            r1Identity = float(lines[rWhoRefPairDict[key][key2][0][0]].split("\t")[2])
            r2Identity = float(lines[rWhoRefPairDict[key][key2][1][0]].split("\t")[2])
            if r1send - r1start > 0:
                overlapRange = (r1send - r2start) * 1
            elif r1send - r1start < 0:
                overlapRange = (r1send - r2start) * -1
            else:
                overlapRange = 0
            rWhoRefPairDict[key][key2][2].append(overlapRange)
            rWhoRefPairDict[key][key2][3].append(r1Identity * r2Identity)
    print(rWhoRefPairDict.get("Alsophila_gigantea_Wade4161_KTHU1758_04_0.014_abundance_8"))

    # 同ASV名稱的，取出overlap最大者留在dict裡，其他的刪除
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in rWhoRefPairDict.keys():
        overlapRangeList = []  # [218, 217, 216, 216, 217, 215,...]
        for key2 in rWhoRefPairDict[key].keys():
            overlapRangeList.append(rWhoRefPairDict[key][key2][2][0])
        maxOverlapRange = max(overlapRangeList)

        # Mark keys for deletion
        for key2 in rWhoRefPairDict[key].keys():
            if rWhoRefPairDict[key][key2][2][0] < maxOverlapRange:
                keys_to_delete.append((key, key2))

    # Delete marked keys
    for key, key2 in keys_to_delete:
        del rWhoRefPairDict[key][key2]
    print(rWhoRefPairDict.get("Alsophila_gigantea_Wade4161_KTHU1758_04_0.014_abundance_8"))

    # 同ASV名稱的，若overlap最大者超過1個，就取出identity最大者留在dict裡，其他的刪除
    keys_to_delete = []  # Create a list to store keys to be deleted
    for key in rWhoRefPairDict.keys():
        identityList = []
        for key2 in rWhoRefPairDict[key].keys():
            identityList.append(rWhoRefPairDict[key][key2][3][0])
        maxIdentity = max(identityList)
        # Mark keys for deletion
        for key2 in rWhoRefPairDict[key].keys():
            if rWhoRefPairDict[key][key2][3][0] < maxIdentity:
                keys_to_delete.append((key, key2))
    # Delete marked keys
    for key, key2 in keys_to_delete:
        del rWhoRefPairDict[key][key2]
    print(rWhoRefPairDict.get("Alsophila_gigantea_Wade4161_KTHU1758_04_0.014_abundance_8"))

    # 使用dict的key來產生新的refResult_overlap.txt
    with open(load_dir + "_result/blastResult/" + loci_name + "_refResult_filtered.txt", "a") as file:
        for key in rWhoRefPairDict.keys():
            for key2 in rWhoRefPairDict[key].keys():
                file.write(lines[rWhoRefPairDict[key][key2][0][0]])
                file.write(lines[rWhoRefPairDict[key][key2][1][0]])

    return rWhoRefPairDict


if __name__ == '__main__':
    load_dir = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202311291745/trnLF"
    loci_name = "trnLF"
    blast_parsing_mode = "0"
    blastRefFilter(load_dir, loci_name, blast_parsing_mode)
