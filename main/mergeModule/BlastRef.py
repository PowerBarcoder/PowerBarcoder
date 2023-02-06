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
            self.sseqidList=[]
            self.pidentList=[]
            self.lengthList=[]
            self.mismatchList=[]
            self.gapopenList=[]
            self.qstartList=[]
            self.qendList=[]
            self.sstartList=[]
            self.sendList=[]
            self.evalueList=[]
            self.bitscoreList=[]
            self.qstartMinusQendList=[]
            self.sstartMinusSendList=[]
            self.rWhoList=[]
            self.refList=[]

    """
    Step 1 O(N)製作所有key(queryName)清單
    Step 2 O(N)按key塞入所有refBlast的12個值+自己新增的四個值
    Step 3 迴圈跑dict裡的所有key，取出值放進個別欄位的list裡(所以回傳出來16個list，每個list都是Object的一個properties)
    """
    def blastRef(self, load_dir,loci_name):
        List=[]
        #製作所有key的清單
        i=1
        text=lc.getline(load_dir+loci_name+"_refResult.txt",1)
        while len(text)>1:
            text=lc.getline(load_dir+loci_name+"_refResult.txt",i)
            if (len(text)<1):
                break

            textList=[]
            textList=text.split("	") #檔案是用tab分隔的
            qseqid=textList[0]
            qseqidSplitList=textList[0].split("_")
            
            # 名稱案例：

            # queryName=qseqidSplitList[3]+"_"+qseqidSplitList[2]+"_"+qseqidSplitList[0]+"_"+qseqidSplitList[1]+"_.fas"
            # # LocalBlast內的：Asplenium_affine_Wade4208_KTHU1183_01_r1_1.000_abundance_65
            # # 當前的名      ：KTHU1183_Wade4208_Asplenium_affine_.fas
            # # 實際r1的名    ：KTHU1183_Wade4208_Asplenium_affine_.fas
            
            # queryName=qseqidSplitList[4]+"_"+qseqidSplitList[3]+"_"+qseqidSplitList[0]+"_"+qseqidSplitList[1]+"_"+qseqidSplitList[2]+"_.fas"
            # # LocalBlast內的：Asplenium_aff._normale_Kuo3457_KTHU1185_01_r1_1.000_abundance_53
            # # 當前的名      ：KTHU1185_Kuo3457_Asplenium_aff._normale_.fas
            # # 實際r1的名    ：KTHU1185_Kuo3457_Asplenium_aff._normale_.fas

            # 最終定案規律如下：localblast轉換成r1或r2檔名的邏輯，先trim掉dada2的後綴(5個)，然後按[KTHUXXX]_[採集號]_[種名]_.fas排
            queryName=qseqidSplitList[:-5][-1]+"_"+qseqidSplitList[:-5][-2]+"_"+"_".join(qseqidSplitList[:-5][:-2])+"_.fas"

            List.append(queryName)
            
            i=i+1

        cate=dict([(k,["","",0,0,0,0,0,0,0,0,"",0,0,0,"",""]) for k in List])
        # 第一個是qseqid，第二個是sseqid，第三個是pident...以此類推
        # print(len(cate))
        # 有31個檔案沒錯

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

        #接上，將value一一貼到key的list裡
        i=1
        text=lc.getline(load_dir+loci_name+"_refResult.txt",1)
        while len(text)>1:
            text=lc.getline(load_dir+loci_name+"_refResult.txt",i)
            if (len(text)<1):
                break
            
            # 第一個是sseqid，第二個是pident，第三個是qstartMinusQend

            # 1.用3排序，取最高者出來，pident=textList[2]  #現在是取最高，可是實際上產出的序列可能%很低，所以把%家在檔名上
            #     如果之後要做篩選，可以從檔名判斷，只要abundance或%有一個過低，就列進清單裡
            # 2.用abs(7-8)取最大，qstartMinusQend=abs(textList[6]-textList[7])

            textList=[]
            textList=text.split("	")
            qseqid=textList[0]
            qseqidSplitList=textList[0].split("_")
            
            # 名稱案例：

            # queryName=qseqidSplitList[3]+"_"+qseqidSplitList[2]+"_"+qseqidSplitList[0]+"_"+qseqidSplitList[1]+"_.fas"
            # # LocalBlast內的：Asplenium_affine_Wade4208_KTHU1183_01_r1_1.000_abundance_65
            # # 當前的名      ：KTHU1183_Wade4208_Asplenium_affine_.fas
            # # 實際r1的名    ：KTHU1183_Wade4208_Asplenium_affine_.fas
            
            # queryName=qseqidSplitList[4]+"_"+qseqidSplitList[3]+"_"+qseqidSplitList[0]+"_"+qseqidSplitList[1]+"_"+qseqidSplitList[2]+"_.fas"
            # # LocalBlast內的：Asplenium_aff._normale_Kuo3457_KTHU1185_01_r1_1.000_abundance_53
            # # 當前的名      ：KTHU1185_Kuo3457_Asplenium_aff._normale_.fas
            # # 實際r1的名    ：KTHU1185_Kuo3457_Asplenium_aff._normale_.fas


            #
            # 最終定案規律如下：localblast轉換成r1或r2檔名的邏輯，先trim掉dada2的後綴(5個)，然後按[KTHUXXX]_[採集號]_[種名]_.fas排
            queryName=qseqidSplitList[:-5][-1]+"_"+qseqidSplitList[:-5][-2]+"_"+"_".join(qseqidSplitList[:-5][:-2])+"_.fas"
            # 這邊取出abundance最高的

            qseqid=queryName
            sseqid=textList[1]
            pident=textList[2]
            length=textList[3]
            mismatch=textList[4]
            gapopen=textList[5]
            qstart=textList[6]
            qend=textList[7]
            sstart=textList[8]
            send=textList[9]
            evalue=textList[10]
            bitscore=textList[11]
            qstartMinusQend=(int(textList[6])-int(textList[7]))
            sstartMinusSend=(int(textList[8])-int(textList[9]))
            # 20230206 10N 處理下，棄用rWho直接寫死，在下一步再按順序判斷
            # rWho=qseqidSplitList[-4] #從後面取過來，因為後綴是dada2加的，固定四個"Nephrolepis_sp._Lu30199_Co262_01_r1_0.976_abundance_280"
            rWho="rWho" #從後面取過來，因為後綴是dada2加的，固定四個"Nephrolepis_sp._Lu30199_Co262_01_r1_0.976_abundance_280"




            # 1.用3排序，取最高者出來，(改成只做>90的，下限90當參數可設，全部做完再挑最高的當best，其他當others) # 判斷順序：%>abundance>orders
            # 2.用abs(7-8)取最大，
            if (float(cate[queryName][2])<float(pident)):
                cate[queryName][0]=qseqid
                cate[queryName][1]=sseqid
                cate[queryName][2]=pident
                cate[queryName][3]=length
                cate[queryName][4]=mismatch
                cate[queryName][5]=gapopen
                cate[queryName][6]=qstart
                cate[queryName][7]=qend
                cate[queryName][8]=sstart
                cate[queryName][9]=send
                cate[queryName][10]=evalue
                cate[queryName][11]=bitscore
                cate[queryName][12]=qstartMinusQend
                cate[queryName][13]=sstartMinusSend
                cate[queryName][14]=rWho

            elif (float(cate[queryName][2])==float(pident)):
                if(float(cate[queryName][12])<float(qstartMinusQend)):
                    cate[queryName][0]=qseqid
                    cate[queryName][1]=sseqid
                    cate[queryName][2]=pident
                    cate[queryName][3]=length
                    cate[queryName][4]=mismatch
                    cate[queryName][5]=gapopen
                    cate[queryName][6]=qstart
                    cate[queryName][7]=qend
                    cate[queryName][8]=sstart
                    cate[queryName][9]=send
                    cate[queryName][10]=evalue
                    cate[queryName][11]=bitscore
                    cate[queryName][12]=qstartMinusQend
                    cate[queryName][13]=sstartMinusSend
                    cate[queryName][14]=rWho

            i=i+1

        # print(cate)
        print(len(cate.keys())) #這個數應該要跟nonmerge裡面的檔案數量一致
        # print(len(cate.keys()))

        qseqidList=[]
        for key in cate:
            qseqidList.append(cate[key][0])
        self.qseqidList=qseqidList

        sseqidList=[]
        for key in cate:
            sseqidList.append(cate[key][1])
        self.sseqidList=sseqidList

        pidentList=[]
        for key in cate:
            pidentList.append(cate[key][2])
        self.pidentList=pidentList

        lengthList=[]
        for key in cate:
            lengthList.append(cate[key][3])
        self.lengthList=lengthList

        mismatchList=[]
        for key in cate:
            mismatchList.append(cate[key][4])
        self.mismatchList=mismatchList
                        
        gapopenList=[]
        for key in cate:
            gapopenList.append(cate[key][5])
        self.gapopenList=gapopenList

        qstartList=[]
        for key in cate:
            qstartList.append(cate[key][6])
        self.qstartList=qstartList

        qendList=[]
        for key in cate:
            qendList.append(cate[key][7])
        self.qendList=qendList

        sstartList=[]
        for key in cate:
            sstartList.append(cate[key][8])
        self.sstartList=sstartList

        sendList=[]
        for key in cate:
            sendList.append(cate[key][9])
        self.sendList=sendList

        evalueList=[]
        for key in cate:
            evalueList.append(cate[key][10])
        self.evalueList=evalueList

        bitscoreList=[]
        for key in cate:
            bitscoreList.append(cate[key][11].replace("\n",""))#這裡莫名其妙有個換行
        self.bitscoreList=bitscoreList

        qstartMinusQendList=[]
        for key in cate:
            qstartMinusQendList.append(cate[key][12])
        self.qstartMinusQendList=qstartMinusQendList

        sstartMinusSendList=[]
        for key in cate:
            sstartMinusSendList.append(cate[key][13])
        self.sstartMinusSendList=sstartMinusSendList

        rWhoList=[]
        for key in cate:
            rWhoList.append(cate[key][14])
        self.rWhoList=rWhoList

        return self
