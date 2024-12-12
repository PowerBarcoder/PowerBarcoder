#' Learn error rates and generate error plots from sequencing data
#' @param file_list List of FASTQ files to learn errors from
#' @param result_path Path where to save the error plot
#' @param output_suffix Suffix for the output plot filename
#' @return Error rate matrix learned from the data
learn_and_plot_errors <- function(file_list, result_path, output_suffix) {
  err <- learnErrors(file_list, multithread = TRUE)
  png(paste0(result_path, output_suffix))
  plotErrors(err, nominalQ = TRUE)
  dev.off()
  return(err)
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
