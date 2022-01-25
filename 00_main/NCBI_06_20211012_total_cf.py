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
Load_file_dir_z="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Polypodiopsida/"

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

filename_z=[]
files = listdir(Load_file_dir_z)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = Load_file_dir_z + f
  # 判斷 fullpath 是檔案還是目錄
  if path.isfile(fullpath):
    #print("檔案：", f)
    filename_z.append(f[:-7])
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

#x=kuofile=7646
#y=testo=9026
#z=keyword=12683

#xy交集，共有項
intersection_xy=set(filename_x)&set(filename_y)
#print(intersection_xy)
print(len(intersection_xy))#7224

#yz交集，共有項
intersection_yz=set(filename_y)&set(filename_z)
#print(intersection_yz)
print(len(intersection_yz))#9007

#xz交集，共有項
intersection_xz=set(filename_x)&set(filename_z)
#print(intersection_xz)
print(len(intersection_xz))#7617

#xy聯集，所有項
union_xy=set(filename_x)|set(filename_y)
#print(union_xy)
print(len(union_xy))#9448

#yz聯集，所有項
union_yz=set(filename_y)|set(filename_z)
#print(union_yz)
print(len(union_yz))#12702

#xz聯集，所有項
union_xz=set(filename_x)|set(filename_z)
#print(union_xz)
print(len(union_xz))#12712


#-------------------------------------------
#x獨有
diff_x_yz=set(filename_x)-set(union_yz)
#print(diff_x_yz)
print(len(diff_x_yz))#10
#{'FJ746564', 'KF006816', 'AF182359', 'FJ746566', 'FJ746567', 'MH229475', 'FJ746565', 'AF182358', 'FJ746568', 'MG969439'}

#y獨有
diff_y_xz=set(filename_y)-set(union_xz)
#print(diff_y_xz)
print(len(diff_y_xz))#0

#z獨有
diff_z_xy=set(filename_z)-set(union_xy)
#print(diff_z_xy)
print(len(diff_z_xy))#3264

#xyz交集，共有項
intersection_xyz=set(filename_y)&set(filename_x)&set(filename_z)
#print(intersection_xyz)
print(len(intersection_xyz))#7205

#xyz聯集
union_xyz=set(filename_x)|set(filename_y)|set(filename_z)
#print(union_xyz)
print(len(union_xyz))#12712


#xyz中xy獨有
diff_xyz_xy=set(intersection_xy)-set(filename_z)
#print(diff_xyz_xy)
print(len(diff_xyz_xy))#19

#xyz中xz獨有
diff_xyz_xz=set(intersection_xz)-set(filename_y)
#print(diff_xyz_xz)
print(len(diff_xyz_xz))#412

#-------------------------------------------





#xy中x獨有
diff_x_y=set(filename_x)-set(filename_y)
#print(diff_x_y)
print(len(diff_x_y))#422

#xy中y獨有
diff_y_x=set(filename_y)-set(filename_x)
#print(diff_y_x)
print(len(diff_y_x))#1802










