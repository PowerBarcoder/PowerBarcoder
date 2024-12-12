# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

# # -----------------------1. prepare env.---------------------
bash ./envCheckModule/checkRequirement.sh "$1"
echo "[INFO] environment OK !"
bash ./envCheckModule/checkDirectory.sh "$1"
echo "[INFO] file directories are created !"
# # ----------------------------------------------------------

echo "[INFO] Start running PowerBarcode !"

# # -----------------------2. demultiplex---------------------
echo "[INFO] start illumina_PE_demultiplex"
bash ./demultiplexModule/illumina_PE_demultiplex_all_newprimer.sh "$1"
echo "[INFO] end illumina_PE_demultiplex"
# # ----------------------------------------------------------

# # -----------------------3. first denoise-------------------
cd ${workingDirectory}
echo "[INFO] start first dada2_denoise"
DEFAULT_ERROR_LEARN_PATH=""
Rscript "${workingDirectory}/denoiseModule/dada2_denoise_PE_newprimer.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$DEFAULT_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
echo "[INFO] end first dada2_denoise"

# # -----------------------3.5 select sequences for second error learning-------------------
echo "[INFO] start selecting sequences for second error learning"
for locus in "${nameOfLoci[@]}"; do
    python3 "${workingDirectory}/denoiseModule/error_learning_2nd_selector.py" "$resultDataPath" "$locus"
done
echo "[INFO] end selecting sequences for second error learning"

# # -----------------------4. second denoise------------------
cd ${workingDirectory}
echo "[INFO] start second dada2_denoise"
SECOND_ERROR_LEARN_PATH="${resultDataPath}/error_learning_2nd"
Rscript "${workingDirectory}/denoiseModule/dada2_denoise_PE_newprimer.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$SECOND_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
echo "[INFO] end second dada2_denoise"

# # -----------------------5. merge---------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}/mergeModule/merge.sh "$1"
echo "[INFO] end merge.sh"
# # ----------------------------------------------------------

# # -----------------------6. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}/qcModule/qc.sh "$1"
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

## # -----------------------7. dev mode------------------------
#cd ${workingDirectory}
#echo "[INFO] start dev.sh"
#bash ${workingDirectory}/housekeepingModule/dev.sh "$1"
#echo "[INFO] end dev.sh"
## # ----------------------------------------------------------

echo "[INFO] end of flow"
