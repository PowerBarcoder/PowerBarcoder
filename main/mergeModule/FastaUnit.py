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



    """
    get file name from path without extension
    """
    def getFileNameFromPath(path):
        fileName = ""
        if "/" in path:
            fileName = path.split("/")[-1]
        elif "\\" in path:
            fileName = path.split("\\")[-1]
        return ".".join(fileName.split(".")[:-1])


    """
    get file extension from path
    """
    def getFileExtensionFromPath(path):
        extension = ""
        if "/" in path:
            extension = path.split(".")[-1]
        return extension


    """
    Split a fasta with mulitple sequences into seperated file with one line header and one line sequence data.
    Input supported for sequence data with multiple lines (such as the alignment result file in MAFFT).  
    """
    def splitMulitpleSeqFastaIntoFiles(self, loadPath, saveDir):
        fileName = self.getFileNameFromPath(loadPath)
        extension = self.getFileExtensionFromPath(loadPath)
        count = len(open(loadPath).readlines())
        print(count)
        bufferedText = ""
        fileSerialNumber=1
        for i in range(1, count+1):
            text = linecache.getline(loadPath, i)
            x = text.replace("\n", "")
            # print(x)
            if ">" in x and i != 1:  # not first line header
                with open(saveDir+fileName+"_"+str(fileSerialNumber)+"."+extension, "w") as file_edit:
                    file_edit.write(bufferedText)
                    fileSerialNumber+=1
                bufferedText = ""
                bufferedText+=(x+"\n")
            elif ">" in x and i == 1: # first line header
                bufferedText = ""
                bufferedText+=(x+"\n")
            elif ">" not in x and i != count: # not last line seq
                bufferedText+=(x)
            else: # last line seq
                bufferedText+=(x)
                with open(saveDir+fileName+"_"+str(fileSerialNumber)+"."+extension, "w") as file_edit:
                    file_edit.write(bufferedText)
                    fileSerialNumber+=1

    # inputPath = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/raw/KTHU2220_Wade5673_Tectaria_pleiosora_.fas'
    # outputDir = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/'
    # inputPath2 = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/raw/KTHU1778_Liu9858_Cephalomanes_oblongifolium_.fas_r2.al'
    # outputDir2 = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/'

    # splitMulitpleSeqFastaIntoFiles(inputPath2, outputDir2)
