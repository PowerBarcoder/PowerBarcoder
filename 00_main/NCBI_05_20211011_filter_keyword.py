#完成版，要找蕨類的請至/Polypodiopsida/

import linecache as lc
from numpy.lib.shape_base import split
import pandas as pd
import csv
from os import path,listdir

Load_file_dir="C:/PYTHON/Download_Seq_files/gb_csv/keyword/total/"
Save_file_dir1="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Spermatophyta/"
Save_file_dir2="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Bryophyta/"
Save_file_dir3="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Polypodiopsida/"
Save_file_dir4="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Lycopodiopsida/"
Save_file_dir5="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Marchantiophyta/"
Save_file_dir6="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Other/"
#Other：

filename=[]

files = listdir(Load_file_dir)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = Load_file_dir + f
  # 判斷 fullpath 是檔案還是目錄
  if path.isfile(fullpath):
    #print("檔案：", f)
    filename.append(f)
  #elif isdir(fullpath):
    # print("目錄：", f)#這裡不需要，因為不是夾中夾
#print(filename)
#現在有gb file的檔案清單"filename"了
checking_file_list=[]
x=0
#checked_num=0
#fitted_num=0
for i in filename:
  with open(Load_file_dir+i,"r") as file:
      #checked_num=checked_num+1
      #x=x+1
      file_content=str(file.readlines())
      #print(type(file_content))
      if "Spermatophyta" in file_content:
        with open(Save_file_dir1+i,"w") as file1:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file1.write(text)
      elif "Bryophyta" in file_content:
        with open(Save_file_dir2+i,"w") as file2:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file2.write(text)
      elif "Polypodiopsida" in file_content:
        with open(Save_file_dir3+i,"w") as file3:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file3.write(text)
      elif "Lycopod" in file_content:
        with open(Save_file_dir4+i,"w") as file4:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file4.write(text)
      elif "Marchantiophyta" in file_content:
        with open(Save_file_dir5+i,"w") as file5:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file5.write(text)
      else:
        checking_file_list.append(i)#可以檢查出被遺漏的都是誰
        with open(Save_file_dir6+i,"w") as file6:
            text=lc.getline(Load_file_dir+i,1)+lc.getline(Load_file_dir+i,2)
            file6.write(text)
        

  #if x>10:
    #break
print(checking_file_list)

"""
"other"裡面有細菌的序列
['KP424367_gb.csv', 'LK000046_gb.csv', 'LK000877_gb.csv', 'LK002336_gb.csv', 'LK010644_gb.csv', 'LK011770_gb.csv', 'LK018738_gb.csv', 'LK019828_gb.csv', 'LK932316_gb.csv', 'LK932325_gb.csv', 'LK932463_gb.csv', 'LK932524_gb.csv', 'LK932816_gb.csv', 'LK932949_gb.csv']
"""