#跑完第一輪後可以再跑一次補缺的，通常一次就可以補齊

#關閉driver視窗的三種方法
#https://stackoverflow.com/questions/15067107/difference-between-webdriver-dispose-close-and-quit

# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import sys
import os
import requests
import urllib.request
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

Load_file_dir="C:/PYTHON/Download_Seq_files/"
Save_file_dir="C:/PYTHON/Download_Seq_files/acclist/"

for i in range(1,2):#881被切成五個檔案，每個檔裡的seq都要BLAST
    seqID=[]
    seqlist=[]
    #input("確定要執行?")
    with open(Load_file_dir+"seqID_testo_%s_edit.csv"%i,"r")as file:
        for line in file:
            seqID.append(line[:-1])
        #print(seqID)#ok，成功印出
    with open(Load_file_dir+"seqlist_testo_%s_edit.csv"%i,"r")as file:
        for line in file:
            seqlist.append(line[:-1])
        #print(seqlist)
    """
    seqID1="Deparia_trnL_F"
    seqID2="Isoetes_trnL_F"
    seq1="GTGACACGAGGATTTTCAGTCCTCTGCTCTACCGACTGAGCTATCTCGGCCGACTCATTCACAGATAAAACTCAACTAGAAATCGGTGAAGTTTATTTTTCAACTCCAGCTTTTTGCCCAGTCAAACAAACCGTTGATCCCGCCTTTATCGATCTGCTTAATACAATACCGCCTTCAGCAAATAAAGTCTGGAGGGGGAGGGGGCTCGATTGAGCCATTCATGGATATTAAAATACCGAATGGCTCACTTGCAAAGTGTTTCGGAAATACCAAGTAGAAAAAAGAGTTGAAGTGGTTTCCGTATTTCGCTTACGAGCAAATTGTGTGAATCCAAACAACTTGAAATGGGTTAATTAAAGTGTCTCATTGGGGATAGAGGGACTCGAACCCTCACGGTCCTGTGAAACCAACGGATTTTCGTTCCACCGCAACTTGCGCCGCTACTTCTCATTTTACCAAGTGCGTGGAGTGGGACTCTACCTCCATTCACGGAAGTATCATTTTTTGCCACCGGCTCGCTTGCTGAATAATTTTCATTGGAACAGAGTGGGATCCCACAGCAGGTAAGAGGGGAATATGCGGACTAGCAATAGTGGAAGGAATCTACTTTGTGTTACATTACTAAGTACGAACAGAATTTCGTGAATGAGTGCTGGCCCCAAACCGAGAGGTCCGCGTCCGATTGAAGAAAGAATTGAAATTTTGATTCTTTACCAGGTCTCAGTATTATACTTCTACATATTACCTCATGCAGTTAACCACGCGAAACAGTTAGATATTCAGTTATTTCGAGAACTAGTAACTAACAGACTGCTCGTTGGAATGGCCCCCGTCGAGTCTCTGCACCTATCTTGCCTCATTGCCCGAAATTCATTTGAATAATACAAGATT"
    seq2="TGAGCCTTAATATAGGANCTTAACTAAGTGATAGCTTTCAGATTCAGGGAAACCTCGGTGGAAACAATAGGCAATCCTGAGCCAAATTCCGTTGTTTCATTTCATGAACGAACGGGATAGGTGCAGAGACTCGATGGAAGCTATCCCAACGAGTGATCCTCAATACCGTATCTATGAAATAAATCATATAGATATGAATTATATGATATAATGTTTCATCTATTCCTGAAGAGGAAGAAGTGAAAGATACTATCATAGATCATACTCAGATCATGTTATTGTTTGATCAATAATAAGATGCTTAAGTTGATTTAAAATTCGAGGGTCATTCATCATTCAATATATTTATTTTTCTAAAAGATATCTATTATCTAATATCTAACGGATCAATCTTATAGTGGATGATTGGACGAGGTTAAAGATAGAGTCCGATTTTACATGCTAATATCAGCAACAATGTGAATTGTAGTAAGGAGAAAATCCGTTGGCTTTATAGGCCGTGAGGGTTCAAGTCCCTCTATCCTCAGAGAAAGTTTGATTTATTCCAAATTAAATATCCAATTCAATATTGGGATTTAATCTTTCGGTGGAAAAAATTCCCACAGCTATAGTAGGGAATAGCCAACA"
    seqID=[seqID1,seqID2]
    seqlist=[seq1,seq2]
    #input("好了嗎?")
    """
    #KX656159.1，Deparia trnL-F
    #AY651835.1，Isoetes trnL-F

    #製作先前已完成之目錄
    filename_done=[]
    #好了我們開始把檔名讀進本py的list裡
    #指定要列出所有檔案的目錄跟整理完檔案的目錄
    #取得所有檔案與子目錄名稱
    files = listdir(Load_file_dir+"acclist/"+"20211013_testo_%s/"%i)
    # 以迴圈處理
    for f in files:
        # 產生檔案的絕對路徑，這裡join用得還不錯
        fullpath = Load_file_dir +"acclist/"+"20211013_testo_%s/"%i + f
        # 判斷 fullpath 是檔案還是目錄
        if isfile(fullpath):
            #print("檔案：", f)
            filename_done.append(f)
        #elif isdir(fullpath):
            # print("目錄：", f)#這裡不需要，因為不是夾中夾
    print(filename_done)


    filename=[]#本次完成之目錄
    #開始進迴圈
    for seq,ID in zip(seqlist,seqID):
        #ID_for_file_name=ID+"_2021-10-13.csv"#以ID為名的檔名會長這樣
        #為了不讓時間戳記影響判讀，我們不使用原檔名，只取其中的ID，filename_done也轉換成str
        if ID in str(filename_done) :#如果該ID已做則跳過本圈進下圈
            #print(ID," have been done")
            
            #第二輪要補檔名的時候再寫這三行
            #localtime = time.localtime()
            #ptime = time.strftime("%Y-%m-%d" , localtime)
            #filename.append(("%(name1)s_%(name2)s.csv"%({"name1":ID,"name2":ptime})))
            
            continue
        else:#如果該ID未做則進圈
            #print(ID,"haven't been done")
            try:
                url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome"
                PATH="C:/Users/123/Desktop/coding/chromedriver_win32/chromedriver.exe"
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                #'excludeSwitches'底下可設'enable-logging'
                #目的是禁止在terminal印出log(日誌)，
                #這樣就不會每次driver開啟就堆出好幾行字
                driver = webdriver.Chrome(PATH,options=options)
                driver.get(url)
                #輸序列
                search1=driver.find_element_by_xpath('//*[@id="seq"]')
                search1.click()
                search1.send_keys(seq)
                #把滑輪滾到最下面，測試後1000差不多
                #https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/479345/
                js1000="var action=document.documentElement.scrollTop=1000"
                driver.execute_script(js1000)
                time.sleep(3)#不休不行
                #按進階選項，然後下拉一段
                more_search=driver.find_element_by_xpath('//*[@id="btnDescrOver"]')
                more_search.click()
                js1100="var action=document.documentElement.scrollTop=1100"
                driver.execute_script(js1100)
                time.sleep(3)#不休不行
                #資料呈現筆數1000
                sort=driver.find_element_by_xpath('//*[@id="NUM_SEQ"]')
                #print(sort)######
                sort.click()
                time.sleep(2)
                sort1000 = driver.find_element_by_xpath('//*[@id="NUM_SEQ"]/option[6]')
                sort1000.click()
                Click_any = driver.find_element_by_xpath('//*[@id="expectHelp"]/i')
                Click_any.click()
                #往下拉然後BLAST
                js1500="var action=document.documentElement.scrollTop=1500"
                driver.execute_script(js1500)
                time.sleep(3)#不休不行
                BLAST = driver.find_element_by_xpath('//*[@id="blastButton2"]/input')
                BLAST.click()
                time.sleep(10)
                #從結果頁弄RID出來
            
                try:
                    RID= driver.find_element_by_xpath('//*[@id="hsum"]/div[1]/dl/dd[2]/a')
                except:
                    #print("------------------fail-------------------")
                    time.sleep(50)
                    RID= driver.find_element_by_xpath('//*[@id="hsum"]/div[1]/dl/dd[2]/a')
                #print("--------------------------------")
                #print("本次blast序號為",RID.text)
                RIDtext=RID.text
                #print("--------------------------------")
                RIDurl="https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&RID=%s&FORMAT_TYPE=CSV&FORMAT_OBJECT=Alignment&DESCRIPTIONS=1000&ALIGNMENT_VIEW=Tabular&CMD=Get"%RIDtext
                accID=[]
                #試過之後發現，大概要90BLAST才會存取不了NCBI網頁，其他之前失誤的應該只是等不夠久而已
                #整理accession number的fun.
                for line in urllib.request.urlopen(RIDurl):
                    #print (line)發現是二進制編碼
                    linestr=line.decode("utf-8") 
                    #print(type(linestr))發現變str了
                    if len(linestr)>=10:
                        linelist=linestr.split(',')
                        #print(type(linelist))發現變list了
                        try:
                            accessionID=linelist[1]
                            #print(accessionID)#發現成功印出accession number了
                            accID.append(accessionID)
                            #讚歐
                        except:
                            pass
                    #print("---------------------------")
                
                accID_x = pd.DataFrame(accID).rename(columns = {0:'accession'})
                localtime = time.localtime()
                #result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
                ptime = time.strftime("%Y-%m-%d" , localtime)
                #print(ptime)
                accID_x.to_csv(Save_file_dir+"20211013_testo_%s/"%i+"%(name1)s_%(name2)s.csv"%({"name1":ID,"name2":ptime}))
                filename.append(("%(name1)s_%(name2)s.csv"%({"name1":ID,"name2":ptime})))
                #print(filename)
                driver.close()
                print("success in ",ID)
            except:
                print("(still) error in ",ID)
                pass

    #全部迴圈完再製作一份檔名清單(檔名清單裡每個檔案都有各自BLAST出的AccID)，跟rawdata存在同一目錄好了
    with open(Load_file_dir+"filelist_testo_%s.csv"%i,"w")as file:
        for ele in filename:
            file.write(ele+",")
    #下一步開始整理AccID


    #testo_1
    #error in  KP226786 V
    #error in  GU387224 V
    #error in  DQ683430 V
    #error in  KF975722 V
    #error in  KC254439 V
    #error in  EU650089 V
    #error in  AY536328 V
    #error in  AF448922   V 
    #error in  JF514041 V
    

    #testo_2
    #error in  GQ256223 V
    #error in  AY194069 V
    #error in  JF514028 V

    #testo_3
    #error in  JN189094 V
    #error in  KJ464659 V
    #error in  AY534845 V
    #error in  AY268772 V
    #error in  AY300058 V
    #error in  GQ256206 V
    #error in  GU387251   V
    #error in  KM106060 V
    #error in  JX569730 V
    #error in  JN189070 V
    #error in  AY534817 V
    #error in  KF113290 V
    #error in  KM106061 V
    #error in  EU650070 V
    #error in  AY083627 V
    #error in  EF177303 V
    #error in  AY529467 V
    #error in  AY736341   V
    #error in  JN572252 V
    #error in  JN572279 V
    #error in  GU476674 V

    #testo_4
    #error in  GQ377138 V
    #error in  HQ631294   V
    #error in  KJ464648 V
    #error in  EU650076 V
    #error in  KJ464622 V
    #error in  JN869326 V
    #error in  KF897940 V
    #error in  KP226791 V
    #error in  EF177293 V
    #error in  JN572257 V
    #error in  EU650094 V


    #testo_5
    #error in  DQ164505 V
    #error in  KM106048 V
    #error in  GQ256192 V
    #error in  AF448923 V
    #error in  JX103800 V
    #error in  DQ151979 V
    #error in  JQ700462 V
    #error in  EF177306 V
    #error in  AY536364 V
    #error in  JN654975 V
    #error in  AY268774 V
    #error in  AY534833 V
    #error in  EF177310 V
    #error in  KJ464660 V
#針對那些BLAST不到1000序列的AccID，手動去查發現真的不到1000，
#例如testo_1的DQ849189，總共就49條，最後一條相似度只剩40幾%





