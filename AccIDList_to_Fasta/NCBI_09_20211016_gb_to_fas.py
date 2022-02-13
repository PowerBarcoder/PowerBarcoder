import linecache as lc
from numpy.lib.shape_base import split
import pandas as pd
import csv
import os 

path, filename = os.path.split(os.path.abspath(__file__))
Load_file_1=path+"/acclist/"
open_file_list=[Load_file_1]
Save_file_1=path+"/fasta/fasta_20220214_rbcl.fas"
Save_file_list=[Save_file_1]


for List,Save in zip(open_file_list,Save_file_list):
  file_fasta=""
  filename=[]
  files = os.listdir(List)
  # 以迴圈處理
  for f in files:
    # 產生檔案的絕對路徑
    fullpath = List + f
    # 判斷 fullpath 是檔案還是目錄
    if os.path.isfile(fullpath):
      #print("檔案：", f)
      filename.append(f)
    #elif isdir(fullpath):
      # print("目錄：", f)#這裡不需要，因為不是夾中夾
  #print(filename)
  #現在有gb file的檔案清單"filename"了

  for item in filename:
    sp_seq=""
    for i in range(1,100000):
        x=lc.getline(List+item,i)
        if "ORIGIN     " in x:
          while len(x)>1:
            x=lc.getline(List+item,i+1)[10:-1]
            if "Expand Ns" in x:
              x=x[(x.find("[gap ")+5):(x.find(" bp]"))]
              y=""
              for r in range(0,int(x)):
                y=y+"n"
              x=y
              print(List,item,y)
              #經查，NNNNN於kuofile、testo、keyword三夾內，
              #有以Expand呈現者，亦有以NNNNNNNN呈現者，
              #如AM689690即於kuofile、testo以NNNNNN呈現，於keyword以Expand呈現
            i=i+1
            sp_seq=sp_seq+x
          sp_seq=sp_seq.replace(" ","")
          #print(sp_seq) 
        elif "  ORGANISM  " in x:
          sp_name=x[12:-1]
          sp_name=sp_name.replace(" ","_")
        elif "ACCESSION   " in x:
          sp_accID=x[12:-1]
        elif len(x)<3:
          break
        #elif "//" in x:
          #遇到JOURNAL提供URL的，
          #如LC004375:http://www.krbali.lipi.go.id
          #就會提前結束迴圈，讀不到序列了
        #else:
          #print("something wrong in ",i)
    file_fasta=file_fasta+">"+sp_name+"_"+sp_accID+"\n"+sp_seq.upper()+"\n"
  #print(file_fasta)

  with open(Save,"w")as file:
    file.write(file_fasta)


