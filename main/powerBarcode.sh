# ! /bin/bash
. ./config.sh

bash checkRequirement.sh

echo "environment OK !"

bash checkDirectory.sh

echo "file directories are created !"

echo "Start running PowerBarcode !"

bash illumina_PE_demultiplex_all_newprimer.sh
