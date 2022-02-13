import linecache as lc
from numpy.lib.shape_base import split
import csv
import os 

#請先新建gb_csv資料夾
#要做自己切目錄

path, filename = os.path.split(os.path.abspath(__file__))
Load_file_dir=path+"\\acclist\\"
Save_file_dir=path+"\\gb_csv\\"


filename=[]
files = os.listdir(Load_file_dir)
# 以迴圈處理
for f in files:
  # 產生檔案的絕對路徑
  fullpath = Load_file_dir + f
  # 判斷 fullpath 是檔案還是目錄
  if os.path.isfile(fullpath):
    #print("檔案：", f)
    filename.append(f)
  #elif isdir(fullpath):
    # print("目錄：", f)#這裡不需要，因為不是夾中夾
#print(filename)
#現在有gb file的檔案清單"filename"了

#開始處理gb to dict to csv

# for item in filename:
for item in filename[0:1]:
    cate={}
    #print("----------------------")
    Line_name=0
    Line_text=""
    for i in range(1,100000):
        x=lc.getline(Load_file_dir+item,i)
        x=x[:-1]

        if "ORIGIN  " in x[0:10]:#迴圈停在序列前，必須有1:10，不然有些文章標題有origin也會被砍
            break  

        elif "FEATURES  " in x[0:10]:#處理annotation欄
            while "  " in x:#取代多空格為單空格
                x=x.replace("  "," ")
            while " " in x[:2]:#去除首字之單空格
                x=x.replace(" ","",1)
            key=x[:x.find(" ")]
            value=x[(x.find(" ")+1):-1]
            Line_name=key
            #print(Line_name)
            #print("----------------------")
            Line_text=value+" "
            j=i+1

            while "ORIGIN" not in lc.getline(Load_file_dir+item,j):
                y=lc.getline(Load_file_dir+item,j)
                if "     " in y:#有子key(source跟misc_feature)
                    while "  " in y:#取代多空格為單空格
                        y=y.replace("  "," ")
                    #while " " in y[:2]:#去除首字之單空格
                        #y=y.replace(" ","",1)
                    key_y=y[:y.find(" ")]
                    value_y=y[(y.find(" ")+1):-1]
                    Line_name_y=key_y
                    Line_text=Line_text+Line_name_y+value_y+" "
                else:#沒有子key
                    while "  " in y:#取代多空格為單空格
                        y=y.replace("  "," ")
                    #while " " in y[:2]:#去除首字之單空格
                        #y=y.replace(" ","",1)
                    value_y=y[:-1]
                    Line_text=Line_text+value_y+" "
                j=j+1
            cate.update({Line_name:Line_text})#開始加到字典裡
            break    
            

        elif "    " not in x[:5]:#for 母title及子title
            Line_text=""
            
            #print("line%s"%i,"solA")
            while "  " in x:#取代多空格為單空格
                x=x.replace("  "," ")
            while " " in x[:2]:#去除首字之單空格
                x=x.replace(" ","",1)
            
            key=x[:x.find(" ")]
            #print(type(key),"：",key)
            value=x[(x.find(" ")+1):]
            #print(type(value),"：",value)
            
            key_num=0#幫重複的key編號
            while key in cate.keys():
                key_num=key_num+1
                key=key+str(key_num)
            cate.update({key:value})#開始加到字典裡
            Line_name=key
            #print(Line_name)
            #print("----------------------")
            
            Line_text=value+" "
            
        elif "      " in x[:6] :#for無title子項
            #print("line%s"%i,"solB")
            while "  " in x:#取代多空格為單空格
                x=x.replace("  "," ")
            while " " in x[:2]:#去除首字之單空格
                x=x.replace(" ","",1)
            key=Line_name
            #print(type(key),"：",key)
            value=Line_text+x+" "#字串尾幫加空格，這樣下一個接來的時候可以有換行變空格的效果
            Line_text=value
            #print(type(value),"：",value)
            cate.update({key:value})#開始加到字典裡    
            #print("----------------------")

        
        else:#for "source" and "misc_feature"
            print(item,"line%s"%i,"solC")

    #print (cate)

    #下一步，把dict變成表格，然後個檔案合併
    #先不逐個儲存，因為說不定執行速度很快，不需要額外檔案支援除錯

    #print(cate.values())

    #dict直接可讀，不需要你們了
    #test=str(cate.keys())[11:-2]
    #test_list=test.split(",")
    #print(type(test_list))


    # 經查，cate=sorted(cate.items(), key=lambda x:x[1])好像是多餘的
    # print(cate)
    # cate=sorted(cate.items(), key=lambda x:x[1])
    #  d.items() 为待排序的对象；key=lambda x: x[1] 为对前面的对象中的第二维数据（即value）的值进行排序
    # print(cate)

    lable=cate.keys()
    text=cate.values()
    with open(Save_file_dir+item[:-3]+"_gb.csv","w",newline='',encoding='UTF-8') as file:
        #newline=''指定換行符號，沒加的話row之間會多一row
        writer=csv.writer(file)
        writer.writerow(lable)#把列名先填上
        writer.writerow(text)




