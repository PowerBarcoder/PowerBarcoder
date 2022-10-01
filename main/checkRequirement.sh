# ! /bin/bash
. ./config.sh


echo "checking reuirement..."

# # check fastp 先跳過，看起來要切路徑到miniconda
# currentPath=$(pwd)
# echo $(pwd)
# cd $myFastpPath
# cd $myFastpPath
# echo $currentPath

# wherewIsCutadapt=$(cd /home/lykuo/miniconda2/bin/)
# checkCutadapt=${#wherewIsCutadapt}
# lengthOfCutadapt=10
# echo ${checkCutadapt}
# # echo $(whereis cutadapt|#)
# if [ $checkCutadapt -le $lengthOfCutadapt ]; then
#     exit "Pipeline terminated because cutadapt is not found"
# fi


# check cutadapt
wherewIsCutadapt=$(whereis cutadapt)
checkCutadapt=${#wherewIsCutadapt}
lengthOfCutadapt=10
# echo $(whereis cutadapt|#)
if [ $checkCutadapt -le $lengthOfCutadapt ]; 
then
    exit "Pipeline terminated because cutadapt is not found"
else
    echo "cutadapt installed"
fi


# check makeblastdb
wherewIsMakeblastdb=$(whereis makeblastdb)
checkMakeblastdb=${#wherewIsMakeblastdb}
lengthOfMakeblastdb=12
# echo $(whereis cutadapt|#)
if [ $checkMakeblastdb -le $lengthOfMakeblastdb ]; 
then
    exit "Pipeline terminated because makeblastdb is not found"
else
    echo "makeblastdb installed"
fi


# check blastn
wherewIsBlastn=$(whereis blastn)
checkBlastn=${#wherewIsBlastn}
lengthOfBlastn=7
# echo $(whereis cutadapt|#)
if [ $checkBlastn -le $lengthOfBlastn ]; 
then
    exit "Pipeline terminated because blastn is not found"
else
    echo "blastn installed"
fi


# check mafft
wherewIsMafft=$(whereis mafft)
checkMafft=${#wherewIsMafft}
lengthOfMafft=6
# echo $(whereis cutadapt|#)
if [ $checkMafft -le $lengthOfMafft ]; 
then
    exit "Pipeline terminated because mafft is not found"
else
    echo "mafft installed"
fi

