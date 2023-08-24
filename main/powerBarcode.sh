# ! /bin/bash

. /PowerBarcoder/data/result/"$1"/config.sh

# # -----------------------1. prepare env.---------------------
bash checkRequirement.sh "$1"
echo "[INFO] environment OK !"
bash checkDirectory.sh "$1"
echo "[INFO] file directories are created !"
# # ----------------------------------------------------------

echo "[INFO] Start running PowerBarcode !"

# # -----------------------2. demultiplex---------------------
echo "[INFO] start illumina_PE_demultiplex"
bash illumina_PE_demultiplex_all_newprimer.sh "$1"
echo "[INFO] end illumina_PE_demultiplex"
# # ----------------------------------------------------------

sourceDir="${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/trimmed"
outputDir="${resultDataPath}${nameOfLoci[i]}_result/demultiplexResult/reverse_complement"

mkdir -p "$outputDir"

for file in "$sourceDir"/*.fq; do
    filename=$(basename "$file")
    outputfile="$outputDir/${filename%.*}.fq"
    seqkit seq -r -p "$file" -o "$outputfile"
done

# # -----------------------3. denoise-------------------------
cd ${workingDirectory}
echo "[INFO] start dada2_denoise"
Rscript "${workingDirectory}dada2_denoise_PE_newprimer.r" "$ampliconInfo" "$workingDirectory" "$resultDataPath" "$dada2LearnErrorFile" "$dada2BarcodeFile" "$ampliconMinimumLength" "$minimumOverlapBasePair" "${nameOfLoci[@]}" "${primerFName[@]}" "${primerRName[@]}"
echo "[INFO] end dada2_denoise"
# # ----------------------------------------------------------

# # -----------------------4. merge---------------------------
cd ${workingDirectory}
echo "[INFO] start merge.sh"
bash ${workingDirectory}merge.sh "$1"
echo "[INFO] end merge.sh"
# # ----------------------------------------------------------

# # -----------------------5. QC------------------------------
cd ${workingDirectory}
echo "[INFO] start qc.sh"
bash ${workingDirectory}qc.sh "$1"
echo "[INFO] end qc.sh"
# # ----------------------------------------------------------

# # -----------------------6. dev mode------------------------
cd ${workingDirectory}
echo "[INFO] start dev.sh"
bash ${workingDirectory}dev.sh "$1"
echo "[INFO] end dev.sh"
# # ----------------------------------------------------------

echo "[INFO] end of flow"
