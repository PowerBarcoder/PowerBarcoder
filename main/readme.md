# Issue Undone
1. dada2 的 chimera killing 功能 看能不加進去
2. "log_dada2.txt" 應該要跟其他result files 放一起比較合理 
3. 可能有人 不 清楚 要先cd 去那裏執行 powerbarcoder.sh，最好全都改寫成傳參寫法的絕對路徑 
4. 看要不要寫一個 powerbarcoder.py 來將 config 的設定讀進去，讓他們(設定檔、執行檔)兩個人的功能是分開清楚的
5. powerbarcode.sh的執行方式是powerbarcoder -config XXX/路徑/XXX/pbc.config
6. secondary merge ： rbcLC + rbcLN (deadline 20230215)
7. create new result files
   - merge_seq_text=">"+output_filename+"\n"+merge_seq+"\n"
   - merge_seq這裡把"N"跟"-"取代掉，然後存一個新的檔案，可以直接給別人用來做樹，之前在mergeSeq的是用來確認序列有沒有拼對的
8. DADA2的10N


# 前置步驟
取出denoise best的nonmerge資料夾內的r1跟r2
從r1及r2資料夾中取出來blast(所以第一步的路徑要抽換成今天的)
//home/lykuo/lab_data/NGS_data/miseq/test_LIB720/rbcLN_demultiplex/denoice_best/nonmerged/r1

 執行順序
 1. '00_blastForRef.sh'：執行localBlast，獲得參考序列的檔案refResult.txt
 2. 'BlastResult.py'：將localBlast結果轉換成物件(BlastRef)，並在blastResult資料夾內寫出成檔案blastResult.txt
        #重啟後大部分檔案都會被覆寫，唯獨blastResult.txt看不會，需要刪除其他localblast的檔案才會有新的生成

 從這裡開始需要執行for迴圈，希望可以只讀一次blastResult
 1. 'BeforeAlignment.py'：align前我們需要在此利用r1 r2製作他們的r1Ref及r2Ref的序列
 2. 'Alignment.py'：將r1 r2序列align
 3. 'merge.py'：開始合併align好的r1 r2從物件(Miseq、FastaUnit)寫出成檔案

 調用的類別(當資料有多個key:value時，用物件存比較方便操作)
 1. 'BlastRef.py' (localblast結果的物件)
 2. 'FastaUnit.py' (fasta檔的物件)
 3. 'Miseq.py' (要拼接的r1或r2的物件)