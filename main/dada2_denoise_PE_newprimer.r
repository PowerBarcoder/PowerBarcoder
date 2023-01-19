#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

# shell封裝的時候，要先裝好給這裡的R來用
library("devtools")
library("dada2")


# shell包一個錯誤處理，如果r1r2沒有配起來的話，loop會直接停掉
# 兩個list要1對1 pair，看是要用map還是讓list塞一個空值，針對file size==0的

#learn error rate illumina
#path is a VARIABLE
path_el <- args[4]   #指定資料，給dada2學error # 預設讀這個，如果他想讀別的，要寫條件判斷去抓一個新的參數 done
path_reads <- args[1]                        #cutadapt讀取資料的位置
path_result <- args[3]                       #cutadapt輸出資料的位置
fnFs <- sort(list.files(path_el, pattern=".r1.fq", full.names = TRUE))
fnRs <- sort(list.files(path_el, pattern=".r2.fq", full.names = TRUE))
errF <- learnErrors(fnFs, multithread=TRUE)
errR <- learnErrors(fnRs, multithread=TRUE)

# 準備一些變數
numbers = c("01", "02", "03", "04", "05", "06", "07", "08", "09", 10:99)



# 這邊寫死了，要修改， TODO
# 策略一： multiplex...txt的table用loci.1、loci.2這樣的參數取代掉c("fNYG", "rVVG")內的兩個參數
# 策略二：直接從config檔裡面傳參數近來，會遇到的問題是，你不知道他要傳幾組，所以可能要寫成向第41行的處理方式
# rbcLC = c("fNYG", "rVVG") #"rbcLC" and column names of primers, VARIABLEs; the first and second items corresponding to the order in demultiplex.sh
# rbcLN = c("fVGF", "rECL")
# 多loci，要從sh傳參近來，搭配multiplex_clean.txt一起使用，後者是使用者自備的，所以格式很重要
# trnLF = c("L5675", "F4121")
# trnL = c("oneIf1", "L7556")
AP_minlength = 270

#AP<-data.frame(rbcLC, rbcLN, trnLF, trnL)
#AP<-data.frame(rbcLC)

#yixuan modified(使用策略一，所以multiplex_cpDNAbarcode_clean那份檔案的欄位名稱要記得改)
#AP as below
#nameOfloci[1]    nameOfloci[2]   ...
#nameOfloci[1]_1  nameOfloci[2]_1 ...
#nameOfloci[1]_2  nameOfloci[2]_2 ...
AP = data.frame(matrix(nrow = 2, ncol = 0))
for(i in 6:(as.numeric(length(args[])))){
  AP_temp = c(paste0(args[i],"_1"), paste0(args[i],"_2"))
  AP[ ,paste0(args[i])] <- AP_temp
}

multiplex_cpDNAbarcode_clean_path = paste0(path_reads, args[5]) #20230107 "multiplex_cpDNAbarcode_clean.txt"請改成變數 done
multiplex <- read.table(
  multiplex_cpDNAbarcode_clean_path,
  sep="\t", header = TRUE)

#1:ncol(AP) to loop all regions
for (a in 1:ncol(AP)){
  colnames(AP[a]) -> region
  AP[,a][1] -> Fp
  AP[,a][2] -> Rp


  # 檢查amplicon欄為空，則刪除table內該列資料
  multiplex[!multiplex[,AP[,a][2]] %in% "",] -> amplicon


  miss = c()
  seqtable = c()
  mergfail = c()
  path_demultiplex = paste0(path_result, region, "_demultiplex")
  path_trim <- paste0(path_demultiplex, "/trimmed")
  sort(list.files(path_trim, pattern=".r1.fq", full.names = FALSE))-> R1.names
  sort(list.files(path_trim, pattern=".r2.fq", full.names = FALSE))-> R2.names
  sort(list.files(path_trim, pattern=".r1.fq", full.names = TRUE))-> R1
  sort(list.files(path_trim, pattern=".r2.fq", full.names = TRUE))-> R2
  paste0(path_trim, "/filtered_", R1.names)-> filtFs
  paste0(path_trim, "/filtered_", R2.names)-> filtRs


  #   這一步做pair，先用了r1的seq_along來迭代，可以改成指定數字，
  for(i in seq_along(R1)) {
    fastqPairedFilter(c(R1[i], R2[i]), c(filtFs[i], filtRs[i]),
                      verbose=TRUE, matchIDs = TRUE)
  }



  #pair好的檔案開始處理
  #pair reads
  for (s in 1:nrow(amplicon)){
    s1 = paste0("filtered_trim_", region, "_", amplicon[s,Fp],"_", amplicon[s,Rp], "_r1.fq")
    r1 = paste0(path_trim, "/filtered_trim_", region, "_", amplicon[s,Fp],"_", amplicon[s,Rp], "_r1.fq")
    r2 = paste0(path_trim, "/filtered_trim_", region, "_", amplicon[s,Fp],"_", amplicon[s,Rp], "_r2.fq")
    r0 = paste0(amplicon[s,Fp],"_", amplicon[s,Rp])
    filename = paste(amplicon[s,1], amplicon[s,2], amplicon[s,3], amplicon[s,4], ".fas", sep = "_")  #看起來應該就是檔名了
    seqname = paste(amplicon[s,3], amplicon[s,4], amplicon[s,2], amplicon[s,1], sep = "_")           #這個式header的文字
    header = paste0(">",seqname)                                                                     #加上了header的符號
    if (purrr::has_element(list.files(path= path_trim),s1)==TRUE){ #這邊只檢查了r1的名字有沒有對，有對boolean就是TRUE

      # 核心運行，運行後看要不要merge，不能merge的就交由我寫的來處理
      dadaFs <- dada(r1, err=errF, multithread=TRUE)
      dadaRs <- dada(r2, err=errR, multithread=TRUE)



      paste0(rep(header, length(dadaFs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaFs[["clustering"]][["abundance"]])], rep("_r1_", length(dadaFs[["clustering"]][["abundance"]])), sprintf(dadaFs[["clustering"]][["abundance"]]/sum(dadaFs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaFs[["clustering"]][["abundance"]])), dadaFs[["clustering"]][["abundance"]])->r1list
      cbind(r1list,dadaFs[["clustering"]][["sequence"]],dadaFs[["clustering"]][["abundance"]])-> r1fas
      r1fas[order(as.numeric(r1fas[,3]), decreasing = TRUE),]-> r1fas
      matrix(r1fas, ncol = 3)-> r1fas
      paste0(rep(header, length(dadaRs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaRs[["clustering"]][["abundance"]])], rep("_r2_", length(dadaRs[["clustering"]][["abundance"]])), sprintf(dadaRs[["clustering"]][["abundance"]]/sum(dadaRs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaRs[["clustering"]][["abundance"]])), dadaRs[["clustering"]][["abundance"]])->r2list
      cbind(r2list,dadaRs[["clustering"]][["sequence"]],dadaRs[["clustering"]][["abundance"]])-> r2fas
      r2fas[order(as.numeric(r2fas[,3]), decreasing = TRUE),]-> r2fas
      matrix(r2fas, ncol = 3)-> r2fas

      # r1 r2要merge了
      try(mergers <- mergePairs(dadaFs, r1, dadaRs, r2, verbose=TRUE))




      if (nrow(mergers)>0 & max(nchar(mergers$sequence))>AP_minlength & max(mergers$abundance)>20){
        sum(mergers$abundance)->clustersum
        paste0(rep(header, length(mergers$abundance)), "_", numbers[1:length(mergers$abundance)], rep("_", length(mergers$abundance)), sprintf(mergers$abundance/clustersum, fmt = '%#.3f'), rep("_abundance_", length(mergers$abundance)), mergers$abundance)->merglist
        cbind(merglist,mergers$sequence,mergers$abundance)-> fas
        fas[order(as.numeric(fas[,3]), decreasing = TRUE),] -> fas
        matrix(fas, ncol = 3)-> fas
        write.table(fas[,1:2], file = paste0(path_demultiplex, "/denoice/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/r1/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r1/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/r2/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r2/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/r2/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r2/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
      }
      else {
        cbind(r1, r2, header)->fail
        rbind(mergfail, fail)-> mergfail
        write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/nonmerged/r1/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/nonmerged/r1/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/nonmerged/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/nonmerged/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/nonmerged/r2/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/nonmerged/r2/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/nonmerged/r2/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/nonmerged/r2/",r0), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
      }
      cbind(rep(r1, length(dadaFs[["clustering"]][["abundance"]])),r1list)-> seqtable01
      cbind(rep(r2, length(dadaRs[["clustering"]][["abundance"]])),r2list)-> seqtable02
      rbind(seqtable, seqtable01, seqtable02)-> seqtable
    }
    if (purrr::has_element(list.files(path= path_trim),s1)==FALSE){
      cbind(r1, header)->mis
      rbind(miss, mis)-> miss
    }
  }
  write.table(miss, file = paste0(path_demultiplex, "/denoice/missing_samples.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
  write.table(seqtable, file = paste0(path_demultiplex, "/denoice/sequence_table.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
  write.table(mergfail, file = paste0(path_demultiplex, "/denoice/merge_fail.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
}
