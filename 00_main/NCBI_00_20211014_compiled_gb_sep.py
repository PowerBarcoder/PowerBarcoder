import linecache

seqID=[]
seqlist=[]
Load_file_dir="C:/PYTHON/Download_Seq_files/"
Save_file_dir="C:/PYTHON/Download_Seq_files/genbank/"
file=Load_file_dir+"keyword.gb"

#with open(file,"r") as file_raw:
    #file_raw.read()
num=0
for i in range(1,1000000000000000):
    text = linecache.getline(file,i)
    if "LOCUS  " in str(text):
        name=text[12:20]
        with open(Save_file_dir+name+".gb","a") as file_save:
            file_save.write(text)
        i=i+1    
        continue
    elif len(str(text)) >=2:            
        if "//"in text[0:3]:#處理多出的最後一行空白
            with open(Save_file_dir+name+".gb","a") as file_save:
                file_save.write(text[:-1])
        else:
            with open(Save_file_dir+name+".gb","a") as file_save:
                file_save.write(text)
        i=i+1
    num=num+1
    if num>661877:
        break
        


"""
text = linecache.getline(file,2)
print(text)
count=len(open(file).readlines())

#行數從第1行算起，但迴圈從0算起
for i in range(0,1000000):
    if i==0:
        continue
    odd=2*i-1
    even=2*i
    ID = linecache.getline(file,odd)
    #抓完之後針對seqID再清理遺下
    #如：ID="Pteridaceae_Cheilanthoideae_Hemionitis_MH173072"
    ID1=(ID[((ID.find("aceae"))+5):])
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
    seqID.append(ID1)
    SEQ= linecache.getline(file,even)
    #print(SEQ)
    seqlist.append(SEQ)
    if (i*2)> count:
        break
#print(seqID)
#print(seqlist)


with open(Load_file_dir+"seqID.csv","w")as file1:
    for ele in seqID:
        file1.write(ele)

with open(Load_file_dir+"seqlist.csv","w")as file2:
    for ele in seqlist:
        file2.write(ele)
"""

