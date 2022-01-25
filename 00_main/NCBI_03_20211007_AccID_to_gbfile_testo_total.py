#等testo抓完再來

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

#一條一條讀，太慢了
column_names = ["", "accession"]
df = pd.read_csv(load_file_dir+"union_testo.csv", names=column_names)
AccID = df.accession.to_list()
A=AccID[1:]
#print(A[:10])

#這邊用字典把等等的keyword變成每200個AccID一組
A_dict={}
remain=[91,95]
for k in range(1,96):
    A_list_name="A"+str(k)+"_95"
    #print(A_list_name)
    #如A1_96:
    A_list=A[(200*(k-1)):(200*k)]
    #print(A_list)
    A_dict.setdefault(A_list_name, A_list)
#print(A_dict.get("A1_95"))

B=200#一頁要呈現的條目數量#eg:200

for i in remain:
    try:
        text=A_dict.get("A%s_95"%i)
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

        print("A%s_95"%i+" finished "+"from "+ starttime + " to " + endtime)

        #os.rename("filename.txt","%s.gb"%i)#前面已經用gb當檔名了
        END()
    except:
        print("A%s_95"%i+" is failed")
        pass


"""
155
A1_95 from 2021-10-14 03:22:36 AM to 2021-10-14 03:28:48 AM
下載完成
154
A2_95 from 2021-10-14 03:22:36 AM to 2021-10-14 03:34:57 AM
下載完成
159
A3_95 from 2021-10-14 03:22:36 AM to 2021-10-14 03:41:20 AM
下載完成
153
A4_95 from 2021-10-14 03:22:36 AM to 2021-10-14 03:47:31 AM
下載完成
165
A5_95 from 2021-10-14 03:22:36 AM to 2021-10-14 03:54:00 AM
下載完成
164
A6_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:00:30 AM
下載完成
161
A7_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:07:00 AM
下載完成
154
A8_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:13:12 AM
下載完成
158
A9_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:19:35 AM
下載完成
158
A10_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:26:00 AM
下載完成
156
A11_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:32:34 AM
下載完成
162
A12_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:39:27 AM
下載完成
154
A13_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:46:13 AM
下載完成
169
A14_95 from 2021-10-14 03:22:36 AM to 2021-10-14 04:52:44 AM
下載完成
"""

#這次做完的從A14_95算起，所以要加14
"""
171
A15_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 05:50:22 AM
下載完成
170
A16_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 05:57:04 AM
下載完成
159
A17_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:03:18 AM
下載完成
170
A18_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:09:59 AM
下載完成
157
A19_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:16:11 AM
下載完成
161
A20_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:22:28 AM
下載完成
157
A21_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:28:46 AM
下載完成
154
A22_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:34:54 AM
下載完成
170
A23_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:41:32 AM
下載完成
166
A24_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:48:04 AM
下載完成
166
A25_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 06:54:36 AM
下載完成
163
A26_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:01:04 AM
下載完成
170
A27_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:07:48 AM
下載完成
155
A28_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:13:55 AM
下載完成
163
A29_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:20:20 AM
下載完成
149
A30_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:26:28 AM
下載完成
151
A31_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:32:35 AM
下載完成
157
A32_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:39:07 AM
下載完成
146
A33_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:45:05 AM
下載完成
161
A34_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:51:35 AM
下載完成
163
A35_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 07:58:06 AM
下載完成
157
A36_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:04:18 AM
下載完成
159
A37_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:10:47 AM
下載完成
148
A38_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:16:47 AM
下載完成
155
A39_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:23:00 AM
下載完成
158
A40_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:29:18 AM
下載完成
164
A41_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:35:58 AM
下載完成
155
A42_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:42:11 AM
下載完成
159
A43_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:48:29 AM
下載完成
166
A44_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 08:55:04 AM
下載完成
155
A45_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:01:14 AM
下載完成
152
A46_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:07:34 AM
下載完成
167
A47_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:14:11 AM
下載完成
159
A48_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:20:29 AM
下載完成
154
A49_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:26:36 AM
下載完成
158
A50_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:32:58 AM
下載完成
157
A51_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:39:17 AM
下載完成
165
A52_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:45:58 AM
下載完成
152
A53_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:52:04 AM
下載完成
162
A54_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 09:58:42 AM
下載完成
163
A55_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:05:11 AM
下載完成
150
A56_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:11:13 AM
下載完成
162
A57_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:17:37 AM
下載完成
168
A58_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:24:23 AM
下載完成
161
A59_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:30:48 AM
下載完成
169
A60_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:37:30 AM
下載完成
161
A61_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:43:51 AM
下載完成
165
A62_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:50:23 AM
下載完成
157
A63_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 10:56:33 AM
下載完成
167
A64_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:03:08 AM
下載完成
158
A65_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:09:22 AM
下載完成
166
A66_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:15:48 AM
下載完成
154
A67_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:21:57 AM
下載完成
155
A68_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:28:04 AM
下載完成
160
A69_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:34:22 AM
下載完成
164
A70_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:40:51 AM
下載完成
160
A71_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:47:11 AM
下載完成
172
A72_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 11:54:08 AM
下載完成
170
A73_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:01:03 PM
下載完成
168
A74_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:07:37 PM
下載完成
160
A75_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:13:56 PM
下載完成
158
A76_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:20:15 PM
下載完成
148
A77_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:26:06 PM
下載完成
158
A78_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:32:20 PM
下載完成
156
A79_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:38:30 PM
下載完成
158
A80_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:44:49 PM
下載完成
159
A81_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:51:02 PM
下載完成
162
A82_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 12:57:28 PM
下載完成
157
A83_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:03:42 PM
下載完成
164
A84_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:10:12 PM
下載完成
159
A85_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:16:27 PM
下載完成
152
A86_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:22:29 PM
下載完成
2
A87_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:23:12 PM
下載完成
163
A88_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:29:35 PM
下載完成
160
A89_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:36:00 PM
下載完成
162
A90_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:42:26 PM
下載完成
156
A91_95 finished from 2021-10-14 02:49:09 PM to 2021-10-14 02:55:24 PM
下載完成
162
A92_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:49:35 PM
下載完成
158
A93_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 01:55:56 PM
下載完成
160
A94_95 finished from 2021-10-14 05:43:41 AM to 2021-10-14 02:02:24 PM
下載完成
160
A95_95 finished from 2021-10-14 02:35:01 PM to 2021-10-14 02:47:11 PM
下載完成
"""

#總計14932條序列，接著轉檔分類