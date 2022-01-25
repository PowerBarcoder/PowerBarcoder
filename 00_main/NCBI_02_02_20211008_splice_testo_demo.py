#處理單行AccID，中間無blank
from pandas.io.parsers import read_csv
import pandas as pd
import csv
load_file_dir="C:/PYTHON/Download_Seq_files/"

"""#格式不同，下面另寫一段
#csv to list
column_names = ["", "accession"]
df = pd.read_csv(load_file_dir+"testo_881.txt", names=column_names)
AccID = df.accession.to_list()
A=AccID[1:]
#print(A)
"""

with open(load_file_dir+"testo_881.txt","r") as file_pre:
    for line in file_pre:
        print(type(line))
        A=line.split(",")
        print(type(A))
print(A)

#list splice to dict
#https://selflearningsuccess.com/python-dictionary/
A_dict={}
for i in range(1,6):#這裡的66是由13108/200=65.54來的
    A_list_name="A"+str(i)+"_5"
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
with open(load_file_dir+"splice200_testo_pre.csv","w") as file:
    writer = csv.writer(file)
    for k, v in A_dict.items():
       writer.writerow([k, v])

#print("done with resule","splice200_pre.csv")
"""

print(A_dict)

#dict to txt
with open(load_file_dir+"splice200_testo_pre.txt","w") as file:
    file.write(str(A_dict))
#print("done with result","splice200_pre.txt")


