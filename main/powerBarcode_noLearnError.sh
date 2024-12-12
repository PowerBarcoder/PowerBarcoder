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

# # -----------------------3. denoise-------------------------
cd ${workingDirectory}
echo "[INFO] start dada2_denoise"
DEFAULT_ERROR_LEARN_PATH=""
Rscript "${workingDirectory}/denoiseModule/dada2DenoiserNoLearnError.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$DEFAULT_ERROR_LEARN_PATH" "$dada2BarcodeFile" "$amplicon_minimum_length" "$minimum_overlap_base_pair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}"
echo "[INFO] end dada2_denoise"
# # ----------------------------------------------------------

# # -----------------------4. merge---------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}/mergeModule/merge.sh "$1"
echo "[INFO] end merge.sh"
# # ----------------------------------------------------------

# # -----------------------5. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}/qcModule/qc.sh "$1"
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

# # -----------------------6. dev mode------------------------
cd ${workingDirectory}
echo "[INFO] start dev.sh"
bash ${workingDirectory}/housekeepingModule/dev.sh "$1"
echo "[INFO] end dev.sh"
# # ----------------------------------------------------------

echo "[INFO] end of flow"
