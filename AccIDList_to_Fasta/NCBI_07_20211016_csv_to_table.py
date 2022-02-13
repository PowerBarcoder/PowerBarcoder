import pandas as pd
import csv
import os 
#接著就是，把各集合裡的gb file分好資料夾
# 然後再把資料夾裡的gb轉csv(直接取另一夾的，別浪費時間)
# 再合併成table就完工了

# 請先新建merge資料夾
# 並生成一個merge_template_unsorted.csv，內含第一列

path, filename = os.path.split(os.path.abspath(__file__))
Load_file_dir=path+"\\gb_csv\\"
Save_file_tep=path+"/merge/merge_template_unsorted.csv"
Save_file_dir=path+"\\merge\\"


file_list={Load_file_dir}

for List in file_list:
  filename=[]
  files = os.listdir(List)
  for f in files:
    fullpath = List + f
    if os.path.isfile(fullpath):
      filename.append(f)
  # print(filename)

  #cols=['LOCUS', 'DEFINITION', 'ACCESSION', 'VERSION', 'KEYWORDS', 'SOURCE', 'ORGANISM', 'REFERENCE', 'AUTHORS', 'TITLE', 'JOURNAL', 'REFERENCE1', 'AUTHORS1', 'TITLE1', 'JOURNAL1', 'FEATURES', 'PUBMED', 'REMARK', 'REFERENCE12', 'AUTHORS12', 'TITLE12', 'JOURNAL12', 'COMMENT', 'PUBMED1', 'REMARK1', 'DBLINK']
  #print(len(cols))
  #cols_sorted=sorted(cols)
  #print(cols_sorted)
  #['ACCESSION', 'AUTHORS', 'AUTHORS1', 'AUTHORS12', 'COMMENT', 'DBLINK', 'DEFINITION', 'FEATURES', 'JOURNAL', 'JOURNAL1', 'JOURNAL12', 'KEYWORDS', 'LOCUS', 'ORGANISM', 'PUBMED', 'PUBMED1', 'REFERENCE', 'REFERENCE1', 'REFERENCE12', 'REMARK', 'REMARK1', 'SOURCE', 'TITLE', 'TITLE1', 'TITLE12', 'VERSION']
  #https://officeguide.cc/python-sort-sorted-tutorial-examples/

  LOCUS=[]
  DEFINITION=[]
  ACCESSION=[]
  VERSION=[]
  KEYWORDS=[]
  SOURCE=[]
  ORGANISM=[]
  REFERENCE=[]
  AUTHORS=[]
  TITLE=[]
  JOURNAL=[]
  PUBMED=[]
  REFERENCE1=[]
  AUTHORS1=[]
  TITLE1=[]
  JOURNAL1=[]
  FEATURES=[]
  PUBMED1=[]
  REMARK=[]
  REFERENCE12=[]
  AUTHORS12=[]
  TITLE12=[]
  JOURNAL12=[]
  COMMENT=[]
  PUBMED12=[]
  REMARK1=[]
  DBLINK=[] 

  #https://stackoverflow.com/questions/5757744/how-can-i-get-a-specific-field-of-a-csv-file
  def read_cell(route,x, y):
      with open(route, 'r',encoding='UTF-8') as f:
          reader = csv.reader(f)
          x_count = 0
          for n in reader:
              if x_count == x:
                  cell = n[y]
                  return cell
              x_count += 1
  # print (read_cell(Load_file_dir+"AB191440_gb.csv",0, 3)) 
  #   #譬如："KY932463_gb.csv"第一行第四列叫"VERSION"
  file_num=0
  #for file in filename[5000:-4100]:
  #for file in filename[4715:4730]:
  for file in filename:
    j=0
    file_num=file_num+1
    while j<28:#先填上有的
      try:
        if str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,0)):
          LOCUS.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,1)):
          DEFINITION.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,2)):
          ACCESSION.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,3)):
          VERSION.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,4)):
          KEYWORDS.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,5)):
          SOURCE.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,6)):
          ORGANISM.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,7)):
          REFERENCE.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,8)):
          AUTHORS.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,9)):
          TITLE.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,10)):
          JOURNAL.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,11)):
          REFERENCE1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,12)):
          AUTHORS1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,13)):
          TITLE1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,14)):
          JOURNAL1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,15)):
          FEATURES.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,16)):
          PUBMED.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,17)):
          REMARK.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,18)):
          REFERENCE12.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,19)):
          AUTHORS12.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,20)):
          TITLE12.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,21)):
          JOURNAL12.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,22)):
          COMMENT.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,23)):
          PUBMED1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,24)):
          REMARK1.append(read_cell(List+"%s"%file,1,j))
        elif str(read_cell(List+"%s"%file,0,j))==str(read_cell(Save_file_tep,0,25)):
          DBLINK.append(read_cell(List+"%s"%file,1,j))
        j=j+1
      except:
        #print(file,j,"error")
        j=j+1
        pass
 
    if len(LOCUS)<file_num:
        LOCUS.append("NaN")
    if len(DEFINITION)<file_num:        
        DEFINITION.append("NaN")
    if len(ACCESSION)<file_num: 
        ACCESSION.append("NaN")
    if len(VERSION)<file_num: 
        VERSION.append("NaN")
    if len(KEYWORDS)<file_num: 
        KEYWORDS.append("NaN")
    if len(SOURCE)<file_num:           
        SOURCE.append("NaN")
    if len(ORGANISM)<file_num:           
        ORGANISM.append("NaN")
    if len(REFERENCE)<file_num:           
        REFERENCE.append("NaN")
    if len(AUTHORS)<file_num:           
        AUTHORS.append("NaN")
    if len(TITLE)<file_num:           
        TITLE.append("NaN")
    if len(JOURNAL)<file_num:    
        JOURNAL.append("NaN")
    if len(REFERENCE1)<file_num:    
        REFERENCE1.append("NaN")
    if len(AUTHORS1)<file_num:    
        AUTHORS1.append("NaN")
    if len(TITLE1)<file_num:    
        TITLE1.append("NaN")
    if len(JOURNAL1)<file_num:    
        JOURNAL1.append("NaN")
    if len(FEATURES)<file_num:    
        FEATURES.append("NaN")
    if len(PUBMED)<file_num:    
        PUBMED.append("NaN")
    if len(REMARK)<file_num:    
        REMARK.append("NaN")
    if len(REFERENCE12)<file_num:    
        REFERENCE12.append("NaN")
    if len(AUTHORS12)<file_num:    
        AUTHORS12.append("NaN")
    if len(TITLE12)<file_num:    
        TITLE12.append("NaN")
    if len(JOURNAL12)<file_num:    
        JOURNAL12.append("NaN")
    if len(COMMENT)<file_num:    
        COMMENT.append("NaN")
    if len(PUBMED1)<file_num:    
        PUBMED1.append("NaN")
    if len(REMARK1)<file_num:    
        REMARK1.append("NaN")
    if len(DBLINK)<file_num:    
        DBLINK.append("NaN")


#print()

  LOCUS_x=pd.DataFrame(LOCUS).rename(columns = {0:'LOCUS'})
  DEFINITION_x=pd.DataFrame(DEFINITION).rename(columns = {0:'DEFINITION'})
  ACCESSION_x=pd.DataFrame(ACCESSION).rename(columns = {0:'ACCESSION'})
  VERSION_x=pd.DataFrame(VERSION).rename(columns = {0:'VERSION'})
  KEYWORDS_x=pd.DataFrame(KEYWORDS).rename(columns = {0:'KEYWORDS'})
  SOURCE_x=pd.DataFrame(SOURCE).rename(columns = {0:'SOURCE'})
  ORGANISM_x=pd.DataFrame(ORGANISM).rename(columns = {0:'ORGANISM'})
  REFERENCE_x=pd.DataFrame(REFERENCE).rename(columns = {0:'REFERENCE'})
  AUTHORS_x=pd.DataFrame(AUTHORS).rename(columns = {0:'AUTHORS'})
  TITLE_x=pd.DataFrame(TITLE).rename(columns = {0:'TITLE'})
  JOURNAL_x=pd.DataFrame(JOURNAL).rename(columns = {0:'JOURNAL'})
  PUBMED_x=pd.DataFrame(PUBMED).rename(columns = {0:'PUBMED'})
  REFERENCE1_x=pd.DataFrame(REFERENCE1).rename(columns = {0:'REFERENCE1'})
  AUTHORS1_x=pd.DataFrame(AUTHORS1).rename(columns = {0:'AUTHORS1'})
  TITLE1_x=pd.DataFrame(TITLE1).rename(columns = {0:'TITLE1'})
  JOURNAL1_x=pd.DataFrame(JOURNAL1).rename(columns = {0:'JOURNAL1'})
  FEATURES_x=pd.DataFrame(FEATURES).rename(columns = {0:'FEATURES'})
  PUBMED1_x=pd.DataFrame(PUBMED1).rename(columns = {0:'PUBMED1'})
  REMARK_x=pd.DataFrame(REMARK).rename(columns = {0:'REMARK'})
  REFERENCE12_x=pd.DataFrame(REFERENCE12).rename(columns = {0:'REFERENCE12'})
  AUTHORS12_x=pd.DataFrame(AUTHORS12).rename(columns = {0:'AUTHORS12'})
  TITLE12_x=pd.DataFrame(TITLE12).rename(columns = {0:'TITLE12'})
  JOURNAL12_x=pd.DataFrame(JOURNAL12).rename(columns = {0:'JOURNAL12'})
  COMMENT_x=pd.DataFrame(COMMENT).rename(columns = {0:'COMMENT'})
  PUBMED12_x=pd.DataFrame(PUBMED12).rename(columns = {0:'PUBMED12'})
  REMARK1_x=pd.DataFrame(REMARK1).rename(columns = {0:'REMARK1'})
  DBLINK_x=pd.DataFrame(DBLINK).rename(columns = {0:'DBLINK'}) 

  #print(_x)

  frames = [LOCUS_x,DEFINITION_x,ACCESSION_x,VERSION_x,KEYWORDS_x,SOURCE_x,ORGANISM_x,REFERENCE_x,AUTHORS_x,TITLE_x,JOURNAL_x,PUBMED_x,REFERENCE1_x,AUTHORS1_x,TITLE1_x,JOURNAL1_x,FEATURES_x,PUBMED1_x,REMARK_x,REFERENCE12_x,AUTHORS12_x,TITLE12_x,JOURNAL12_x,COMMENT_x,PUBMED12_x,REMARK1_x,DBLINK_x]
  #frames_1= [LOCUS_x,DEFINITION_x,ACCESSION_x,VERSION_x,KEYWORDS_x,SOURCE_x,ORGANISM_x,REFERENCE_x,AUTHORS_x,TITLE_x,JOURNAL_x,PUBMED_x,REFERENCE1_x,AUTHORS1_x,TITLE1_x,JOURNAL1_x,FEATURES_x,_x,PUBMED1_x,REMARK_x,_x,_x,_x,REFERENCE12_x,AUTHORS12_x,TITLE12_x,JOURNAL12_x,_x]
  #frames_2= [1_x,12_x,1_x,_x,COMMENT_x,1_x,_x,_x,12_x,1_x,_x,PUBMED12_x,REMARK1_x,_x,1_x,1_x,1_x,12_x,124_x,12_x,DBLINK_x]
  #r_1 = pd.concat(frames_1, axis = 1, join = 'outer')
  #r_2 = pd.concat(frames_2, axis = 1, join = 'outer')
  r = pd.concat(frames, axis = 1, join = 'outer')
  #問題可能是出在inner跟outer，因為在範例裡的10個檔案都沒有，所以理當會被刪除???
  #東西是出現了，但是col還是只到
  #r_1.to_csv(Save_file_dir+'merge_done_1.csv')
  #r_2.to_csv(Save_file_dir+'merge_done_2.csv')
  r.to_csv(Save_file_dir+'merge_%s.csv'%List[36:-16])
  print('merge_%s.csv'%List[36:-16]," is finished")


