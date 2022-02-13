# 修改自NCBI_00_20211007_05read_fasta_by_line_testo.py
# 主要用來排seq為一列
#直接用NCBI的fasta即可，這裡會轉出edit版，再用edit版生成seqID&seqlist

from importlib.resources import path
import linecache
import os

############################當前路徑及py檔名################################
path, filename = os.path.split(os.path.abspath(__file__))
# print(path)
# print(filename)
############################當前路徑及py檔名################################

seqID=[]
seqlist=[]

Load_file_dir=path+"\\"
file=Load_file_dir+"sequence.fasta"
count=len(open(file).readlines())
print(count)
for i in range(1,count):
    text = linecache.getline(file,i)
    x=text.replace("\n","")
    #print(x)
    with open(Load_file_dir+"sequence.fasta_edit.fas","a") as file_edit:
        if ">" in x and i!=1:
            file_edit.write("\n"+x+"\n")
        elif ">" in x and i==1:
            file_edit.write(x+"\n")
        else:
            file_edit.write(x)
#產出的sequence.fasta_edit.fas是一行名一行序列的格式了
   
count_new=len(open(Load_file_dir+"sequence.fasta_edit.fas").readlines())
print(count_new)


# 取accID及accSEQ
#行數從第1行算起，但迴圈從0算起
for i in range(0,1000000):
    if i==0:
        continue
    odd=2*i-1
    even=2*i
    ID = linecache.getline(Load_file_dir+"sequence.fasta_edit.fas",odd)
    #抓完之後針對seqID再清理遺下
    #如：ID="Pteridaceae_Cheilanthoideae_Hemionitis_MH173072"
    ID1=(ID[(ID.find(">")+1):(ID.find(">")+9)]+"\n")
    
    """
    #print(ID1)
    #變這個：_Cheilanthoideae_Hemionitis_MH173072
    ID1site=ID1.find("_")
    #print(ID1site)
    print("-------------------------")
    while int(ID1site)>-1:
        ID1=(ID1[(ID1site+1):])
        ID1site=ID1.find("_")
        print(ID1site)
        print(ID1)
    #清理完畢
    """

    seqID.append(ID1)
    SEQ= linecache.getline(Load_file_dir+"sequence.fasta_edit.fas",even)
    #print(SEQ)
    seqlist.append(SEQ)
    if (i*2)> count_new:
        break
#print(seqID)
#print(seqlist)


with open(Load_file_dir+"seqID_sequence.fasta_edit.csv","w")as file1:
    for ele in seqID:
        file1.write(ele)

with open(Load_file_dir+"seqlist_sequence.fasta_edit.csv","w")as file2:
    for ele in seqlist:
        file2.write(ele)


# # 接著把一個fas檔分成多個fas檔
# for i in range(0,1000000):
#     if i==0:
#         continue
#     odd=2*i-1
#     even=2*i
#     ID = linecache.getline(Load_file_dir+"sequence.fasta_edit.fas",odd)
#     #抓完之後針對seqID再清理遺下
#     #如：ID="Pteridaceae_Cheilanthoideae_Hemionitis_MH173072"
#     ID1=(ID[(ID.find(">")+1):(ID.find(">")+9)]+"\n")

#     seqID.append(ID1)
#     SEQ= linecache.getline(Load_file_dir+"sequence.fasta_edit.fas",even)
#     #print(SEQ)
#     seqlist.append(SEQ)
#     if (i*2)> count_new:
#         break

#     with open(Load_file_dir+"seqlist_sequence.fasta_edit.csv","w")as file2:
#         for ele in seqlist:
#             file2.write(ele)


    
print("原有648條序列，但是AB196364有兩個，所以只有647條")
