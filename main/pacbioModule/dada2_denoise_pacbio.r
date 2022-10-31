library("devtools")
library("dada2")

# 20221015直接吃這個檔案試試看，比較快

#learn error rate pacbio
path_el <- "/home/lykuo/lab_data/NGS_data/Pacbio/error_learn/pacbio/SuperRed_35"
path_reads <- "/home/lykuo/lab_data/NGS_data/Pacbio/"
list.files(path_el)-> fq
paste0(path_el,fq)-> fqfiles
err <- learnErrors(fqfiles, errorEstimationFunction=PacBioErrfun, multithread=FALSE)

numbers = c("01", "02", "03", "04", "05", "06", "07", "08", "09", 10:99)

rbcL = c("fVGF", "rVVG")
trnLLF = c("L0725", "F4121")
AP<-data.frame(rbcL, trnLLF)
multiplex <- as.matrix(read.table(
  "multiplex_clean.txt",
  sep="\t", header = TRUE))
for (a in 1:ncol(AP)){
  colnames(AP[a]) -> region
  AP[,a][1] -> Fp
  AP[,a][2] -> Rp
  multiplex[!multiplex[,AP[,a][1]] %in% "",] -> amplicon
  miss = c()
  seqtable = c()
  path_demultiplex = paste0(path_reads, region, "_demultiplex")
  path_trim <- paste0(path_demultiplex, "/trimmed")
  for (s in 1:nrow(amplicon)){
    trim_reads = paste0("trim_dd_",region, "_", amplicon[s,Fp],"_", amplicon[s,Rp], ".fq")
    filename = paste(amplicon[s,"Databaseno..name_on_the_tube."], amplicon[s,"Collection_no."], amplicon[s,"Genus"], amplicon[s,"X.Infra.Species"], ".fas", sep = "_")
    readfilename = paste(amplicon[s,"Databaseno..name_on_the_tube."], amplicon[s,"Collection_no."], amplicon[s,"Genus"], amplicon[s,"X.Infra.Species"], ".fas", sep = "_")
    seqname = paste(amplicon[s,"Genus"], amplicon[s,"X.Infra.Species"], amplicon[s,"Collection_no."], amplicon[s,"Databaseno..name_on_the_tube."], sep = "_")
    header = paste0(">",seqname)
    if (purrr::has_element(list.files(path= path_trim),trim_reads)==TRUE)
    trim_reads_file = paste0(path_trim, "/", trim_reads)
	dadas <- dada(trim_reads_file, err=err, multithread=TRUE)
	#try(dadas <- removeBimeraDenovo(dadas, multithread=TRUE, verbose=TRUE))# not yet test this function 
    length(dadas[["clustering"]][["abundance"]]) -> seqnumber
    rlist <- paste0(rep(header, seqnumber), "_", numbers[1:seqnumber], rep("_", seqnumber), sprintf(dadas[["clustering"]][["abundance"]]/sum(dadas[["clustering"]][["abundance"]]), fmt = '%#.3f'), rep("_abundance_", seqnumber), dadas[["clustering"]][["abundance"]])
    cbind (rep(trim_reads, seqnumber),rlist)-> seqtable0
    rbind(seqtable, seqtable0)-> seqtable
    cbind(rlist,dadas[["clustering"]][["sequence"]],dadas[["clustering"]][["abundance"]])-> rfas
	  rfas[order(rfas[,3])]
    write.table(rfas[,1:2], file = paste0(path_demultiplex,"/denoice/",readfilename), append = FALSE, sep = "\n", quote = FALSE,
                row.names = FALSE, col.names = FALSE)
    write.table(rfas[1,1:2], file = paste0(path_demultiplex,"/denoice_best/",readfilename), append = FALSE, sep = "\n", quote = FALSE,
                row.names = FALSE, col.names = FALSE)
    }
	if (purrr::has_element(list.files(path= path_trim),trim_reads)==FALSE){
	cbind(trim_reads, header)-> mis
	rbind(miss, mis)-> miss
	  }
  }
  write.table(miss, file = paste0(path_demultiplex,"/denoice/missing_samples.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
  write.table(seqtable, file = paste0(path_demultiplex,"/denoice/sequence_table.txt"), append = FALSE, sep = "\t", quote = FALSE,
              row.names = FALSE, col.names = FALSE)
}