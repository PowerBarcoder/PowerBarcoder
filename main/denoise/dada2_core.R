
#' Learn error rates from either custom files or filtered reads
#' @param filtFs.exists List of existing filtered forward read files
#' @param filtRs.exists List of existing filtered reverse read files
#' @param error_learn_path Optional path to custom error learning files
#' @param path_regional Path for saving error rate plots
#' @param region Region/locus name for plot filenames
#' @return List containing error rate matrices for forward and reverse reads
learn_error_rates <- function(filtFs.exists, filtRs.exists, error_learn_path, path_regional, region) {
  # Determine which files to use for error learning
  if (!is.null(error_learn_path) && error_learn_path != "" && dir.exists(error_learn_path)) {
    print(paste0("[INFO] Using custom error learning path: ", error_learn_path))
    errF.files <- list.files(error_learn_path, pattern = "r1", full.names = TRUE)
    errR.files <- list.files(error_learn_path, pattern = "r2", full.names = TRUE)
  } else {
    print("[INFO] Using filtered reads for error learning")
    errF.files <- filtFs.exists
    errR.files <- filtRs.exists
  }
  
  # Learn and plot forward read errors
  errF <- learnErrors(errF.files, multithread = TRUE)
  png(paste0(path_regional, region, "_error_rate_F.png"))
  plotErrors(errF, nominalQ = TRUE)
  dev.off()
  
  # Learn and plot reverse read errors
  errR <- learnErrors(errR.files, multithread = TRUE)
  png(paste0(path_regional, region, "_error_rate_R.png"))
  plotErrors(errR, nominalQ = TRUE)
  dev.off()
  
  return(list(errF=errF, errR=errR))
}

#' Filter paired-end reads in parallel using DADA2
#' @param R1 List of forward read FASTQ files
#' @param R2 List of reverse read FASTQ files 
#' @param filtFs Output filenames for filtered forward reads
#' @param filtRs Output filenames for filtered reverse reads
#' @return None, writes filtered files to disk
filter_reads_parallel <- function(R1, R2, filtFs, filtRs) {
  numCores <- detectCores()
  registerDoParallel(cores = numCores)
  foreach(i = seq_along(R1), .packages = "dada2") %dopar% {
    fastqPairedFilter(c(R1[i], R2[i]), c(filtFs[i], filtRs[i]),
                      verbose = TRUE, matchIDs = TRUE, compress = FALSE)
  }
  stopImplicitCluster()
}
