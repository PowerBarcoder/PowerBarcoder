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

Load_file_dir="C:/PYTHON/Download_Seq_files/"
Save_file_dir="C:/PYTHON/Download_Seq_files/acclist/"

seqID=[]
seqlist=[]

#input("確定要執行?")
with open(Load_file_dir+"seqID.csv","r")as file:
    for line in file:
        seqID.append(line[:-1])
    print(seqID)
with open(Load_file_dir+"seqlist.csv","r")as file:
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

filename=[]
for seq,ID in zip(seqlist,seqID):
    url="https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome"
    PATH="C:/Users/123/Desktop/coding/chromedriver_win32/chromedriver.exe"
    driver=webdriver.Chrome(PATH)
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
    print(sort)######
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
        print("------------------fail-------------------")
        time.sleep(20)
        RID= driver.find_element_by_xpath('//*[@id="hsum"]/div[1]/dl/dd[2]/a')

    print("--------------------------------")
    print("本次blast序號為",RID.text)
    RIDtext=RID.text
    print("--------------------------------")
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
    accID_x.to_csv(Save_file_dir+"%(name1)s_%(name2)s.csv"%({"name1":ID,"name2":ptime}))
    filename.append(("%(name1)s_%(name2)s.csv"%({"name1":ID,"name2":ptime})))
    print(filename)
    driver.close()

#全部迴圈完再製作一份檔名清單(檔名清單裡每個檔案都有各自BLAST出的AccID)，跟rawdata存在同一目錄好了
with open(Load_file_dir+"filelist.csv","w")as file:
    for ele in filename:
        file.write(ele+",")
#下一步開始整理AccID





