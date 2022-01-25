import operator
import csv
import numpy as np

#因為正常功能只有sort by columen，所以我們轉前先轉置

#先知道資料有幾欄
reader = csv.reader(open("C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/AB046973_gb.csv"), delimiter=",")
sortedlist = sorted(reader)
#print(type(sortedlist[-1]))

file_list_1=sortedlist[-1]
file_process_1=str(file_list_1)[1:-1]
#print(file_process_1)
file_process_1_1=file_process_1.replace(",","','")
file_process_1=file_process_1.replace("'","")
file_process_1=file_process_1.split(",")
#print(type(file_process_1),file_process_1)
#file_len=len(file_process_1)
#print(file_len)#總共幾行知道了

file_list_2=sortedlist[0]
file_process_2=str(file_list_2)[1:-1]
#print(file_process_1)
file_process_2=file_process_2.replace(",","','")
file_process_2=file_process_2.replace("'","")
file_process_2=file_process_2.split(",")
#print(type(file_process_1),file_process_1)
#file_len=len(file_process_2)
#print(file_len)#總共幾行知道了


#目前只試出單列轉置
#csv_table = np.genfromtxt("C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/AB046973_gb.csv", delimiter=",",dtype=str)
csv_table = csv.reader(open("C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/AB046973_gb.csv"), delimiter=",")
csv_table=np.array([file_process_1])
#資料格式預設為float，要讀文字的話一定要寫一下
print(csv_table)
transposed = csv_table.T
print(transposed)
np.savetxt("C:/PYTHON/Download_Seq_files/gb_csv/transpose_Polypodiopsida/kuofile/table.csv", transposed, fmt="%s")
#https://www.kite.com/python/answers/how-to-transpose-a-csv-table-in-python


  
# load csv file
#data = csv.reader(open("C:/PYTHON/Download_Seq_files/gb_csv/transpose_Polypodiopsida/kuofile/table.csv"),delimiter=',')
 
"""
print(data[-1])
#['LOCUS,DEFINITION,ACCESSION,VERSION,KEYWORDS,SOURCE,ORGANISM,REFERENCE,AUTHORS,TITLE,JOURNAL,REFERENCE1,AUTHORS1,TITLE1,JOURNAL1,FEATURES']
print(type(data[-1]))
file_list=data[-1]
file_process_1=str(file_list)[1:-1]
print(file_process_1)
file_process_1=file_process_1.replace(",","','")
file_process_1=file_process_1.replace("'","")
file_process_1=file_process_1.split(",")
print(type(file_process_1),file_process_1)
file_sorted=sorted(file_process_1)
"""










# sort data on the basis of age
#data = sorted(data, key=operator.itemgetter(2))   
#data = sorted(data)   
# displaying sorted data 
#print('After sorting:')
#print(data)







"""
#單行排序
reader = csv.reader(open("C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/AB046973_gb.csv"), delimiter=";")
print(reader)
#<_csv.reader object at 0x00000260714D1F50>
sortedlist = sorted(reader)
#print(sortedlist)
#[['AB046973 369 bp DNA linear PLN 02-OCT-2001,"Deparia marginalis chloroplast DNA, trnL-trnF intergenic spacer.",AB046973,AB046973.1,.,chloroplast Deparia marginalis,Deparia marginalis Eukaryota', ' Viridiplantae', ' Streptophyta', ' Embryophyta', ' Tracheophyta', ' Polypodiopsida', ' Polypodiidae', ' Polypodiales', ' Aspleniineae', ' Athyriaceae', ' Deparia. ,1,"Kato,M.","Deparia cataracticola (Woodsiaceae), a New Species of the Hawaii",Unpublished,2 (bases 1 to 369),"Kato,M. and Nakahira,Y.",Direct Submission,"Submitted (05-AUG-2000) Yuka Nakahira, Graduate School of Arts and Sciences, University of Tokyo, Life Sciences, Multi-Disciplinary Sciences', ' 3-8-1, Komaba, Meguro-ku, Tokyo 153-8902, Japan (E-mail:nakahira@f2.dion.ne.jp, Tel:81-3-5454-6653, Fax:81-3-5454-4333) ","Location/Qualifier source 1..369 /organism=""Deparia marginalis"" /organelle=""plastid:chloroplast"" /mol_type=""genomic DNA"" /db_xref=""taxon:134818"" misc_feature 1..369 /note=""trnL-trnF intergenic spacer"" "'], ['LOCUS,DEFINITION,ACCESSION,VERSION,KEYWORDS,SOURCE,ORGANISM,REFERENCE,AUTHORS,TITLE,JOURNAL,REFERENCE1,AUTHORS1,TITLE1,JOURNAL1,FEATURES']]
print(sortedlist[-1])
#['LOCUS,DEFINITION,ACCESSION,VERSION,KEYWORDS,SOURCE,ORGANISM,REFERENCE,AUTHORS,TITLE,JOURNAL,REFERENCE1,AUTHORS1,TITLE1,JOURNAL1,FEATURES']
print(type(sortedlist[-1]))
file_list=sortedlist[-1]
file_process_1=str(file_list)[1:-1]
print(file_process_1)
file_process_1=file_process_1.replace(",","','")
file_process_1=file_process_1.replace("'","")
file_process_1=file_process_1.split(",")
print(type(file_process_1),file_process_1)
file_sorted=sorted(file_process_1)
print(file_sorted)
#['ACCESSION', 'AUTHORS', 'AUTHORS1', 'DEFINITION', 'FEATURES', 'JOURNAL', 'JOURNAL1', 'KEYWORDS', 'LOCUS', 'ORGANISM', 'REFERENCE', 'REFERENCE1', 'SOURCE', 'TITLE', 'TITLE1', 'VERSION']
"""


