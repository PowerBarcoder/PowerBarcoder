# 直接用NCBI的fasta即可，這裡會轉出edit版，再用edit版生成seqID&seqlist

import linecache


class FastaUnit:

    def __init__(self):
        self.seqMap = {}

    # 把fasta存成一行一行的檔案
    def saveFastaUnitAsFile(self, loadPath, saveDir):
        file = loadPath
        fileName = ""
        if "/" in file:
            fileName = file.split("/")[-1]
        elif "\\" in file:
            fileName = file.split("\\")[-1]

        count = len(open(file).readlines())
        for i in range(1, count+1):
            text = linecache.getline(file, i)
            x = text.replace("\n", "")
            # print(x)
            with open(saveDir+fileName, "a") as file_edit:
                if ">" in x and i != 1:
                    file_edit.write("\n"+x+"\n")
                elif ">" in x and i == 1:
                    file_edit.write(x+"\n")
                else:
                    file_edit.write(x)

    # 把fasta轉成一行一行的map物件

    def fastaUnit(self, loadPath):
        seqMap = {}
        # 製作所有序列的map
        seqHeader = ""
        seqRead = ""
        count = len(open(loadPath).readlines())
        for i in range(1, count+1):
            text = linecache.getline(loadPath, i)
            x = text.replace("\n", "")
            # 不是第一行的header
            if ">" in x and i != 1:
                seqHeader = x
                seqRead = ""
            # 第一行的header
            elif ">" in x and i == 1:
                seqHeader = x
                seqRead = ""
            else:
                seqRead = seqRead+x
                seqMap[seqHeader] = seqRead
            # seqMap = dict(zip(seqHeader, seqRead))
        self.seqMap = seqMap
        return self
