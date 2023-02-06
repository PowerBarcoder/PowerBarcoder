# ! /bin/bash
. ./config.sh

#bash checkRequirement.sh
#
#echo "[INFO] environment OK !"
#
bash checkDirectory.sh
#
#echo "[INFO] file directories are created !"
#
#echo "[INFO] Start running PowerBarcode !"
#
## # -----------------------執行demultiplex-----------------------------
#echo "[INFO] start illumina_PE_demultiplex"
#bash illumina_PE_demultiplex_all_newprimer.sh
#echo "[INFO] end illumina_PE_demultiplex"
#
## # -----------------------執行denoise-----------------------------
#cd ${workingDirectory}
#echo "[INFO] start dada2_denoise"
#Rscript ${workingDirectory}dada2_denoise_PE_newprimer.r $ampliconInfo $workingDirectory $resultDataPath $dada2LearnErrorFile $dada2BarcodeFile ${nameOfLoci[@]} > ${resultDataPath}log_dada2.txt
#echo "[INFO] end dada2_denoise"

# # -----------------------執行merge-----------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}merge.sh
echo "[INFO] end merge.sh"

echo "[INFO] end of flow"