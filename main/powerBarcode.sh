# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

# # -----------------------1. prepare env.---------------------
bash checkRequirement.sh "$1"
echo "[INFO] environment OK !"
bash checkDirectory.sh "$1"
echo "[INFO] file directories are created !"
# # ----------------------------------------------------------

#echo "[INFO] Start running PowerBarcode !"
#
## # -----------------------2. demultiplex---------------------
#echo "[INFO] start illumina_PE_demultiplex"
#bash illumina_PE_demultiplex_all_newprimer.sh "$1"
#echo "[INFO] end illumina_PE_demultiplex"
## # ----------------------------------------------------------
#
## # -----------------------3. denoise-------------------------
#cd ${workingDirectory}
#echo "[INFO] start dada2_denoise"
#Rscript "${workingDirectory}dada2_denoise_PE_newprimer.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$dada2LearnErrorFile" "$dada2BarcodeFile" "$ampliconMinimumLength" "$minimunOverlapBasePair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}"
#echo "[INFO] end dada2_denoise"
## # ----------------------------------------------------------
#
## # -----------------------4. merge---------------------------
#cd ${workingDirectory}
#echo "[INFO] start merge.sh"
#bash ${workingDirectory}merge.sh "$1"
#echo "[INFO] end merge.sh"
## # ----------------------------------------------------------

# # -----------------------5. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}qc.sh "$1"
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

echo "[INFO] end of flow"
