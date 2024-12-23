#' Read and parse a barcode mapping file
#' @param path_of_reads Path containing the barcode file
#' @param barcode_file Name of the barcode mapping file
#' @return Data frame containing barcode mappings
read_barcode_file <- function(path_of_reads, barcode_file) {
  barcode_file_path <- paste0(path_of_reads, barcode_file)
  return(read.table(barcode_file_path, sep = "\t", header = TRUE))
}

#' Prepare analysis parameters from command line arguments
#' @param args Command line arguments containing locus information
#' @return Data frame with 4 rows (forward primers, reverse primers, min overlap, max mismatch)
#'         and columns for each locus
prepare_parameters <- function(args) {
  loci_count <- length(args[8:length(args)]) / 5
  locus_names <- args[8:(8 + loci_count - 1)]
  locus_elements <- args[(8 + loci_count):(8 + (loci_count * 3) - 1)]
  locus_minimum_overlap_base_pair <- args[(8 + (loci_count * 3)):(8 + (loci_count * 4) - 1)]
  locus_maximum_mismatch_base_pair <- args[(8 + (loci_count * 4)):(8 + (loci_count * 5) - 1)]

  AP <- data.frame(matrix(nrow = 4, ncol = length(locus_names)))
  colnames(AP) <- locus_names
  AP[1,] <- locus_elements[1:(length(locus_elements) %/% 2)]
  AP[2,] <- locus_elements[((length(locus_elements) %/% 2) + 1):length(locus_elements)]
  AP[3,] <- locus_minimum_overlap_base_pair
  AP[4,] <- locus_maximum_mismatch_base_pair

  return(AP)
}
