#https://www.crifan.com/resolved_python_implementation_of_an_error_httperror_http_error_502_bad_gateway/
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import time 
import sys
import os
import pandas as pd

Download_file_dir = 'C:/PYTHON/Download_Seq_files/genbank/'
load_file_dir="C:/PYTHON/Download_Seq_files/"

starttime = time.localtime()
starttime = time.strftime("%Y-%m-%d %I:%M:%S %p" , starttime)

"""
#一條一條讀，太慢了
column_names = ["", "accession"]
df = pd.read_csv(load_file_dir+"union_testo.csv", names=column_names)
AccID = df.accession.to_list()
A=AccID[1:]
#print(A[:10])
"""

with open(load_file_dir+"testo_881.txt","r") as file_pre:
    for line in file_pre:
        print(type(line))
        A=line.split(",")
        print(type(A))
print(A)

#這邊用字典把等等的keyword變成每200個AccID一組
A_dict={}
for k in range(1,6):
    A_list_name="A"+str(k)+"_5"
    #print(A_list_name)
    #如A1_88:
    A_list=A[(200*(k-1)):(200*k)]
    #print(A_list)
    A_dict.setdefault(A_list_name, A_list)
#print(A_dict.get("A1_87"))

B=200#一頁要呈現的條目數量#eg:200

for i in range(1,6):
    text=A_dict.get("A%s_5"%i)
    time.perf_counter()
    #print(text)
    text_rep=str(text).replace("', '", ",%20")
    #https://www.runoob.com/python/att-string-replace.html
    keyword=text_rep[2:-2]
    #print(keyword)

    url="https://www.ncbi.nlm.nih.gov/search/all/?term=%s"%keyword
    PATH="C:/Users/123/Desktop/coding/chromedriver_win32/chromedriver.exe"
    ###########處理這類的報錯ERROR:chrome_browser_main_extra_parts_metrics.cc(234)
    #https://stackoverflow.com/questions/69418411/get-rid-of-response-message-in-python-selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    ###########
    driver=webdriver.Chrome(PATH,options=options)
    driver.get(url)
    search1=driver.find_element_by_xpath('//*[@id="search_db_nuccore"]/span[1]')
    search1.click()

    def END():
        print("下載完成")
        #print("已從",driver.title,"下載序列")
        #print("運行時間是%-5.5ss"%time.perf_counter())
        driver.close()

    def FASTA():
        format=driver.find_element_by_link_text("Summary")
        format.click()
        time.sleep(2)
        showfasta = driver.find_element_by_xpath('//*[@id="fasta"]')
        showfasta.click()

    def GENBANK():
        format=driver.find_element_by_link_text("Summary")
        format.click()
        time.sleep(2)
        showgenbank = driver.find_element_by_xpath('//*[@id="genbank"]')
        showgenbank.click()

    def GENBANK():
        format=driver.find_element_by_link_text("Summary")
        format.click()
        time.sleep(2)
        showgenbank = driver.find_element_by_xpath('//*[@id="genbank"]')
        showgenbank.click()



    def GENBANK_FULL():
        format=driver.find_element_by_link_text("Summary")
        format.click()
        time.sleep(2)
        showgenbank = driver.find_element_by_xpath('//*[@id="gbwithparts"]')
        showgenbank.click()

    def FILTER():
        time.sleep(2)
        filter5000=driver.find_element_by_xpath('//*[@id="facet_rangeseqlen"]')
        filter5000.click()
        from0=driver.find_element_by_xpath('//*[@id="facet_range_stseqlen"]')
        from0.click()
        from0.send_keys("0")
        to5000=driver.find_element_by_xpath('//*[@id="facet_range_endseqlen"]')
        to5000.click()
        to5000.send_keys("5000")
        to5000.send_keys(Keys.ENTER)

    try: #總條目數大於20
        sort=driver.find_element_by_link_text("20 per page")
        #print(sort)#################走這#################
        sort.click()
        time.sleep(2)
        sort200 = driver.find_element_by_xpath('//*[@id="ps%s"]'%B)
        sort200.click()
        #print("try1_A")#################走這#################
    except:#總條目數小於20
        #print("try1_B")
        pass
     
    try:
        FILTER()#我發現filter完之後她是照時間排的，最新的排最前面
        #限制序列長度得加在這裡
        count=driver.find_element_by_class_name("result_count")
        #如果count這行放在FILTER前面，
        #就會變篩選前的count=200，
        # 篩選後必須重讀一次，不然remainder會錯
        #所以我們直接把FILTER往前移
        if len(count.text)>10:#總條目數大於欲呈現之條目數量
            total_items=count.text[16+len(str(B)):]
            page=float(total_items)//int(B)
            remainder=float(total_items)%int(B)
            if remainder!=0:
                page=int(page+1)
            #print(count.text)#"Item: XXXX"
            #print("total page= ",page)
        else:#總條目數小於欲呈現之條目數量
            total_items=count.text[7:]
            page=float(total_items)//int(B)
            remainder=float(total_items)%int(B)
            if remainder!=0:
                page=int(page+1)
            #print(count.text)#################走這#################
            #print(remainder)#################走這#################
            #print("total page= ",page)#################走這#################
        GENBANK()
        seqnum=1
        #print("try2_A")#################走這#################
    except:#總條目數為1
        format=driver.find_element_by_link_text("GenBank")
        format.click()
        time.sleep(2)
        showgenbank = driver.find_element_by_xpath('//*[@id="genbank"]')
        showgenbank.click()
        seqnum=1
        page=1
        remainder=1
        #print("try2_B")
    
    def NEXTPAGE():
        nextpage=driver.find_element_by_link_text("Next >")
        nextpage.click()
    


    def RETRIVE():
        try:
            printgenbank=driver.find_element_by_xpath('//*[@id="%s"]/pre'%page_items)
            x=printgenbank.text
            #print(x)
            x_splice=str(x)[12:24]
            #print(x_splice)
            x_rep=str(x_splice).replace(" ", "")
            with open(Download_file_dir+x_rep+".gb","w") as file:
                file.write(x)
            #print("RetriveA")
        except:
            printgenbank=driver.find_element_by_xpath('//*[@id="%s"]/div/div/pre'%page_items)
            #page_items="viewercontent1"
            x=printgenbank.text
            #print(x)
            x_splice=str(x)[12:24]
            #print(x_splice)#################走這#################
            x_rep=str(x_splice).replace(" ", "")
            with open(Download_file_dir+x_rep+".gb","w") as file:
                file.write(x)
            #print("Download:"+x_rep)
            #print("RetriveB")#################走這#################

    if remainder!=0:
        while page!=1:
            num=1
            while num!=int(B)+1:#這裡需要修改，不然最後一夜會異常終止，雖然還是載得完
                page_items="viewercontent"+str(num)
                time.sleep(2)
                RETRIVE()
                num=num+1
                #print(seqnum)
                #print("solA")
                seqnum=seqnum+1
            NEXTPAGE()
            page=page-1
            #print("剩下頁數：",page)
        if page==1:
            num=1
            while num!=remainder+1:
                page_items="viewercontent"+str(num)
                time.sleep(2)
                RETRIVE()
                num=num+1
                #print(seqnum)#################走這#################
                #print("solB")#################走這#################
                seqnum=seqnum+1      
    else:#remainder==0
        while page!=1:
            num=1
            while num!=int(B)+1:
                page_items="viewercontent"+str(num)
                time.sleep(2)
                RETRIVE()
                num=num+1
                #print(seqnum)
                #print("solC")
                seqnum=seqnum+1
            NEXTPAGE()
            page=page-1
            #print("剩下頁數：",page)
        if page==1:
            num=1
            while num!=int(B)+1:
                page_items="viewercontent"+str(num)
                time.sleep(2)
                RETRIVE()  
                num=num+1
                #print(seqnum)
                #print("solD")
                seqnum=seqnum+1   
    print(seqnum)
    
    endtime = time.localtime()
    endtime = time.strftime("%Y-%m-%d %I:%M:%S %p" , endtime)

    print("from "+ starttime + " to " + endtime)

    #os.rename("filename.txt","%s.gb"%i)#前面已經用gb當檔名了
    END()


