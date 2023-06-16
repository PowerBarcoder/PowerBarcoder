# ! /bin/bash
. ./config.sh

# # -----------------------1. prepare env.---------------------
bash checkRequirement.sh
echo "[INFO] environment OK !"
bash checkDirectory.sh
echo "[INFO] file directories are created !"
# # ----------------------------------------------------------

echo "[INFO] Start running PowerBarcode !"

# # -----------------------2. demultiplex---------------------
echo "[INFO] start illumina_PE_demultiplex"
bash illumina_PE_demultiplex_all_newprimer.sh
echo "[INFO] end illumina_PE_demultiplex"
# # ----------------------------------------------------------

# # -----------------------3. denoise-------------------------
cd ${workingDirectory}
echo "[INFO] start dada2_denoise"
Rscript "${workingDirectory}dada2_denoise_PE_newprimer.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$dada2LearnErrorFile" "$dada2BarcodeFile" "${nameOfLoci[@]}"
echo "[INFO] end dada2_denoise"
# # ----------------------------------------------------------

# # -----------------------4. merge---------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}merge.sh
echo "[INFO] end merge.sh"
# # ----------------------------------------------------------

# # -----------------------5. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}qc.sh
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

echo "[INFO] end of flow"
