#主要處理organism切分問題
import csv
import os 
#https://www.geeksforgeeks.org/replacing-column-value-of-a-csv-file-in-python/

path, filename = os.path.split(os.path.abspath(__file__))
Load_file_1=path+"/merge/merge_load_from_.csv"
Save_file_1=path+"/merge/merge_load_from_revised.csv"

Load_file_list=[Load_file_1]
Save_file_list=[Save_file_1]
#reading the CSV file

for i,j in zip(Load_file_list,Save_file_list):
    text = open(i, "r",encoding='UTF-8')
    
    #join() method combines all contents of 
    # csvfile.csv and formed as a string
    text = ''.join([i for i in text]) 
    #上面的方法真聰明
    #join用法
    #https://learn.markteaching.com/python-join-%E6%95%99%E5%AD%B8/
    #search and replace the contents
    text = text.replace("ORGANISM", "Scientific_name,ORGANISM") 
    text = text.replace(" Eukaryota", ",Eukaryota") 
    
    #output.csv is the output file opened in write mode
    x = open(j,"w",encoding='UTF-8')
    
    #all the replaced text is written in the output.csv file
    x.writelines(text)
    x.close()

