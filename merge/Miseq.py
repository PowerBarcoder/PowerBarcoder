class Miseq:
    # 建構式
    def __init__(self):
        self.forword = ""  # True表示放ref頭端，False表示放ref尾端
        self.stickSite = ""  # ，拼接點(r1_p2或r2_p1)
        self.F_Rtrim = ""  # 從尾trim頭部；從頭trim尾部
        self.delSite = ""  # del的位置跟長度
        self.inSite = ""  # in的位置跟長度

    # 印出物件
    def show(self):
        return f'forword: {self.forword}, stickSite(r1_p2,r2_p1): {self.stickSite}, F_Rtrim: {self.F_Rtrim}, delSite: {self.delSite}, inSite: {self.inSite}' 
    # {'forword': True, 'stickSiteFinder': 166, 'F_Rtrim': 96, 'del': {45: 6, 173: 96}, 'in': {22: 7}}


        #定義一個方法用來創建初始陣列，長度為原序列長度，初始值皆為0 
    def zeroListMaker(self,n):
        listofzeros = [0] * n
        return listofzeros

    #定義一個方法用產出拼接位點
    def stickSiteFinder(self,r,ref):
        # 陣列1：重疊判定陣列
        r_arr_overlap=self.zeroListMaker(len(r))

        # 標記相符位點，相異但有一為"-"者為0，相符者value=1，相異但皆不為"-"者也為1
        for j in range(0,len(r)):
            if (r[j]==ref[j])or((r[j]!="-")and(ref[j]!="-")):
                r_arr_overlap[j]=1
            # elif (r[j]!=ref[j])and(r[j]!="-") and (ref[j]!="-"):
            #     r_arr_overlap[j]=0
        # print("---------------------------")
        # print(r_arr_overlap)
        # print("---------------------------")

        # 判斷序列起始於ref的左側或右側
        if (r[0]!="-")and(r[-1]=="-"):
            target_direction="start from the left side of reference"
            self.forword=True
        elif(r[0]=="-")and(r[-1]!="-"):
            target_direction="start from the right side of reference"
            self.forword=False

        # 判斷r相對於ref的insert片段數及其數量
        self.inSite={} #insert片段數
        self.delSite={} #insert片段數
        
        if (self.forword==True):
            indel_bool=False
            insert_bool=False
            delete_bool=False

        elif(self.forword==False):
            indel_bool=True
            insert_bool=False
            delete_bool=True
            position=0

        insert_sites_index=1
        delete_sites_index=1
            
        for j in range(0,len(r)):
            # 從候選陣列進入序列
            if ((j+1)!=len(r)):
                # 迴圈逐點檢視，判定當前位點是否與下一點相同
                # 最後一位不比
                if ((r_arr_overlap[j]!=r_arr_overlap[j+1])):
                    # 不同時
                    # 出現符號轉變，"...10..."為進入indel區的起點，"...01..."為終點
                    indel_bool=not indel_bool
                    if (indel_bool==True)and(ref[j+1]=="-") and (r[j+1]!="-"):
                        # 進入indel區內的in
                        insert_bool= True
                    elif (indel_bool==True)and(ref[j+1]!="-") and (r[j+1]=="-"):
                        # 進入indel區內的del
                        delete_bool= True
                    elif (indel_bool==False):
                        # 離開indel區
                        insert_bool= False
                        delete_bool= False 
                        insert_sites_index=1
                        delete_sites_index=1

                    # 紀錄當前位點
                    position=j+1
                    position+=0
                    
                else:
                    # 相同時
                    if delete_bool==True:
                        delete_sites_index+=1
                        self.delSite[position]=delete_sites_index
                    elif insert_bool==True:
                        insert_sites_index+=1
                        self.inSite[position]=insert_sites_index
        # print("從x位點往後算有y個")
        # print("del:",self.delSite)
        # print("in:",self.inSite)

        # 判斷接合點位置
        self.F_Rtrim=0
        if (self.forword==True):
            self.stickSite=list(self.delSite.keys())[-1]
            # self.stickSite要減掉r的insertion，才是real位點
            for key in self.inSite:
                self.stickSite=self.stickSite-self.inSite[key]
                # trim=trim+self.inSite[key]
            self.F_Rtrim=self.F_Rtrim+self.delSite[list(self.delSite.keys())[-1]]
        elif (self.forword==False):
            self.stickSite=self.delSite[0]+1
            # trim=trim+self.delSite[0]
            # self.stickSite直接取delete第一個key的value+1即可
            self.F_Rtrim=self.F_Rtrim+self.delSite[0]

        # print("target_direction=",target_direction,"\ntarget_del=",self.delSite,"\ntarget_in=",self.inSite,"\nself.stickSite on reference=",self.stickSite)
        # print("------------------------------------------------------")
        
        # result_dict={"forword":forword,"self.stickSite":self.stickSite,"self.F_Rtrim":self.F_Rtrim,"del":self.delSite,"in":self.inSite}

        return self