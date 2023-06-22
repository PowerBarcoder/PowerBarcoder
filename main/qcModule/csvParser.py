import csv
import sys

steps = [
    "Cutadapt demultiplex by sample barcode",
    "Cutadapt trim the primer sites",
    "DADA2 filter",
    "DADA2 denoise",
    "DADA2 merge",
    "DADA2 10N concat",
    "Merger blast",
    "Merger merge"
]

filenames = [
    "rbcLN_fVGF_br01_rECL_br01_r1.fq,Co262_Lu30199_Nephrolepis_sp._.fas",
    "rbcLN_fVGF_br01_rECL_br01_r2.fq,KTHU1183_Wade4208_Asplenium_affine_.fas",
    "rbcLN_fVGF_br01_rECL_br02_r1.fq,KTHU1190_Kuo1823_Asplenium_aff._Yoshinagae_.fas",
    "rbcLN_fVGF_br01_rECL_br02_r2.fq,KTHU1190_Kuo1823_Asplenium_aff._Yoshinagae_.fas",
    "rbcLN_fVGF_br01_rECL_br03_r1.fq,KTHU1198_Kuo2054_Asplenium_cymbifolium_.fas"
]

# Define the output file path
output_path = sys.argv[1]+sys.argv[2]+"_result/qcResult/filenames.csv"

# Create a CSV file and write the header
with open(output_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Sample'] + steps)

    # Loop over filenames and steps to fill the CSV
    for filename in filenames:
        files = filename.split(',')
        row_data = [files[0]]

        for step in steps:
            found = "N/A"

            for file in files[1:]:
                if file in step:
                    found = file
                    break

            row_data.append(found)

        writer.writerow(row_data)

print("[INFO] End of parsing csv!")


# KTHU1770_Wade4001_Tomophyllum_repandulum_.fas
# Tomophyllum_repandulum_Wade4001_KTHU1770_01_1.000_abundance_53.fas