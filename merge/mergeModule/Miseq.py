class Miseq:
    # 建構式
    def __init__(self):
        self.forword = ""  # True表示放ref頭端，False表示放ref尾端
        self.stickSite = ""  # 拼接點(r1_p2或r2_p1)
        self.F_Rtrim = "deprecated_parameter"  # 從尾trim頭部；從頭trim尾部
        self.delSite = "deprecated_parameter"  # del的位置跟長度
        self.inSite = ""  # in的位置跟長度

    # 印出物件
    def show(self):
        return f'forword: {self.forword}, stickSite(r1_p2,r2_p1): {self.stickSite}, F_Rtrim: {self.F_Rtrim}, delSite: {self.delSite}, inSite: {self.inSite}'
    # {'forword': True, 'stickSiteFinder': 166, 'F_Rtrim': 96, 'del': {45: 6, 173: 96}, 'in': {22: 7}}

        # 定義一個方法用來創建初始陣列，長度為原序列長度，初始值皆為0
    def zeroListMaker(self, n):
        listofzeros = [0] * n
        return listofzeros

# 因為是用ref當中介序列，所以不如直接用ref紀錄接合點位
    # 定義一個方法用產出拼接位點
    def stickSiteFinder(self, r, ref, rWho):
        # 陣列1：重疊判定陣列
        r_arr_overlap = self.zeroListMaker(len(ref))

        # 標記序列位點，
        #   ref r
        # 0  A  A (both)
        # 1  A  - (in)
        # 2  -  A (del)
        # 3  -  - (none)

        for j in range(0, len(ref)):
            if ((r[j] == "-") and (ref[j] == "-")):
                r_arr_overlap[j] = 3
            elif (r[j] != "-") and (ref[j] != "-"):
                r_arr_overlap[j] = 0
            elif ((r[j] == "-") and (ref[j] != "-")):
                r_arr_overlap[j] = 1
            elif ((r[j] != "-") and (ref[j] == "-")):
                r_arr_overlap[j] = 2

        # print("---------------------------")
        # print(r_arr_overlap)
        # print("---------------------------")

        # 直接從r是r1或r2來定義r是起始於ref的左側或右側
        if (rWho == "r1"):
            # target_direction="start from the left side of reference"
            self.forword = True
        elif(rWho == "r2"):
            # target_direction="start from the right side of reference"
            self.forword = False

        # 判斷r與ref重疊區域，即找"0"(譬如557~823)
        firstOne = r_arr_overlap.index(0)
        # code從0起算，所以這裡是557的話，bioedit就是第558個bp開始
        r_arr_overlap.reverse()
        lastOne = len(r_arr_overlap)-r_arr_overlap.index(0)
        # code從0起算，所以這裡是823的話，bioedit就也是到第823個bp結束
        r_arr_overlap.reverse()
        # 序列要轉回來，等等還要用
        # print(firstOne)
        # print(lastOne)
        if rWho == "r1":
            self.stickSite = ["r1_p2",lastOne]
        elif rWho == "r2":
            self.stickSite = ["r2_p1",firstOne]



        # 最後來算一下ref內indel的位點，之後比對的時候可以用這些位點來trim
        # (code從0起算，所以位點也都從0開始)

        # 判斷ref相對於r的indel片段數及其數量
        self.inSite = {}  # insert片段數
        self.delSite = {}  # delet片段數

        # 看ref
        site_status = 99
        site_number = 0
        indel_start_site=0
        for j in range(0, len(ref)):
            # 迴圈逐點檢視，判定當前位點是否與下一點相同，
            if ((j+1) != len(ref)):
                # 位點非最後一位
                if (r_arr_overlap[j] == 1):
                    # insertion
                    if (site_status != 1) and (site_number == 0):
                        # 入口
                        if (r_arr_overlap[j] == r_arr_overlap[j+1]):
                        # 入口但非出口
                            site_status = 1
                            indel_start_site=j
                            self.inSite[j] = 1
                            site_number = site_number+1
                        elif (r_arr_overlap[j] != r_arr_overlap[j+1]):
                        # 入口即出口(即indel僅為單一位點)
                            site_status = 1
                            indel_start_site=j
                            self.inSite[j] = 1
                            # 出口的話要重置
                            site_status = 99
                            site_number = 0
                            indel_start_site=0
                        else:
                            print ("something wrong")
                    elif (site_status == 1)and (site_number != 0) :
                        # 非入口
                        if (r_arr_overlap[j] == r_arr_overlap[j+1]):
                            # 非入口且非出口
                            site_number = site_number+1
                            self.inSite[indel_start_site] = site_number
                        elif (r_arr_overlap[j] != r_arr_overlap[j+1]):
                            # 出口
                            site_number = site_number+1
                            self.inSite[indel_start_site] = site_number
                            # 出口的話要重置
                            site_status = 99
                            site_number = 0
                            indel_start_site=0
                        else:
                            print ("something wrong")
                    else:
                        print ("something wrong")

                elif (r_arr_overlap[j] == 2):
                    # deletion
                    if (site_status != 2) and (site_number == 0):
                        # 入口
                        if (r_arr_overlap[j] == r_arr_overlap[j+1]):
                        # 入口但非出口
                            site_status = 2
                            indel_start_site=j
                            self.delSite[j] = 1
                            site_number = site_number+1
                        elif (r_arr_overlap[j] != r_arr_overlap[j+1]):
                        # 入口即出口(即indel僅為單一位點)
                            site_status = 2
                            indel_start_site=j
                            self.delSite[j] = 1
                            # 出口的話要重置
                            site_status = 99
                            site_number = 0
                            indel_start_site=0
                        else:
                            print ("something wrong")
                    elif (site_status == 2)and (site_number != 0) :
                        # 非入口
                        if (r_arr_overlap[j] == r_arr_overlap[j+1]):
                            # 非入口且非出口
                            site_number = site_number+1
                            self.delSite[indel_start_site] = site_number
                        elif (r_arr_overlap[j] != r_arr_overlap[j+1]):
                            # 出口
                            site_number = site_number+1
                            self.delSite[indel_start_site] = site_number
                            # 出口的話要重置
                            site_status = 99
                            site_number = 0
                            indel_start_site=0
                        else:
                            print ("something wrong")
                    else:
                        print ("something wrong")
            # 位點是最後一位
            elif ((j+1) == len(ref)):
                if (r_arr_overlap[j] == 1):
                    site_number = site_number+1
                    self.inSite[indel_start_site] = site_number
                elif (r_arr_overlap[j] == 2):
                    site_number = site_number+1
                    self.delSite[indel_start_site] = site_number
                else:
                    print ("something wrong")

        return self
