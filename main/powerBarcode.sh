# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

# # -----------------------1. prepare env.---------------------
bash ./envCheck/checkRequirement.sh "$1"
echo "[INFO] environment OK !"
bash ./envCheck/checkDirectory.sh "$1"
echo "[INFO] file directories are created !"
# # ----------------------------------------------------------

echo "[INFO] Start running PowerBarcode !"

# # -----------------------2. demultiplex---------------------
echo "[INFO] start illumina_PE_demultiplex"
bash ./demultiplex/illumina_PE_demultiplex_all_newprimer.sh "$1"
echo "[INFO] end illumina_PE_demultiplex"
# # ----------------------------------------------------------

# # -----------------------3. denoise-------------------------
cd ${workingDirectory}
echo "[INFO] start dada2_denoise"
DEFAULT_ERROR_LEARN_PATH=""

if [ "$denoise_mode" == "0" ]; then
    # # -----------------------3.1 default denoise-------------------
    Rscript "${workingDirectory}/denoise/dada2_denoise.r" "$ampliconInfo" "TRUE" "$resultDataPath" "$DEFAULT_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
    echo "[INFO] end dada2_denoise"
elif [ "$denoise_mode" == "1" ]; then
    # # -----------------------3.2 no error learning denoise-------------------
    Rscript "${workingDirectory}/denoise/dada2_denoise.r" "$ampliconInfo" "FALSE" "$resultDataPath" "$DEFAULT_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
    echo "[INFO] end dada2_denoise"
elif [ "$denoise_mode" == "2" ]; then
    # # -----------------------3.3.1. first denoise-------------------
    Rscript "${workingDirectory}/denoise/dada2_denoise.r" "$ampliconInfo" "TRUE" "$resultDataPath" "$DEFAULT_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
    echo "[INFO] end first dada2_denoise"

    # # -----------------------3.3.2 select sequences for second error learning-------------------
    echo "[INFO] start selecting sequences for second error learning"
    for locus in "${nameOfLoci[@]}"; do
        python3 "${workingDirectory}/denoise/error_learning_2nd_selector.py" "$resultDataPath" "$locus"
    done
    echo "[INFO] end selecting sequences for second error learning"

    # # -----------------------3.3.3. second denoise------------------
    echo "[INFO] start second dada2_denoise"
    SECOND_ERROR_LEARN_PATH="${resultDataPath}/${locus}_result/demultiplexResult/error_learning_2nd"
    echo "[INFO] SECOND_ERROR_LEARN_PATH: ${SECOND_ERROR_LEARN_PATH}"
    Rscript "${workingDirectory}/denoise/dada2_denoise.r" "$ampliconInfo" "TRUE" "$resultDataPath" "$SECOND_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}" "${minimumOverlapBasePair[@]}" "${maximumMismatchBasePair[@]}"
    echo "[INFO] end second dada2_denoise"
fi
# # ----------------------------------------------------------

# # -----------------------4. merge---------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}/merge/merge.sh "$1"
echo "[INFO] end merge.sh"
# # ----------------------------------------------------------

# # -----------------------5. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}/qc/qc.sh "$1"
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

## # -----------------------6. dev mode------------------------
#cd ${workingDirectory}
#echo "[INFO] start dev.sh"
#bash ${workingDirectory}/housekeeping/dev.sh "$1"
#echo "[INFO] end dev.sh"
## # ----------------------------------------------------------

echo "[INFO] end of flow"
