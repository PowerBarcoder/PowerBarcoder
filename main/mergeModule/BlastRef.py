# blast參考物件，blastRef

# load_dir="C:/Users/123/"
#  1.	 qseqid	 query (e.g., gene) sequence id                Microlepia_substrigosa_CYH20090514.016_514.016_01_0.997_abundance_2026_10Ncat
#  2.	 sseqid	 subject (e.g., reference genome) sequence id  MH319942_Dennstaedtiaceae_Histiopteris_incisa
#  3.	 pident	 percentage of identical matches               94.656
#  4.	 length	 alignment length                              262
#  5.	 mismatch	 number of mismatches                      13
#  6.	 gapopen	 number of gap openings                    1
#  7.	 qstart	 start of alignment in query                   1
#  8.	 qend	 end of alignment in query                     262
#  9.	 sstart	 start of alignment in subject                 558
#  10.	 send	 end of alignment in subject                   818
#  11.	 evalue	 expect value                                  3.03e-115
#  12.	 bitscore	 bit score                                 405

# TARGET_FILE_NAME = "_refResult.txt"
TARGET_FILE_NAME = "_refResult_filtered.txt"


class BlastRef:

    def __init__(self):
        self.qseqid_list = []
        self.sseqid_list = []
        self.pident_list = []
        self.length_list = []  # 3
        self.mismatch_list = []
        self.gapopen_list = []
        self.qstart_list = []  # 6
        self.qend_list = []  # 7
        self.sstart_list = []
        self.send_list = []
        self.evalue_list = []
        self.bitscore_list = []
        self.qstart_minus_qend_list = []  # 12
        self.sstart_minus_send_list = []
        self.rwho_list = []
        self.ref_list = []

    def blast_ref(self, load_dir: str, loci_name: str, blast_parsing_mode: str):
        """
        Step 1 O(N)製作所有key(queryName)清單
        Step 2 O(N)按key塞入所有refBlast的12個值+自己新增的四個值
        Step 3 迴圈跑dict裡的所有key，取出值放進個別欄位的list裡(所以回傳出來16個list，每個list都是Object的一個properties)
        """
        qseqid_file_dir_r1 = load_dir + "_result/mergeResult/merger/r1/"
        qseqid_file_dir_r2 = load_dir + "_result/mergeResult/merger/r2/"
        qseqid_file_dir_cat = load_dir + "_result/mergeResult/merger/nCatR1R2/forSplit/"
        # Step 1: Read file
        with open(load_dir + "_result/blastResult/" + loci_name + TARGET_FILE_NAME, encoding='iso-8859-1') as f:
            lines = f.readlines()

        # Step 2: Initialize the category dictionary and value list
        default_value_list = ["", "", 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, "", ""]
        cate = {}

        # Step 3: Process the lines and update the category dictionary
        print("[INFO] blast_parsing_mode = ", blast_parsing_mode)
        temp_query_name = ""  # 給第一個query_name用的，如果下一個query_name跟這個一樣，就不用再讀檔算qseqid序列長度了
        for line in lines:
            if not line.strip():
                break

            text_list = (line.split("\t"))
            # print(text_list) # ['Arachniodes_aristata_122_12_2_01_0.632_abundance_127', 'Cu_po_JP_1', '100.000', '269', '0', '0', '286', '554', '135', '403', '6.28e-143', '497\n']

            # 20230619 因為所有abundance都要做，所以檔名直接用text_list[0]，不用再parsing了
            query_name = text_list[0] + ".fas"
            qseqid = query_name
            sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = text_list[1:12]
            qstart_minus_qend = abs(int(qstart) - int(qend))  # 20230702 應該是之前用到負數來比了，所以才會取反，這裡補上abs()
            sstart_minus_send = abs(int(sstart) - int(send))

            # r1r2 cat起來blast
            rwho = "rWho"
            # r1r2分開blast
            if query_name.find("_r1") != -1:
                rwho = "r1"
            elif query_name.find("_r2") != -1:
                rwho = "r2"

            # # add default value in the category dictionary
            if query_name not in cate:
                cate[query_name] = default_value_list

            value_list = [qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue,
                          bitscore, qstart_minus_qend, sstart_minus_send, rwho]
            # print(value_List)
            # 20230715 修改float(cate[query_name][3])，改成去讀檔算長度，不然這裡的length其實是有align到的範圍的length
            if query_name != temp_query_name:  # 不篩的話讀檔次數要從幾千變幾十萬
                temp_query_name = query_name
                # r1r2分開blast
                if query_name.find("_r1") != -1:
                    qseqid_file_path = qseqid_file_dir_r1 + query_name
                elif query_name.find("_r2") != -1:
                    qseqid_file_path = qseqid_file_dir_r2 + query_name
                # r1r2 cat起來blast
                else:
                    qseqid_file_path = qseqid_file_dir_cat + query_name

                # get fasta sequence length
                with open(qseqid_file_path, encoding='iso-8859-1') as f:
                    lines = f.readlines()
                    qseqid_length = len(lines[1].strip())
                    print(qseqid_file_path, str(qseqid_length))
                    # /PowerBarcoder/data/result/202307150850/trnLF_result/mergeResult/merger/r1/Diplazium_sp._Wade5374_KTHU1451_02_0.387_abundance_251_r1.fas 271

            # 一個Sample會blast到多筆，每讀出一行就要檢查是否有更符合條件的值，有的話就更新
            # 使用blastParsingMode參數來決定使用以下四種情境之一 (20230702)
            # cate[query_name][12]代表當前最高的qstartMinusQend
            # 用float(cate[query_name][12]) < float(qstartMinusQend)可判斷新值是否比舊值大
            # 同理，用float(cate[query_name][2]) == float(pident)可判斷新值是否跟舊值一樣
            if blast_parsing_mode == "0":
                # # 模式一:
                # 1.identity: 用3排序，取最高者出來，但不低於85
                # 2.qstart-qend: 用abs(7-8)取最大，但不低於序列長度的一半
                if float(cate[query_name][2]) < float(pident):
                    # if float(cate[query_name][2]) < float(pident) and float(pident) >= 85 and float(cate[query_name][12]) >= 0.5*float(qseqid_length):
                    cate[query_name] = value_list
                elif float(cate[query_name][2]) == float(pident):
                    if float(cate[query_name][12]) < float(qstart_minus_qend):
                        cate[query_name] = value_list
            elif blast_parsing_mode == "1":
                # # 模式二:
                # 1.qstart-qend: 用abs(7-8)取最大，但不低於序列長度(qseqid_length)的一半
                # 2.identity: 用3排序，取最高者出來，但不低於85
                if float(cate[query_name][12]) < float(qstart_minus_qend):
                    # if float(cate[query_name][12]) < float(qstart_minus_qend) and float(pident) >= 85 and float(qstart_minus_qend) >= 0.5*float(qseqid_length):
                    cate[query_name] = value_list
                elif float(cate[query_name][12]) == float(qstart_minus_qend):
                    if float(cate[query_name][2]) < float(pident):
                        cate[query_name] = value_list
            elif blast_parsing_mode == "2":
                # # 模式三:
                # 1.qstart-qend & identity 並行，用abs(7-8)*identity取最大，但不低於序列長度的一半，且identity要大於85
                # if float(cate[query_name][12])*float(cate[query_name][2]) < float(qstart_minus_qend)*float(pident) and float(pident) >= 85 and float(qstart_minus_qend) >= 0.5*float(qseqid_length):
                if float(cate[query_name][12]) * float(cate[query_name][2]) < float(qstart_minus_qend) * float(pident):
                    # if float(cate[query_name][12])*float(cate[query_name][2]) < float(qstart_minus_qend)*float(pident) and float(pident) >= 85:
                    cate[query_name] = value_list
            elif blast_parsing_mode == "3":
                # # 模式四:
                # 1. e-value, 越小越好，但不高於0.01，1/10000代表每10000次align才可能出現一次更好的結果
                if float(cate[query_name][10]) > float(evalue) and float(evalue) < 0.01:
                    # if float(cate[query_name][10]) > float(evalue) and float(evalue) < 0.01 and float(pident) >= 85 and float(qstart_minus_qend) >= 0.5*float(qseqid_length):
                    cate[query_name] = value_list
            else:
                print("can't choose the right blastParsingMode: " + query_name)

        # print(cate)
        # print(len(cate.keys())) #這個數應該要跟nonmerge裡面的檔案數量一致，20230206 267沒錯
        # print(len(cate.keys()))

        # Step 4: 物件拼裝
        qseqid_list = []
        for key in cate:
            qseqid_list.append(cate[key][0])
        self.qseqid_list = qseqid_list

        sseqid_list = []
        for key in cate:
            sseqid_list.append(cate[key][1])
        self.sseqid_list = sseqid_list

        pident_list = []
        for key in cate:
            pident_list.append(cate[key][2])
        self.pident_list = pident_list

        length_list = []
        for key in cate:
            length_list.append(cate[key][3])
        self.length_list = length_list

        mismatch_list = []
        for key in cate:
            mismatch_list.append(cate[key][4])
        self.mismatch_list = mismatch_list

        gapopen_list = []
        for key in cate:
            gapopen_list.append(cate[key][5])
        self.gapopen_list = gapopen_list

        qstart_list = []
        for key in cate:
            qstart_list.append(cate[key][6])
        self.qstart_list = qstart_list

        qend_list = []
        for key in cate:
            qend_list.append(cate[key][7])
        self.qend_list = qend_list

        sstart_list = []
        for key in cate:
            sstart_list.append(cate[key][8])
        self.sstart_list = sstart_list

        send_list = []
        for key in cate:
            send_list.append(cate[key][9])
        self.send_list = send_list

        evalue_list = []
        for key in cate:
            evalue_list.append(cate[key][10])
        self.evalue_list = evalue_list

        bitscore_list = []
        for key in cate:
            bitscore_list.append(str(cate[key][11]).replace("\n", ""))  # 這裡莫名其妙有個換行
        self.bitscore_list = bitscore_list

        qstart_minus_qend_list = []
        for key in cate:
            qstart_minus_qend_list.append(cate[key][12])
        self.qstart_minus_qend_list = qstart_minus_qend_list

        sstart_minus_send_list = []
        for key in cate:
            sstart_minus_send_list.append(cate[key][13])
        self.sstart_minus_send_list = sstart_minus_send_list

        rwho_list = []
        for key in cate:
            rwho_list.append(cate[key][14])
        self.rwho_list = rwho_list

        return self

        #  1.	 qseqid	 query (e.g., gene) sequence id
        #  2.	 sseqid	 subject (e.g., reference genome) sequence id
        #  3.	 pident	 percentage of identical matches
        #  4.	 length	 alignment length
        #  5.	 mismatch	 number of mismatches
        #  6.	 gapopen	 number of gap openings
        #  7.	 qstart	 start of alignment in query
        #  8.	 qend	 end of alignment in query
        #  9.	 sstart	 start of alignment in subject
        #  10.	 send	 end of alignment in subject
        #  11.	 evalue	 expect value
        #  12.	 bitscore	 bit score
        #  13.   qstartMinusQend
        #  14.   sstartMinusSend
        #  15.   rwho_list(r1或r2)
        #  16.   ref_list(???)

    # r1 r2方向經過10Ncat後都一致了，不需要rc
    # 所以有兩個情況
    # 先用send-sstart判斷方向，>0者，必為正
    # (r1 send - r2 sstart)*1
    # 再用send-sstart判斷方向，<0者，乘負號轉正
    # (r1 send - r2 sstart)*-1
    # 兩個數值pool起來，取出最大者


if __name__ == '__main__':
    test_load_dir = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202311291745/trnLF"
    test_loci_name = "trnLF"
    test_blast_parsing_mode = "0"
    blast_ref_instance = BlastRef()
    blast_ref_instance.blast_ref(test_load_dir, test_loci_name, test_blast_parsing_mode)
    # print(blast_ref_instance.qseqid_list)
    # print(blast_ref_instance.sseqid_list)
    # print(blast_ref_instance.pident_list)
    # print(blast_ref_instance.length_list)
    # print(blast_ref_instance.mismatch_list)
    # print(blast_ref_instance.gapopen_list)
    # print(blast_ref_instance.qstart_list)
    # print(blast_ref_instance.qend_list)
    # print(blast_ref_instance.sstart_list)
    # print(blast_ref_instance.send_list)
    # print(blast_ref_instance.evalue_list)
    # print(blast_ref_instance.bitscore_list)
    # print(blast_ref_instance.qstart_minus_qend_list)
    # print(blast_ref_instance.sstart_minus_send_list)
    # print(blast_ref_instance.rwho_list)
    # print(blast_ref_instance.ref_list)
