from pandas.io.parsers import read_csv
import pandas as pd
import csv
load_file_dir="C:/PYTHON/Download_Seq_files/"

#csv to list
column_names = ["", "accession"]
df = pd.read_csv(load_file_dir+"union_testo.csv", names=column_names)
AccID = df.accession.to_list()
A=AccID[1:]
#print(A)

#list splice to dict
#https://selflearningsuccess.com/python-dictionary/
A_dict={}
for i in range(1,88):
    A_list_name="A"+str(i)+"_87"
    #print(A_list_name)
    #如A1_88:
    A_list=A[(200*(i-1)):(200*i)]
    #print(A_list)
    A_dict.setdefault(A_list_name, A_list)
#print(A_dict)
#print(A_dict.get("A1_87"))#頭正確
#print(len(A_dict.get("A1_87")))#200
#print(A_dict.get("A87_87"))#尾正確
#print(len(A_dict.get("A87_87")))#174

"""
#dict to csv
with open(load_file_dir+"splice200.csv","w") as file:
    writer = csv.writer(file)
    for k, v in A_dict.items():
       writer.writerow([k, v])

#print("done with resule","splice200.csv")
"""

#dict to txt
with open(load_file_dir+"splice200_testo.txt","w") as file:
    file.write(str(A_dict))
#print("done with resule","splice200.txt")


