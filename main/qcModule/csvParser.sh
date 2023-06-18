#! /bin/bash

. ./config.sh

echo "[INFO] Start to parse csv !"
# Define the steps and filenames
steps=(
  "Cutadapt demultiplex by sample barcode,"
  "Cutadapt trim the primer sites,"
  "DADA2 filter,"
  "DADA2 denoise,"
  "DADA2 merge,"
  "DADA2 10N concat,"
  "Merger blast,"
  "Merger merge"
)

# Define the filenames for each step
filenames=(
  "rbcLN_fVGF_br01_rECL_br01_r1.fq,Co262_Lu30199_Nephrolepis_sp._.fas"
  "rbcLN_fVGF_br01_rECL_br01_r2.fq,KTHU1183_Wade4208_Asplenium_affine_.fas"
  "rbcLN_fVGF_br01_rECL_br02_r1.fq,KTHU1190_Kuo1823_Asplenium_aff._Yoshinagae_.fas"
  "rbcLN_fVGF_br01_rECL_br02_r2.fq,KTHU1190_Kuo1823_Asplenium_aff._Yoshinagae_.fas"
  "rbcLN_fVGF_br01_rECL_br03_r1.fq,KTHU1198_Kuo2054_Asplenium_cymbifolium_.fas"
)

# Create a CSV file
echo "Sample,${steps[*]}" > ${resultDataPath}/filenames.csv

# Loop over filenames and steps to fill the CSV
for filename in "${filenames[@]}"; do
  IFS=',' read -r -a files <<< "$filename"
  echo -n "${files[0]}" >> ${resultDataPath}/filenames.csv
  for step in "${steps[@]}"; do
    found="N/A"
    for file in "${files[@]:1}"; do
      if [[ "$step" == *"$file"* ]]; then
        found="$file"
        break
      fi
    done
    echo -n ",$found" >> ${resultDataPath}/filenames.csv
  done
  echo "" >> ${resultDataPath}/filenames.csv
done

echo "[INFO] End of parsing csv !"