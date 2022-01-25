#!/usr/bin/python
# -*- coding: utf-8 -*-
#csv to lost
#https://www.kite.com/python/answers/how-to-read-columns-from-a-csv-file-to-lists-in-python
#取交集
#https://www.itread01.com/content/1543751226.html
#基礎set運算
#https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists


import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

filename=[]
#好了我們開始把檔名讀進本py的list裡
seqN=[]
#順便紀錄一下每次合併後有幾條，可以畫個折線圖

#指定要列出所有檔案的目錄跟整理完檔案的目錄
Load_file_dir="C:/PYTHON/Download_Seq_files/acclist/"
Save_file_dir="C:/PYTHON/Download_Seq_files/"
#取得所有檔案與子目錄名稱
files = listdir(Load_file_dir)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑，這裡join用得還不錯
  fullpath = join(Load_file_dir, f)
  # 判斷 fullpath 是檔案還是目錄
  if isfile(fullpath):
    #print("檔案：", f)
    filename.append(f)
  #elif isdir(fullpath):
    # print("目錄：", f)#這裡不需要，因為不是夾中夾
#print(filename)


#開始把檔案一個一個讀近來比較裡面的accID有沒有重複
with open(Save_file_dir+"union.csv","w")as file:
    file.write("")
for i in filename:
    column_names = ["", "accession"]
    df = pd.read_csv(Save_file_dir+"union.csv", names=column_names)
    #print(df)
    AccID = df.accession.to_list()
    template=AccID[1:]
    #print(template)
    #i裡面的text是dataframe，所以得用pd
    df1 = pd.read_csv(Load_file_dir+i, names=column_names)
    AccID1= df1.accession.to_list()#把叫accseeion的col轉成list
    compare=AccID1[1:]
    #print(compare)
    result=set(template).union(compare)
    #print(result)
    num=len(result)
    print(num)
    seqN.append(num)
    #print(seqN)
    result_x = pd.DataFrame(result).rename(columns = {0:'accession'})
    result_x.to_csv(Save_file_dir+"union.csv")

#畫圖
#https://newaurora.pixnet.net/blog/post/227933636-python-%E4%BD%BF%E7%94%A8matplotlib%E7%95%AB%E6%8A%98%E7%B7%9A%E5%9C%96%28line-chart%29
# import matplotlib相關套件
import matplotlib.pyplot as plt
# 使用月份當做X軸資料
BLASTnumber=list(range(0,213))
x=BLASTnumber
y=seqN
# 設定圖片大小為長15、寬10
plt.figure(figsize=(5,5),dpi=100,linewidth = 2)
# 把資料放進來並指定對應的X軸、Y軸的資料，用方形做標記(s-)，並指定線條顏色為紅色，使用label標記線條含意
plt.plot(x,y,'s-',color = 'r', label="No. of accID")
# 設定圖片標題，以及指定字型設定，x代表與圖案最左側的距離，y代表與圖片的距離
plt.title("you can type what you want",  x=0.5, y=1.03)
# 设置刻度字体大小
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# 標示x軸(labelpad代表與圖片的距離)
plt.xlabel("How many item I BLAST", fontsize=10, labelpad = 15)
# 標示y軸(labelpad代表與圖片的距離)
plt.ylabel("No. of accID", fontsize=10, labelpad = 20)
# 顯示出線條標記位置
plt.legend(loc = "best", fontsize=10)
# 畫出圖片
plt.show()


#小練習
#t = [1, 2, 3, 1, 2, 5, 6, 7, 8]
#list(set(t))
#s = [1, 2, 3]
#result=list(set(t) - set(s))
#print(result)