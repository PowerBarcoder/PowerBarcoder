# ! /bin/bash

for file in /home2/analyses/BIFA/rbcL_for_merge/rbcLN_single/*; do
    base=$(basename "$file")
    head -n 2 "$file" > "/home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result_rbcL_final/rbcLN_demultiplex/denoice_best/nonmerged/r1/$base"
done

for file in /home2/analyses/BIFA/rbcL_for_merge/rbcLC_single/*; do
    base=$(basename "$file")
    head -n 2 "$file" > "/home2/barcoder_test/RUN_sk_20230111_10N/PowerBarcoder/result_rbcL_final/rbcLN_demultiplex/denoice_best/nonmerged/r2/$base"
done
