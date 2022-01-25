#主要處理organism切分問題
import csv

#https://www.geeksforgeeks.org/replacing-column-value-of-a-csv-file-in-python/

Load_file_1="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_kuofile.csv"
Load_file_2="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_testo_total.csv"
Load_file_3="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_keyword.csv"
Save_file_1="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_kuofile_revised.csv"
Save_file_2="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_testo_total_revised.csv"
Save_file_3="C:/PYTHON/Download_Seq_files/gb_and_table/merge/merge_keyword_revised.csv"

Load_file_list=[Load_file_1,Load_file_2,Load_file_3]
Save_file_list=[Save_file_1,Save_file_2,Save_file_3]
#reading the CSV file

for i,j in zip(Load_file_list,Save_file_list):
    text = open(i, "r")
    
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
    x = open(j,"w")
    
    #all the replaced text is written in the output.csv file
    x.writelines(text)
    x.close()

