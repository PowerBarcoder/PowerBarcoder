#目的：獲得col的項目
import pandas as pd
from os import listdir,path

Load_file_dir_x="C:/PYTHON/Download_Seq_files/gb_csv/kuofile/Polypodiopsida/"
Load_file_dir_y="C:/PYTHON/Download_Seq_files/gb_csv/testo_total/Polypodiopsida/"
Load_file_dir_z="C:/PYTHON/Download_Seq_files/gb_csv/keyword/Polypodiopsida/"
Save_file_dir="C:/PYTHON/Download_Seq_files/gb_and_table/merge/"

dir_load_list=[Load_file_dir_x,Load_file_dir_y,Load_file_dir_z]


filename=[]

for i in dir_load_list:
    files = listdir(i)
    for f in files:
        fullpath = i + f
        if path.isfile(fullpath):
            filename.append(fullpath)
    #print(filename)
    print(len(filename))#7646#16672#29355

col=[]
#x=0
for f in filename:
    #print(f)
    text=open(f).readline()[:-1]#又多了最後一個字元
    #print(text)
    #LOCUS,DEFINITION,ACCESSION,VERSION,KEYWORDS,SOURCE,ORGANISM,REFERENCE,AUTHORS,TITLE,JOURNAL,REFERENCE1,AUTHORS1,TITLE1,JOURNAL1,FEATURES,source,misc_feature
    List=text.split(",")
    #print(List)
    #['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'source', 'misc_feature\n']
    for ele in List:
        if ele in col:
            pass
        else:
            col.append(ele)
    #print(list)
    #x=x+1
    #if x>100:
    #    break
print(col)

"""全部的col項就這樣了
['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'source', 'misc_feature', 'PUBMED', 'REMARK', 'gene', 'intron', 'CDS', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'gap', 'gap1', 'gap12', 'gene1', 'tRNA', 'COMMENT', 'tRNA1', 'primer_bind', 'exon', 'gene12', 'misc_feature1', 'misc_difference', 'PUBMED1', 'REMARK1', 'misc_RNA', 'CDS1', 'exon1', 'intron1', 'exon12', 'gene123', 'tRNA12', 'DBLINK']
"""

"""
['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'source', 'misc_feature', 'PUBMED', 'REMARK', 'gene', 'intron', 'CDS', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'gap', 'gap1', 'gap12', 'gene1', 'tRNA', 'COMMENT', 'tRNA1', 'primer_bind', 'exon', 'gene12', 'misc_feature1', 'misc_difference', 'PUBMED1', 'REMARK1', 'misc_RNA', 'CDS1', 'exon1', 'intron1', 'exon12', 'gene123', 'tRNA12', 'DBLINK']
"""

"""
L=['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'source', 'misc_feature', 'PUBMED', 'REMARK', 'gene', 'intron', 'CDS', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'gap', 'gap1', 'gap12', 'gene1', 'tRNA', 'COMMENT', 'tRNA1', 'primer_bind', 'exon', 'gene12', 'misc_feature1', 'misc_difference', 'PUBMED1', 'REMARK1', 'misc_RNA', 'CDS1', 'exon1', 'intron1', 'exon12', 'gene123', 'tRNA12', 'DBLINK']
print(len(L))#49，沒問題，修完bug後col條目沒變
"""

"""FEATURE合併
['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'PUBMED', 'REMARK', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'COMMENT', 'PUBMED1', 'REMARK1', 'DBLINK']
"""
L=['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'PUBMED', 'REMARK', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'COMMENT', 'PUBMED1', 'REMARK1', 'DBLINK']
print(len(L))#26
