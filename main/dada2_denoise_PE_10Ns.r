library("devtools")
library("dada2")
path_el <- "C:/Users/salvi/googledrive/Manual/Powerbarcoder_230105_test/dada2_revising/error_learn/SuperRed_35"
path_result <-"C:/Users/salvi/googledrive/Manual/Powerbarcoder_230105_test/dada2_revising/"
setwd("C:/Users/salvi/googledrive/Manual/Powerbarcoder_230105_test/dada2_revising")

fnFs <- sort(list.files(path_el, pattern=".r1.fq", full.names = TRUE))
fnRs <- sort(list.files(path_el, pattern=".r2.fq", full.names = TRUE))
errF <- learnErrors(fnFs, multithread=TRUE)
errR <- learnErrors(fnRs, multithread=TRUE)

numbers = c("01", "02", "03", "04", "05", "06", "07", "08", "09", 10:99)

rbcLN = c("fVGF", "rECL")
AP_minlength = 500  # 這個也變參數
minoverlap = 4 # 這個也變參數

AP<-data.frame(rbcLN)

multiplex <- read.table(
  "multiplex_cpDNAbarcode_clean.txt",
  sep="\t", header = TRUE)

for (a in 1:ncol(AP)){
  colnames(AP[a]) -> region
  AP[,a][1] -> Fp
  AP[,a][2] -> Rp
  multiplex[!multiplex[,AP[,a][2]] %in% "",] -> amplicon
  miss = c()
  seqtable = c()
  dadamergfail = c()
  merg = c() #Kuo_modified
  nonmerg = c() #Kuo_modified
  path_demultiplex = paste0(path_result, region, "_demultiplex")
  path_trim <- paste0(path_demultiplex, "/trimmed")
  sort(list.files(path_trim, pattern=".r1.fq", full.names = FALSE))-> R1.names
  sort(list.files(path_trim, pattern=".r2.fq", full.names = FALSE))-> R2.names
  sort(list.files(path_trim, pattern=".r1.fq", full.names = TRUE))-> R1
  sort(list.files(path_trim, pattern=".r2.fq", full.names = TRUE))-> R2
  paste0(path_trim, "/filtered_", R1.names)-> filtFs
  paste0(path_trim, "/filtered_", R2.names)-> filtRs
  #for(i in seq_along(R1)) {
  #  fastqPairedFilter(c(R1[i], R2[i]), c(filtFs[i], filtRs[i]),
  #                    verbose=TRUE, matchIDs = TRUE)
  #}
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
      write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/r1/",filename), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)
      write.table(r1fas[,1:2], file = paste0(path_demultiplex, "/denoice/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)
      write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/r2/",filename), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)
      write.table(r2fas[,1:2], file = paste0(path_demultiplex, "/denoice/r2/",r0), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)
      #write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r2/",filename), append = FALSE, sep = "\n", quote = FALSE, row.names = FALSE, col.names = FALSE)
      #write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r1/",filename), append = FALSE, sep = "\n", quote = FALSE, row.names = FALSE, col.names = FALSE)
      #write.table(r1fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r1/",r0), append = FALSE, sep = "\n", quote = FALSE,row.names = FALSE, col.names = FALSE)
      #write.table(r2fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/r2/",r0), append = FALSE, sep = "\n", quote = FALSE, row.names = FALSE, col.names = FALSE)

      # r1 r2要merge了
      try(mergers <- mergePairs(dadaFs, r1, dadaRs, r2, minOverlap = minoverlap, verbose=TRUE))
      if (nrow(mergers)>0 & max(nchar(mergers$sequence))>AP_minlength & max(mergers$abundance)>20){
        sum(mergers$abundance)->clustersum
        paste0(rep(header, length(mergers$abundance)), "_", numbers[1:length(mergers$abundance)], rep("_", length(mergers$abundance)), sprintf(mergers$abundance/clustersum, fmt = '%#.3f'), rep("_abundance_", length(mergers$abundance)), mergers$abundance)->merglist
        as.matrix(mergers)->mergers.table
        nchar(mergers.table[,1]) -> seqlen #Kuo_modified
        cbind(merglist,mergers.table,seqlen)-> fas0 #Kuo_modified
        matrix(fas0, ncol = 11)->fas0
        fas0[order(as.numeric(fas0[,3]), decreasing = TRUE),] -> fas0
        matrix(fas0, ncol = 11)->fas0 #Kuo_modified may write out this matrix
        rbind(merg, fas0)-> merg #Kuo_modified could be a table for dada2merge
        fas0[as.numeric(fas0[,11])>AP_minlength,] -> fas #Kuo_modified
        matrix(fas, ncol = 11)->fas
        if (nrow(fas)==0){
          cbind(r1, r2, header)->fail
          rbind(dadamergfail, fail)-> dadamergfail
        }
        write.table(fas[,1:2], file = paste0(path_demultiplex, "/denoice/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(fas[1,1:2], file = paste0(path_demultiplex, "/denoice_best/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
      }else{
        cbind(r1, r2, header)->fail
        rbind(dadamergfail, fail)-> dadamergfail
      }

      try(nonmergers <- mergePairs(dadaFs, r1, dadaRs, r2, verbose=TRUE, justConcatenate=TRUE))#Kuo_modified in following lines else
      if (nrow(nonmergers)>0 ){
        sum(nonmergers$abundance)->clustersum
        paste0(rep(header, length(nonmergers$abundance)), "_", numbers[1:length(nonmergers$abundance)], rep("_", length(nonmergers$abundance)), sprintf(nonmergers$abundance/clustersum, fmt = '%#.3f'), rep("_abundance_", length(nonmergers$abundance)), nonmergers$abundance, rep("_10Ncat", length(nonmergers$abundance)))->nonmerglist
        as.matrix(nonmergers)->nonmergers.table
        cbind(nonmerglist,nonmergers.table)-> fascat #Kuo_modified
        matrix(fascat, ncol = 10)->fascat
        fascat[order(as.numeric(fascat[,3]), decreasing = TRUE),] -> fascat #Kuo_modified may write out this matrix
        matrix(fascat, ncol = 10)->fascat
        rbind(nonmerg, fascat)-> nonmerg #Kuo_modified could be a table for dada2nonmerge
        write.table(fascat[,1:2], file = paste0(path_demultiplex, "/denoice/nonmerged/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        write.table(fascat[1,1:2], file = paste0(path_demultiplex, "/denoice_best/nonmerged/",filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        }

      cbind(rep(r1, length(dadaFs[["clustering"]][["abundance"]])),r1list)-> seqtable01
      cbind(rep(r2, length(dadaRs[["clustering"]][["abundance"]])),r2list)-> seqtable02
      rbind(seqtable, seqtable01, seqtable02)-> seqtable
    }
    if (purrr::has_element(list.files(path= path_trim),s1)==FALSE){
      cbind(r1, header)->mis
      rbind(miss, mis)-> miss}
    }
  write.table(miss, file = paste0(path_demultiplex, "/denoice/missing_samples.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
  write.table(seqtable, file = paste0(path_demultiplex, "/denoice/sequence_table.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
  write.table(dadamergfail, file = paste0(path_demultiplex, "/denoice/dadamerge_fail.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
}







# r1 = "./rbcLN_demultiplex/trimmed/filtered_trim_rbcLN_fVGF_br18_rECL_br13_r1.fq" #Adiantum_hosei_Wade5667_KTHU1824_01_1.000_abundance_60
# r2 = "./rbcLN_demultiplex/trimmed/filtered_trim_rbcLN_fVGF_br18_rECL_br13_r2.fq"
#
#
# r1 = "./rbcLN_demultiplex/trimmed/filtered_trim_rbcLN_fVGF_br08_rECL_br06_r1.fq" #Dicranopteris_linearis_Wade5644_KTHU2005_01_0.274_abundance_45
# r2 = "./rbcLN_demultiplex/trimmed/filtered_trim_rbcLN_fVGF_br08_rECL_br06_r2.fq"
#
#
# dadaFs <- dada(r1, err=errF, multithread=TRUE)
# dadaRs <- dada(r2, err=errR, multithread=TRUE)
# try(nonmergers <- mergePairs(dadaFs, r1, dadaRs, r2, verbose=TRUE, justConcatenate=TRUE))
# as.matrix(nonmergers)-> nonmergers.table
# mergers.table[order(mergers.table[,2],decreasing=TRUE),]
# library("stringr")
# split_r1 = rep("", nrow(nonmergers.table))
# split_r2r = rep("", nrow(nonmergers.table))
# cbind(nonmergers.table,split_r1,split_r2r)
# for (si in 1:nrow(nonmergers.table)){
#   str_split(nonmergers.table2[si,1], "NNNNNNNNNN")[[si]] -> rr
#   nonmergers.table2[si,10] <- rr[1]
#   nonmergers.table2[si,11] <- rr[2]
# }
# cbind(nonmerglist,nonmergers.table2)-> nonmergers.table3
