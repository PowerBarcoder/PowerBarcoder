#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)

# shell封裝的時候，要先裝好給這裡的R來用
library("devtools")
library("dada2")
library("foreach")
library("doParallel")

# shell包一個錯誤處理，如果r1r2沒有配起來的話，loop會直接停掉
# 兩個list要1對1 pair，看是要用map還是讓list塞一個空值，針對file size==0的

#learn error rate illumina

# TODO  DADA2 requires no Ns if filtered reads are not worked

#path is a VARIABLE
path_of_error_learning <- args[4]   #指定資料，給dada2學error # 預設讀這個，如果他想讀別的，要寫條件判斷去抓一個新的參數 done
path_of_reads <- args[1]                        #cutadapt讀取資料的位置
path_of_result <- args[3]                       #cutadapt輸出資料的位置
filename_of_error_learning_Fs <- sort(list.files(path_of_error_learning, pattern = ".r1.fq", full.names = TRUE))
filename_of_error_learning_Rs <- sort(list.files(path_of_error_learning, pattern = ".r2.fq", full.names = TRUE))
errF <- learnErrors(filename_of_error_learning_Fs, multithread = TRUE)
errR <- learnErrors(filename_of_error_learning_Rs, multithread = TRUE)

# 準備一些變數
# (用於標示abundance排序，意味一個sample最多就99個ASV)
numbers = c("01", "02", "03", "04", "05", "06", "07", "08", "09", 10:99)
AP_minlength = as.numeric(args[6])  # 這個也變參數(序列長度)
minoverlap = as.numeric(args[7]) # 這個也變參數(merge重疊bp數)


# Get the locus names and their elements as parameters
# # example: "a" "b" "c" "d" "e" "rbcLN" "trnLF" "rbcLC" "trnL" "fVGF" "rECL" "L5675" "F4121" "fNYG" "rVVG" "oneIf1" "L7556"
loci_count <- length(args[8:as.numeric(length(args[]))]) / 3
loci_count # 4
locus_names <- args[8:(8 + loci_count - 1)]
locus_names # "rbcLN" "trnLF" "rbcLC" "trnL"
locus_elements <- args[(8 + loci_count):as.numeric(length(args[]))]
locus_elements # "fVGF" "rECL" "L5675" "F4121" "fNYG"   "rVVG" "oneIf1" "L7556"

# Create a data frame using the locus names and elements
AP <- data.frame(matrix(nrow = 2, ncol = length(locus_names)))
colnames(AP) <- locus_names
AP[1,] <- locus_elements[1:(length(locus_elements) %/% 2)] # 取primerF
AP[2,] <- locus_elements[((length(locus_elements) %/% 2)+1):length(locus_elements)] # 取primerR

# Print the resulting data frame
print(AP)

multiplex_cpDNAbarcode_clean_path = paste0(path_of_reads, args[5]) #20230107 "multiplex_cpDNAbarcode_clean.txt"請改成變數 done
multiplex <- read.table(
  multiplex_cpDNAbarcode_clean_path,
  sep = "\t", header = TRUE)
#1:ncol(AP) to loop all regions
for (a in 1:ncol(AP)) {
  colnames(AP[a]) -> region
  AP[, a][1] -> Fp
  AP[, a][2] -> Rp

  # 檢查amplicon欄為空，則刪除table內該列資料
  multiplex[!multiplex[, AP[, a][2]] %in% "",] -> amplicon


  missing_sample_list = c()
  seqtable = c()
  dadamergfail = c()
  merg = c() #Kuo_modified
  nonmerg = c() #Kuo_modified
  path_demultiplex = paste0(path_of_result, region, "_result/demultiplexResult")
  path_denoise = paste0(path_of_result, region, "_result/denoiseResult")
  path_merge = paste0(path_of_result, region, "_result/mergeResult")

  path_trim <- paste0(path_demultiplex, "/trimmed")
  sort(list.files(path_trim, pattern = ".r1.fq", full.names = FALSE)) -> R1.names
  sort(list.files(path_trim, pattern = ".r2.fq", full.names = FALSE)) -> R2.names
  sort(list.files(path_trim, pattern = ".r1.fq", full.names = TRUE)) -> R1
  sort(list.files(path_trim, pattern = ".r2.fq", full.names = TRUE)) -> R2
  path_filter <- paste0(path_demultiplex, "/filtered")
  paste0(path_filter, "/filtered_", R1.names) -> filtFs
  paste0(path_filter, "/filtered_", R2.names) -> filtRs

  # first step: filter
  # 這一步做pair，先用了r1的seq_along來迭代，可以改成指定數字， (this step is really slow)
  # 64s vs. 24s
  # Set the number of cores to utilize
  numCores <- detectCores()
  # Register parallel backend
  registerDoParallel(cores = numCores)
  # Create a parallelized version of the loop using foreach
  foreach(i = seq_along(R1), .packages = c("dada2")) %dopar% {
    fastqPairedFilter(c(R1[i], R2[i]), c(filtFs[i], filtRs[i]),
                      verbose = TRUE, matchIDs = TRUE, compress = FALSE)
  }
  # Stop the parallel backend
  stopImplicitCluster()


  #  20230604 這裡開始不知道怎麼把"_"改成"_splitter_"，先擱置
  #  (20230630 經過檔名重排後，現在檔名統一都從這裡開始牌之後就不再過多的加工了，)
  #           (若需要parsing，則盡量從尾端往頭端，因為頭端的物種名可能有數量不一的分割符("_"))
  # second step: denoise
  numCores <- detectCores()
  registerDoParallel(cores = numCores)
  foreach(sample_number = 1:nrow(amplicon), .packages = c("dplyr")) %dopar% { #20230421 we use multi-thread to speed up
    sample_filename = paste0("filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r1.fq")
    r1 = paste0(path_filter, "/filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r1.fq")
    r2 = paste0(path_filter, "/filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r2.fq")
    r0 = paste0(amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp])
    # filename = paste(amplicon[sample_number, 1], amplicon[sample_number, 2], amplicon[sample_number, 3], amplicon[sample_number, 4], ".fas", sep = "_")  #看起來應該就是檔名了
    filename = paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], ".fas", sep = "_")    #20230623 檔名改跟header一樣
    seqname = paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], sep = "_")           #這個式header的文字
    header = paste0(">", seqname) #加上了header的符號

    #這邊只檢查了r1的名字有沒有對，有對boolean就是TRUE
    if (purrr::has_element(list.files(path = path_filter), sample_filename) == FALSE) {
      cbind(r1, header) -> mis
      rbind(missing_sample_list, mis) -> missing_sample_list
    }else {

      # # # TODO 這裡僅供測試
      # # 使用DADA2merge結果作為BLAST REF，identical仍為N/A者
      # debug_filter_list = c("trnLF_L5675_br02_F4121_br04", "trnLF_L5675_br02_F4121_br07", "trnLF_L5675_br02_F4121_br09", "trnLF_L5675_br02_F4121_br15", "trnLF_L5675_br03_F4121_br12", "trnLF_L5675_br03_F4121_br18", "trnLF_L5675_br04_F4121_br07", "trnLF_L5675_br04_F4121_br12", "trnLF_L5675_br04_F4121_br16", "trnLF_L5675_br05_F4121_br06", "trnLF_L5675_br05_F4121_br09", "trnLF_L5675_br05_F4121_br13", "trnLF_L5675_br05_F4121_br14", "trnLF_L5675_br06_F4121_br02", "trnLF_L5675_br06_F4121_br06", "trnLF_L5675_br06_F4121_br09", "trnLF_L5675_br06_F4121_br14", "trnLF_L5675_br06_F4121_br17", "trnLF_L5675_br07_F4121_br10", "trnLF_L5675_br07_F4121_br11", "trnLF_L5675_br07_F4121_br14", "trnLF_L5675_br07_F4121_br15", "trnLF_L5675_br07_F4121_br16", "trnLF_L5675_br08_F4121_br04", "trnLF_L5675_br09_F4121_br02", "trnLF_L5675_br09_F4121_br03", "trnLF_L5675_br09_F4121_br07", "trnLF_L5675_br10_F4121_br06", "trnLF_L5675_br10_F4121_br16", "trnLF_L5675_br10_F4121_br17", "trnLF_L5675_br11_F4121_br16", "trnLF_L5675_br12_F4121_br16", "trnLF_L5675_br13_F4121_br01", "trnLF_L5675_br13_F4121_br03", "trnLF_L5675_br13_F4121_br06", "trnLF_L5675_br13_F4121_br10", "trnLF_L5675_br14_F4121_br07", "trnLF_L5675_br14_F4121_br10", "trnLF_L5675_br14_F4121_br15", "trnLF_L5675_br15_F4121_br02", "trnLF_L5675_br15_F4121_br07", "trnLF_L5675_br15_F4121_br12", "trnLF_L5675_br16_F4121_br03", "trnLF_L5675_br16_F4121_br10", "trnLF_L5675_br16_F4121_br14", "trnLF_L5675_br16_F4121_br18", "trnLF_L5675_br17_F4121_br01", "trnLF_L5675_br17_F4121_br06", "trnLF_L5675_br17_F4121_br07", "trnLF_L5675_br17_F4121_br13", "trnLF_L5675_br18_F4121_br06", "trnLF_L5675_br18_F4121_br16")

      # # 202310281735 DADA2失敗，merger成功 (8)
      debug_filter_list = c("trnLF_L5675_br01_F4121_br11","trnLF_L5675_br04_F4121_br08","trnLF_L5675_br04_F4121_br11","trnLF_L5675_br05_F4121_br11","trnLF_L5675_br13_F4121_br08","trnLF_L5675_br14_F4121_br11","trnLF_L5675_br15_F4121_br11","trnLF_L5675_br17_F4121_br11")

      # # 202310281735 拿去做2nd denoise的learn error samples (39個)
      # debug_filter_list = c("trnLF_L5675_br12_F4121_br11","trnLF_L5675_br18_F4121_br11","trnLF_L5675_br03_F4121_br11","trnLF_L5675_br07_F4121_br03","trnLF_L5675_br08_F4121_br05","trnLF_L5675_br01_F4121_br05","trnLF_L5675_br08_F4121_br10","trnLF_L5675_br01_F4121_br06","trnLF_L5675_br04_F4121_br15","trnLF_L5675_br05_F4121_br03","trnLF_L5675_br14_F4121_br10","trnLF_L5675_br13_F4121_br03","trnLF_L5675_br05_F4121_br16","trnLF_L5675_br07_F4121_br05","trnLF_L5675_br12_F4121_br17","trnLF_L5675_br16_F4121_br13","trnLF_L5675_br04_F4121_br16","trnLF_L5675_br02_F4121_br15","trnLF_L5675_br09_F4121_br12","trnLF_L5675_br17_F4121_br06","trnLF_L5675_br04_F4121_br04","trnLF_L5675_br07_F4121_br11","trnLF_L5675_br06_F4121_br02","trnLF_L5675_br08_F4121_br12","trnLF_L5675_br14_F4121_br06","trnLF_L5675_br16_F4121_br15","trnLF_L5675_br08_F4121_br07","trnLF_L5675_br01_F4121_br03","trnLF_L5675_br13_F4121_br17","trnLF_L5675_br17_F4121_br01","trnLF_L5675_br15_F4121_br07","trnLF_L5675_br18_F4121_br10","trnLF_L5675_br18_F4121_br14","trnLF_L5675_br10_F4121_br16","trnLF_L5675_br07_F4121_br14","trnLF_L5675_br18_F4121_br01","trnLF_L5675_br05_F4121_br14","trnLF_L5675_br13_F4121_br15","trnLF_L5675_br17_F4121_br13")

      # # 這裡加入debug的filter，可以一併處理到sample跟qc
      # filtering_list = paste0(region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp])
      # if (!filtering_list %in% debug_filter_list){
      #   return(NULL)
      # }

      # 核心運行:denoise
      dadaFs <- dada(r1, err = errF, multithread = TRUE)
      dadaRs <- dada(r2, err = errR, multithread = TRUE)


      paste0(rep(header, length(dadaFs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaFs[["clustering"]][["abundance"]])], rep("_r1_", length(dadaFs[["clustering"]][["abundance"]])), sprintf(dadaFs[["clustering"]][["abundance"]] / sum(dadaFs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaFs[["clustering"]][["abundance"]])), dadaFs[["clustering"]][["abundance"]]) -> r1list
      cbind(r1list, dadaFs[["clustering"]][["sequence"]], dadaFs[["clustering"]][["abundance"]]) -> r1fas
      r1fas[order(as.numeric(r1fas[, 3]), decreasing = TRUE),] -> r1fas
      matrix(r1fas, ncol = 3) -> r1fas
      paste0(rep(header, length(dadaRs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaRs[["clustering"]][["abundance"]])], rep("_r2_", length(dadaRs[["clustering"]][["abundance"]])), sprintf(dadaRs[["clustering"]][["abundance"]] / sum(dadaRs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaRs[["clustering"]][["abundance"]])), dadaRs[["clustering"]][["abundance"]]) -> r2list
      cbind(r2list, dadaRs[["clustering"]][["sequence"]], dadaRs[["clustering"]][["abundance"]]) -> r2fas
      r2fas[order(as.numeric(r2fas[, 3]), decreasing = TRUE),] -> r2fas
      matrix(r2fas, ncol = 3) -> r2fas


      # TODO "只做best的"開關 (暫時不用)

      # # save r1 and r2 seq from dada() results (unnecessary for dada(), but necessary for mergeModule)
      # 匯出denoise後的r1序列，一條序列兩種檔名把檔名，如: "KTHU2084_Wade5880_Calymmodon_societatis_.fas", "fVGF_br01_rECL_br02"
      write.table(r1fas[, 1:2], file = paste0(path_denoise, "/r1/", filename), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)
      # 匯出denoise後的r2序列，一條序列兩種檔名把檔名，如: "KTHU2084_Wade5880_Calymmodon_societatis_.fas", "fVGF_br01_rECL_br02"
      write.table(r2fas[, 1:2], file = paste0(path_denoise, "/r2/", filename), append = FALSE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)

      # 順便存一個(barcodeName,sampleName)的namePair list
      barcode_name = paste(region, amplicon[sample_number, Fp], amplicon[sample_number, Rp], sep = "_")
      sample_name = paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], sep = "_")
      name_pair = paste(barcode_name, sample_name, sep = ",")
      write.table(name_pair, file = paste0(path_denoise, "/denoise_pairs.txt"), append = TRUE, sep = "\n", quote = FALSE,
                  row.names = FALSE, col.names = FALSE)


      # third step: 請DADA2對r1 r2 merge (necessary)
      tryCatch({
        mergers <- mergePairs(dadaFs, r1, dadaRs, r2, minOverlap = minoverlap, verbose = TRUE)
      }, error = function(e) {
        message("Error occurred during mergePairs(): ", conditionMessage(e))
      })

      ####TODO 加上chimera killing (做核的會需要)

      # # parsing merge 結果並存檔
      # 確認merge內資訊，
      # 1. 抓出成功merge的，不是的就記錄在dadamergfail內
      # 2. 抓出abundance最高的ASV存到denoise_best (deprecated)
      if (nrow(mergers) > 0 & max(nchar(mergers$sequence)) > AP_minlength) { #20230624 拿掉" & max(mergers$abundance) > 20"，可以考慮拿到其他步驟當篩選標準
        # parsing
        sum(mergers$abundance) -> clustersum
        paste0(rep(header, length(mergers$abundance)), "_", numbers[1:length(mergers$abundance)], rep("_", length(mergers$abundance)), sprintf(mergers$abundance / clustersum, fmt = '%#.3f'), rep("_abundance_", length(mergers$abundance)), mergers$abundance) -> merglist
        as.matrix(mergers) -> mergers.table
        nchar(mergers.table[, 1]) -> seqlen #Kuo_modified
        cbind(merglist, mergers.table, seqlen) -> fas0 #Kuo_modified
        matrix(fas0, ncol = 11) -> fas0
        fas0[order(as.numeric(fas0[, 3]), decreasing = TRUE),] -> fas0
        matrix(fas0, ncol = 11) -> fas0 #Kuo_modified may write out this matrix
        rbind(merg, fas0) -> merg #Kuo_modified could be a table for dada2merge
        fas0[as.numeric(fas0[, 11]) > AP_minlength,] -> fas #Kuo_modified
        matrix(fas, ncol = 11) -> fas
        if (nrow(fas) == 0) {
          cbind(r1, r2, header) -> fail
          rbind(dadamergfail, fail) -> dadamergfail
        }
        # 存檔rbcLN_result\mergeResult\dada2
        write.table(fas[, 1:2], file = paste0(path_merge, "/dada2/merged/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
      }else {
        cbind(r1, r2, header) -> fail
        rbind(dadamergfail, fail) -> dadamergfail
      }


      # fourth step: 請DADA2對r1 r2 做10N拼接 (unnecessary, because pyhton can do too)
      tryCatch({
        nonmergers <- mergePairs(dadaFs, r1, dadaRs, r2, verbose = TRUE, justConcatenate = TRUE) #Kuo_modified in following lines else
      }, error = function(e) {
        message("Error occurred during mergePairs(): ", conditionMessage(e))
      })

      # # parsing 10Ncat 結果並存檔
      # 確認10Ncat內資訊，
      # 1. 抓出成功cat的，存檔
      # 2. 抓出abundance最高的ASV存到denoise_best (deprecated)
      if (nrow(nonmergers) > 0) {
        # parsing
        sum(nonmergers$abundance) -> clustersum
        paste0(rep(header, length(nonmergers$abundance)), "_", numbers[1:length(nonmergers$abundance)], rep("_", length(nonmergers$abundance)), sprintf(nonmergers$abundance / clustersum, fmt = '%#.3f'), rep("_abundance_", length(nonmergers$abundance)), nonmergers$abundance) -> nonmerglist
        as.matrix(nonmergers) -> nonmergers.table
        cbind(nonmerglist, nonmergers.table) -> fascat #Kuo_modified
        matrix(fascat, ncol = 10) -> fascat
        fascat[order(as.numeric(fascat[, 3]), decreasing = TRUE),] -> fascat #Kuo_modified may write out this matrix
        matrix(fascat, ncol = 10) -> fascat
        rbind(nonmerg, fascat) -> nonmerg #Kuo_modified could be a table for dada2nonmerge
        # 存檔
        write.table(fascat[, 1:2], file = paste0(path_merge, "/merger/nCatR1R2/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
      }

      # 20230611 QC可取代，考慮刪掉
      cbind(rep(r1, length(dadaFs[["clustering"]][["abundance"]])), r1list) -> seqtable01
      cbind(rep(r2, length(dadaRs[["clustering"]][["abundance"]])), r2list) -> seqtable02
      rbind(seqtable, seqtable01, seqtable02) -> seqtable
    }

  }
  stopImplicitCluster()
}