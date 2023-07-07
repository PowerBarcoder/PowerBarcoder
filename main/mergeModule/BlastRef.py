import linecache as lc


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


class BlastRef:

    def __init__(self):
        self.qseqidList = []
        self.sseqidList = []
        self.pidentList = []
        self.lengthList = []
        self.mismatchList = []
        self.gapopenList = []
        self.qstartList = []
        self.qendList = []
        self.sstartList = []
        self.sendList = []
        self.evalueList = []
        self.bitscoreList = []
        self.qstartMinusQendList = []
        self.sstartMinusSendList = []
        self.rWhoList = []
        self.refList = []

    """
    Step 1 O(N)製作所有key(queryName)清單
    Step 2 O(N)按key塞入所有refBlast的12個值+自己新增的四個值
    Step 3 迴圈跑dict裡的所有key，取出值放進個別欄位的list裡(所以回傳出來16個list，每個list都是Object的一個properties)
    """

    def blastRef(self, load_dir, loci_name, blast_parsing_mode):
        # Step 1: Read file
        with open(load_dir + loci_name + "_refResult.txt", encoding='iso-8859-1') as f:
            lines = f.readlines()

        # Step 2: Initialize the category dictionary and value list
        default_value_List = ["", "", 0, 0, 0, 0, 0, 0, 0, 0, "", 0, 0, 0, "", ""]
        cate = {}

        # Step 3: Process the lines and update the category dictionary
        print("[INFO] blast_parsing_mode = ", blast_parsing_mode)
        for line in lines:
            if not line.strip():
                break

            textList = (line.split("\t"))
            # print(textList) # ['Arachniodes_aristata_122_12_2_01_0.632_abundance_127', 'Cu_po_JP_1', '100.000', '269', '0', '0', '286', '554', '135', '403', '6.28e-143', '497\n']

            # 20230619 因為所有abundance都要做，所以檔名直接用textList[0]，不用再parsing了
            query_name = textList[0] + ".fas"
            qseqid = query_name
            sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = textList[1:12]
            qstartMinusQend = abs(int(qstart) - int(qend)) #20230702 應該是之前用到負數來比了，所以才會取反，這裡補上abs()
            sstartMinusSend = abs(int(sstart) - int(send))
            rWho = "rWho"

            # # add default value in the category dictionary
            if query_name not in cate:
                cate[query_name] = default_value_List

            value_List = [qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue,
                          bitscore, qstartMinusQend, sstartMinusSend, rWho]

        # 一個Sample會blast到多筆，每讀出一行就要檢查是否有更符合條件的值，有的話就更新
        # 使用blastParsingMode參數來決定使用以下四種情境之一 (20230702)
            if blast_parsing_mode == "0":
                # # 模式一:
                # 1.identity: 用3排序，取最高者出來，但不低於85
                # 2.qstart-qend: 用abs(7-8)取最大，但不低於序列長度的一半
                if float(cate[query_name][2]) < float(pident) and float(pident) >= 85 and float(cate[query_name][12]) >= 0.5*float(cate[query_name][3]):
                    cate[query_name] = value_List
                elif float(cate[query_name][2]) == float(pident):
                    if float(cate[query_name][12]) < float(qstartMinusQend):
                        cate[query_name] = value_List
            elif blast_parsing_mode == "1":
                # # 模式二:
                # 1.qstart-qend: 用abs(7-8)取最大，但不低於序列長度的一半
                # 2.identity: 用3排序，取最高者出來，但不低於85
                if float(cate[query_name][12]) < float(qstartMinusQend) and float(pident) >= 85 and float(cate[query_name][12]) >= 0.5*float(cate[query_name][3]):
                    cate[query_name] = value_List
                elif float(cate[query_name][12]) == float(qstartMinusQend):
                    if float(cate[query_name][2]) < float(pident):
                        cate[query_name] = value_List
            elif blast_parsing_mode == "2":
                # # 模式三:
                # 1.qstart-qend & identity 並行，用abs(7-8)*identity取最大，但不低於序列長度的一半，且identity要大於85
                if float(cate[query_name][12])*float(cate[query_name][2]) < float(qstartMinusQend)*float(pident) and float(pident) >= 85 and float(cate[query_name][12]) >= 0.5*float(cate[query_name][3]):
                    cate[query_name] = value_List
            elif blast_parsing_mode == "3":
                # # 模式四:
                # 1. e-value, 越小越好，但不高於0.01，1/10000代表每10000次align才可能出現一次更好的結果
                if float(cate[query_name][10]) < float(evalue) and evalue < 0.01 and float(pident) >= 85 and float(cate[query_name][12]) >= 0.5*float(cate[query_name][3]):
                    cate[query_name] = value_List
            else:
                print("blastParsingMode error")


        # print(cate)
        # print(len(cate.keys())) #這個數應該要跟nonmerge裡面的檔案數量一致，20230206 267沒錯
        # print(len(cate.keys()))

        # Step 4: 物件拼裝
        qseqidList = []
        for key in cate:
            qseqidList.append(cate[key][0])
        self.qseqidList = qseqidList

        sseqidList = []
        for key in cate:
            sseqidList.append(cate[key][1])
        self.sseqidList = sseqidList

        pidentList = []
        for key in cate:
            pidentList.append(cate[key][2])
        self.pidentList = pidentList

        lengthList = []
        for key in cate:
            lengthList.append(cate[key][3])
        self.lengthList = lengthList

        mismatchList = []
        for key in cate:
            mismatchList.append(cate[key][4])
        self.mismatchList = mismatchList

        gapopenList = []
        for key in cate:
            gapopenList.append(cate[key][5])
        self.gapopenList = gapopenList

        qstartList = []
        for key in cate:
            qstartList.append(cate[key][6])
        self.qstartList = qstartList

        qendList = []
        for key in cate:
            qendList.append(cate[key][7])
        self.qendList = qendList

        sstartList = []
        for key in cate:
            sstartList.append(cate[key][8])
        self.sstartList = sstartList

        sendList = []
        for key in cate:
            sendList.append(cate[key][9])
        self.sendList = sendList

        evalueList = []
        for key in cate:
            evalueList.append(cate[key][10])
        self.evalueList = evalueList

        bitscoreList = []
        for key in cate:
            bitscoreList.append(str(cate[key][11]).replace("\n", ""))  # 這裡莫名其妙有個換行
        self.bitscoreList = bitscoreList

        qstartMinusQendList = []
        for key in cate:
            qstartMinusQendList.append(cate[key][12])
        self.qstartMinusQendList = qstartMinusQendList

        sstartMinusSendList = []
        for key in cate:
            sstartMinusSendList.append(cate[key][13])
        self.sstartMinusSendList = sstartMinusSendList

        rWhoList = []
        for key in cate:
            rWhoList.append(cate[key][14])
        self.rWhoList = rWhoList

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
        #  15.   rWhoList(r1或r2)
        #  16.   refList(???)