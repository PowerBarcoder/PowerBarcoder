# ! /bin/bash
. ./config.sh

bash checkRequirement.sh

echo "environment OK !"

bash checkDirectory.sh

echo "file directories are created !"

echo "Start running PowerBarcode !"

## # -----------------------執行demultiplex-----------------------------
#echo "start illumina_PE_demultiplex"
#bash illumina_PE_demultiplex_all_newprimer.sh
#echo "end illumina_PE_demultiplex"

## # -----------------------轉去執行R-----------------------------
#cd ${workingDirectory}
#echo "start dada2_denoise"
#Rscript ${workingDirectory}dada2_denoise_PE_newprimer.r $ampliconInfo $workingDirectory $resultDataPath $dada2LearnErrorFile $dada2BarcodeFile ${nameOfLoci[@]} > ${resultDataPath}log_dada2.txt
#echo "end dada2_denoise"

# # -----------------------nonmerge的要來執行python-----------------------------
cd ${workingDirectory}
echo "start merge.sh"
bash ${workingDirectory}merge.sh
echo "end merge.sh"

echo "end of flow"