#kuofile做完之後拿testo的2000多條來比

#集合寫法
#https://wenyuangg.github.io/posts/python3/python-set.html
import linecache as lc
from numpy.lib.shape_base import split
import pandas as pd
import csv
from os import path,listdir

Load_file_dir_x="C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/"
Load_file_dir_y="C:/PYTHON/Download_Seq_files/gb_csv/testo_total/Polypodiopsida/"
Save_file_dir=""

filename_x=[]
files = listdir(Load_file_dir_x)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = Load_file_dir_x + f
  # 判斷 fullpath 是檔案還是目錄
  if path.isfile(fullpath):
    #print("檔案：", f)
    filename_x.append(f[:-7])
  #elif isdir(fullpath):
    # print("目錄：", f)#這裡不需要，因為不是夾中夾
#print(filename)
# "C:/PYTHON/Download_Seq_files/gb_csv/Polypodiopsida/"有7646個檔
#現在有Polypodiopsida的檔案清單"filename"了

filename_y=[]
files = listdir(Load_file_dir_y)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = Load_file_dir_y + f
  # 判斷 fullpath 是檔案還是目錄
  if path.isfile(fullpath):
    #print("檔案：", f)
    filename_y.append(f[:-7])
  #elif isdir(fullpath):
    # print("目錄：", f)#這裡不需要，因為不是夾中夾
#print(filename)
# "C:/PYTHON/Download_Seq_files/gb_csv/Polypodiopsida/"有7646個檔
#現在有Polypodiopsida的檔案清單"filename"了
#接著要來把csv合併起來，
#應該得用pd了



"""
a=[1,3,5]
b=[1,2,3]
set(a) - set(b)
set([5])
"""

#kuofile=7646
#testo=9026

#x獨有
diff_xy=set(filename_x)-set(filename_y)
#print(diff_xy)
print(len(diff_xy))#422

#y獨有
diff_yx=set(filename_y)-set(filename_x)
#print(diff_yx)
print(len(diff_yx))#1802

#聯集，所有項
union_yx=set(filename_y)|set(filename_x)
#print(union_yx)
print(len(union_yx))#9448

#交集，共有項
intersection_yx=set(filename_y)&set(filename_x)
#print(intersection_yx)
print(len(intersection_yx))#7224