# 標記序列位點，      #   ref r
OVERLAP_BOTH = 0  # 0  A  A (both)  # OVERLAP_BOTH=r_arr_overlap[j] 0=皆不空
OVERLAP_INSERT = 1  # 1  A  - (in)    # OVERLAP_INSERT=r_arr_overlap[j] 1=r空
OVERLAP_DELETE = 2  # 2  -  A (del)   # OVERLAP_DELET=r_arr_overlap[j] 2=ref空
OVERLAP_NONE = 3  # 3  -  - (none)  # OVERLAP_NONE=r_arr_overlap[j] 3=皆空
OVERLAP_UNKNOWN = 99


def zero_list_maker(n):
    list_of_zeros = [0] * n
    return list_of_zeros


class Miseq:
    """
    @class Miseq
    @brief A class to represent Miseq sequencing data and perform sequence alignment and analysis.
    """

    def __init__(self):
        """
        @brief Initialize a Miseq object.
        """
        self.forword = ""  # True表示放ref頭端，False表示放ref尾端
        self.stick_site = ""  # 拼接點(r1_p2或r2_p1)
        self.f_r_trim = "deprecated_parameter"  # 從尾trim頭部；從頭trim尾部
        self.del_site = "deprecated_parameter"  # del的位置跟長度
        self.in_site = ""  # in的位置跟長度

    def show(self):
        """
        @brief Print the attributes of the Miseq object.
        @return: A string representation of the Miseq object.
        @example {'forword': True, 'stickSiteFinder': 166, 'F_Rtrim': 96, 'del': {45: 6, 173: 96}, 'in': {22: 7}}
        """
        return f'forword: {self.forword}, stickSite(r1_p2,r2_p1): {self.stick_site}, F_Rtrim: {self.f_r_trim}, delSite: {self.del_site}, inSite: {self.in_site}'

    

    # 定義一個方法用來創建初始陣列，長度為原序列長度，初始值皆為0

    # 因為是用ref當中介序列，所以不如直接用ref紀錄接合點位
    # 定義一個方法用產出拼接位點
    def stick_site_finder(self, filename, r, ref, r_who):
        """
        @brief Find the stick site for sequence alignment.
        @param filename: The name of the file.
        @param r: The sequence to be aligned.
        @param ref: The reference sequence.
        @param r_who: The direction of the sequence (r1 or r2).
        @return: The Miseq object with updated attributes.
        """
        # 陣列1：重疊判定陣列
        r_arr_overlap = zero_list_maker(len(ref))  # ref跟r都align了，所以長度是一樣的

        for j in range(0, len(ref)):
            if (r[j] == "-") and (ref[j] == "-"):
                r_arr_overlap[j] = OVERLAP_NONE
            elif (r[j] != "-") and (ref[j] != "-"):
                r_arr_overlap[j] = OVERLAP_BOTH
            elif (r[j] == "-") and (ref[j] != "-"):
                r_arr_overlap[j] = OVERLAP_INSERT
            elif (r[j] != "-") and (ref[j] == "-"):
                r_arr_overlap[j] = OVERLAP_DELETE

        # print("---------------------------")
        # print(r_arr_overlap)
        # print("---------------------------")

        # 直接從r是r1或r2來定義r是起始於ref的左側或右側
        if r_who == "r1":
            # target_direction="start from the left side of reference"
            self.forword = True
        elif r_who == "r2":
            # target_direction="start from the right side of reference"
            self.forword = False

        # 判斷r與ref重疊區域，即找"0"(譬如557~823)
        first_one = r_arr_overlap.index(OVERLAP_BOTH)
        # code從0起算，所以這裡是557的話，bioedit就是第558個bp開始
        r_arr_overlap.reverse()
        last_one = len(r_arr_overlap) - r_arr_overlap.index(OVERLAP_BOTH)
        # code從0起算，所以這裡是823的話，bioedit就也是到第823個bp結束
        r_arr_overlap.reverse()
        # 序列要轉回來，等等還要用
        # print(first_one)
        # print(last_one)
        if r_who == "r1":
            self.stick_site = ["r1_p2", last_one]
        elif r_who == "r2":
            self.stick_site = ["r2_p1", first_one]

        # 最後來算一下ref內indel的位點，之後比對的時候可以用這些位點來trim
        # (code從0起算，所以位點也都從0開始)

        # 判斷ref相對於r的indel片段數及其數量
        self.in_site = {}  # insert片段數
        self.del_site = {}  # delet片段數

        # 看ref
        site_status = OVERLAP_UNKNOWN
        site_number = 0
        indel_start_site = 0
        for j in range(0, len(ref)):
            # 迴圈逐點檢視，判定當前位點是否與下一點相同，
            if (j + 1) != len(ref):
                # 位點非最後一位
                if r_arr_overlap[j] == OVERLAP_INSERT:
                    # insertion
                    if (site_status != OVERLAP_INSERT) and (site_number == 0):
                        # 入口
                        if r_arr_overlap[j] == r_arr_overlap[j + 1]:
                            # 入口但非出口
                            site_status = OVERLAP_INSERT
                            indel_start_site = j
                            self.in_site[j] = 1
                            site_number = site_number + 1
                        elif r_arr_overlap[j] != r_arr_overlap[j + 1]:
                            # 入口即出口(即indel僅為單一位點)
                            # site_status = OVERLAP_INSERT
                            # indel_start_site = j
                            self.in_site[j] = 1
                            # 出口的話要重置
                            site_status = OVERLAP_UNKNOWN
                            site_number = 0
                            indel_start_site = 0
                        else:
                            print("Miseq 107: something wrong. ", filename)
                    elif (site_status == OVERLAP_INSERT) and (site_number != 0):
                        # 非入口
                        if r_arr_overlap[j] == r_arr_overlap[j + 1]:
                            # 非入口且非出口
                            site_number = site_number + 1
                            self.in_site[indel_start_site] = site_number
                        elif r_arr_overlap[j] != r_arr_overlap[j + 1]:
                            # 出口
                            site_number = site_number + 1
                            self.in_site[indel_start_site] = site_number
                            # 出口的話要重置
                            site_status = OVERLAP_UNKNOWN
                            site_number = 0
                            indel_start_site = 0
                        else:
                            print("Miseq 123: something wrong. ", filename)
                    else:
                        print("Miseq 125: something wrong. ", filename)

                elif r_arr_overlap[j] == OVERLAP_DELETE:
                    # deletion
                    if (site_status != OVERLAP_DELETE) and (site_number == 0):
                        # 入口
                        if r_arr_overlap[j] == r_arr_overlap[j + 1]:
                            # 入口但非出口
                            site_status = OVERLAP_DELETE
                            indel_start_site = j
                            self.del_site[j] = 1
                            site_number = site_number + 1
                        elif r_arr_overlap[j] != r_arr_overlap[j + 1]:
                            # 入口即出口(即indel僅為單一位點)
                            # site_status = OVERLAP_DELETE
                            # indel_start_site = j
                            self.del_site[j] = 1
                            # 出口的話要重置
                            site_status = OVERLAP_UNKNOWN
                            site_number = 0
                            indel_start_site = 0
                        else:
                            print("Miseq 147: something wrong. ", filename)
                    elif (site_status == OVERLAP_DELETE) and (site_number != 0):
                        # 非入口
                        if r_arr_overlap[j] == r_arr_overlap[j + 1]:
                            # 非入口且非出口
                            site_number = site_number + 1
                            self.del_site[indel_start_site] = site_number
                        elif r_arr_overlap[j] != r_arr_overlap[j + 1]:
                            # 出口
                            site_number = site_number + 1
                            self.del_site[indel_start_site] = site_number
                            # 出口的話要重置
                            site_status = OVERLAP_UNKNOWN
                            site_number = 0
                            indel_start_site = 0
                        else:
                            print("Miseq 163: something wrong. ", filename)
                    else:
                        print("Miseq 165: something wrong. ", filename)
            # 位點是最後一位
            elif (j + 1) == len(ref):
                if r_arr_overlap[j] == OVERLAP_INSERT:
                    site_number = site_number + 1
                    self.in_site[indel_start_site] = site_number
                elif r_arr_overlap[j] == OVERLAP_DELETE:
                    site_number = site_number + 1
                    self.del_site[indel_start_site] = site_number
                else:  # OVERLAP_BOTH
                    # print ("Miseq 175: something wrong. ",filename)
                    # print(self.stick_site)
                    pass  # 這步代表最後一位r跟ref都有base
        return self
