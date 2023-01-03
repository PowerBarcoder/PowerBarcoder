# ! /bin/bash
. ./config.sh

bash checkRequirement.sh

echo "environment OK !"
echo "Start running PowerBarcode !"

bash illumina_PE_demultiplex_all_newprimer.sh
