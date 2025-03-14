#!/usr/bin/env Rscript

#' DADA2 Paired-End Read Denoising Pipeline
#' 
#' This script implements a DADA2-based pipeline for processing paired-end amplicon sequences:
#' 1. Filters and trims input reads
#' 2. Learns error rates from either custom files or filtered data (optional based on args[2])
#' 3. Denoises forward and reverse reads separately using DADA2
#' 4. Outputs denoised R1 and R2 sequences separately
#' 5. Performs two types of read merging:
#'    a. Standard DADA2 merging with overlap detection
#'    b. Concatenation of unmerged pairs with N spacers
#' 
#' Required arguments:
#' args[1]: Input reads directory
#' args[2]: Use error learning (TRUE/FALSE)
#' args[3]: Output results directory 
#' args[4]: Custom error learning directory path (optional, if empty will use filtered reads)
#' args[5]: Barcode mapping file
#' args[6]: Minimum length threshold
#' args[8+]: Locus-specific parameters (forward primer, reverse primer, min overlap, max mismatch)
#'
#' Note: args[2] (working directory) and args[7] (minimum overlap base pair) are deprecated

# Load required modules
source(paste0(getwd(), "/denoise/constants.R"))
source(paste0(getwd(), "/denoise/install_dependencies.R"))
source(paste0(getwd(), "/denoise/file_utils.R"))
source(paste0(getwd(), "/denoise/dada2_core.R"))

args = commandArgs(trailingOnly = TRUE)

# Main function
main <- function(args) {
  install_dependencies()

  path_of_reads <- args[1]
  use_error_learning <- as.logical(args[2])
  path_of_result <- args[3]

  # (Used for marking abundance sorting, meaning one sample has at most 99 ASVs)
  numbers <- c("01", "02", "03", "04", "05", "06", "07", "08", "09", 10:99)
  AP_minlength <- as.numeric(args[6])
  AP <- prepare_parameters(args)
  print(AP)

  # Read barcode file
  multiplex <- read_barcode_file(path_of_reads, args[5])

  # Loop through all regions specified in AP
  for (a in 1:ncol(AP)) {
    colnames(AP[a]) -> region
    # Extract parameters for the current region
    AP[, a][1] -> Fp
    AP[, a][2] -> Rp
    AP[, a][3] -> minoverlap
    AP[, a][4] -> maxmismatch

    print(paste0("Forward primer: ", Fp, "; Reverse primer: ", Rp, "; Minimum overlap: ", minoverlap, "; Maximum mismatch: ", maxmismatch))

    # Set up file paths
    path_demultiplex <- paste0(path_of_result, region, "_result/demultiplexResult")
    path_denoise <- paste0(path_of_result, region, "_result/denoiseResult")
    path_merge <- paste0(path_of_result, region, "_result/mergeResult")
    path_regional <- paste0(path_of_result, region, "_result/")
    path_trim <- paste0(path_demultiplex, "/trimmed")
    path_filter <- paste0(path_demultiplex, "/filtered")

    # Get lists of file names for R1 and R2 reads
    R1.names <- sort(list.files(path_trim, pattern = ".r1.fq", full.names = FALSE))
    R2.names <- sort(list.files(path_trim, pattern = ".r2.fq", full.names = FALSE))
    R1 <- sort(list.files(path_trim, pattern = ".r1.fq", full.names = TRUE))
    R2 <- sort(list.files(path_trim, pattern = ".r2.fq", full.names = TRUE))
    filtFs <- paste0(path_filter, "/filtered_", R1.names)
    filtRs <- paste0(path_filter, "/filtered_", R2.names)

    # First step: Filter reads in parallel
    filter_reads_parallel(R1, R2, filtFs, filtRs)

    # Second step: Learn error rates from filtered reads (conditional)
    if (use_error_learning) {
      # Get filtered file paths
      filtFs.exists <- filtFs[file.exists(filtFs)]
      filtRs.exists <- filtRs[file.exists(filtRs)]

      # Learn and plot errors using filtered reads
      err_results <- learn_error_rates(filtFs.exists, filtRs.exists, args[4], path_regional, region)
      errF <- err_results$errF
      errR <- err_results$errR

      # Save err matrix to file with locus prefix
      write.table(errF, 
                  file = paste0(path_regional, region, "_error_rate_F.txt"),
                  append = FALSE, sep = "\t", 
                  quote = FALSE, row.names = FALSE, col.names = FALSE)
      write.table(errR, 
                  file = paste0(path_regional, region, "_error_rate_R.txt"),
                  append = FALSE, sep = "\t", 
                  quote = FALSE, row.names = FALSE, col.names = FALSE)
    }

    # Remove rows from the multiplex table where the amplicon column is empty
    multiplex[!multiplex[, AP[, a][2]] %in% "",] -> amplicon

    # Initialize variables for tracking missing samples, sequence table, and DADA2 merge failures
    missing_sample_list <- c()
    seqtable <- c()
    dadamergfail <- c()
    merg <- c()
    nonmerg <- c()

    # Third step: Denoise reads in parallel
    numCores <- detectCores()
    registerDoParallel(cores = numCores)
    foreach(sample_number = 1:nrow(amplicon), .packages = "dplyr") %dopar% {
      # Process each sample in parallel
      # Extract filenames and other parameters for denoising
      sample_filename <- paste0("filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r1.fq")
      r1 <- paste0(path_filter, "/filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r1.fq")
      r2 <- paste0(path_filter, "/filtered_trim_", region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp], "_r2.fq")
      r0 <- paste0(amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp])
      filename = paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], ".fas", sep = "_")    #檔名改跟header一樣
      seqname = paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], sep = "_")           #header的文字
      header = paste0(">", seqname) #加上了header的符號

      #這邊只檢查了r1的名字有沒有對，有對boolean就是TRUE
      if (purrr::has_element(list.files(path = path_filter), sample_filename) == FALSE) {
        # If not, add it to the list of missing samples
        cbind(r1, header) -> mis
        rbind(missing_sample_list, mis) -> missing_sample_list
      }else {

        debug_filter_list <- type_2_debug_filter_list

        # # 這裡加入debug的filter，可以一併處理到sample跟qc
        # filtering_list = paste0(region, "_", amplicon[sample_number, Fp], "_", amplicon[sample_number, Rp])
        # if (!filtering_list %in% debug_filter_list){
        #   return(NULL)
        # }

        # 核心運行:denoise
        if (use_error_learning) {
          dadaFs <- dada(r1, err = errF, multithread = TRUE)
          dadaRs <- dada(r2, err = errR, multithread = TRUE)
        } else {
          dadaFs <- dada(r1, err=NULL, selfConsist = TRUE, multithread = TRUE)
          dadaRs <- dada(r2, err=NULL, selfConsist = TRUE, multithread = TRUE)
        }

        paste0(rep(header, length(dadaFs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaFs[["clustering"]][["abundance"]])], rep("_r1_", length(dadaFs[["clustering"]][["abundance"]])), sprintf(dadaFs[["clustering"]][["abundance"]] / sum(dadaFs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaFs[["clustering"]][["abundance"]])), dadaFs[["clustering"]][["abundance"]]) -> r1list
        cbind(r1list, dadaFs[["clustering"]][["sequence"]], dadaFs[["clustering"]][["abundance"]]) -> r1fas
        r1fas[order(as.numeric(r1fas[, 3]), decreasing = TRUE),] -> r1fas
        matrix(r1fas, ncol = 3) -> r1fas
        paste0(rep(header, length(dadaRs[["clustering"]][["abundance"]])), "_", numbers[1:length(dadaRs[["clustering"]][["abundance"]])], rep("_r2_", length(dadaRs[["clustering"]][["abundance"]])), sprintf(dadaRs[["clustering"]][["abundance"]] / sum(dadaRs[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", length(dadaRs[["clustering"]][["abundance"]])), dadaRs[["clustering"]][["abundance"]]) -> r2list
        cbind(r2list, dadaRs[["clustering"]][["sequence"]], dadaRs[["clustering"]][["abundance"]]) -> r2fas
        r2fas[order(as.numeric(r2fas[, 3]), decreasing = TRUE),] -> r2fas
        matrix(r2fas, ncol = 3) -> r2fas


        # # save r1 and r2 seq from dada() results (unnecessary for dada(), but necessary for merge module)
        # 匯出denoise後的r1序列，一條序列兩種檔名把檔名，如: "KTHU2084_Wade5880_Calymmodon_societatis_.fas", "fVGF_br01_rECL_br02"
        write.table(r1fas[, 1:2], file = paste0(path_denoise, "/r1/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)
        # 匯出denoise後的r2序列，一條序列兩種檔名把檔名，如: "KTHU2084_Wade5880_Calymmodon_societatis_.fas", "fVGF_br01_rECL_br02"
        write.table(r2fas[, 1:2], file = paste0(path_denoise, "/r2/", filename), append = FALSE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)

        # 順便存一個(barcodeName,sampleName)的namePair list
        barcode_name <- paste(region, amplicon[sample_number, Fp], amplicon[sample_number, Rp], sep = "_")
        sample_name <- paste(amplicon[sample_number, 3], amplicon[sample_number, 4], amplicon[sample_number, 2], amplicon[sample_number, 1], sep = "_")
        name_pair <- paste(barcode_name, sample_name, sep = ",")
        write.table(name_pair, file = paste0(path_denoise, "/denoise_pairs.txt"), append = TRUE, sep = "\n", quote = FALSE,
                    row.names = FALSE, col.names = FALSE)


        # fourth step: 請DADA2對r1 r2 merge (necessary)
        tryCatch({
          mergers <- mergePairs(dadaFs, r1, dadaRs, r2, minOverlap = minoverlap, verbose = TRUE, maxMismatch = maxmismatch)
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


        # fifth step: 請DADA2對r1 r2 做10N拼接 (unnecessary, because pyhton can do too)
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
}

# Execute main function
main(args)
