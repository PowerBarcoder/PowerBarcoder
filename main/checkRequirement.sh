# ! /bin/bash

echo "[INFO] checking reuirement..."

# check fastp
wherewIsFastp=$(whereis fastp)
checkFastp=${#wherewIsFastp}
lengthOfFastp=10
# echo $(whereis fastp|#)
if [ $checkFastp -le $lengthOfFastp ]; then
  exit "[WARNING] Pipeline terminated because fastp is not found"
else
  echo "[INFO] fastp installed"
fi

# check cutadapt
wherewIsCutadapt=$(whereis cutadapt)
checkCutadapt=${#wherewIsCutadapt}
lengthOfCutadapt=10
# echo $(whereis cutadapt|#)
if [ $checkCutadapt -le $lengthOfCutadapt ]; then
  exit "[WARNING] Pipeline terminated because cutadapt is not found"
else
  echo "[INFO] cutadapt installed"
fi

# check makeblastdb
wherewIsMakeblastdb=$(whereis makeblastdb)
checkMakeblastdb=${#wherewIsMakeblastdb}
lengthOfMakeblastdb=12
# echo $(whereis cutadapt|#)
if [ $checkMakeblastdb -le $lengthOfMakeblastdb ]; then
  exit "[WARNING] Pipeline terminated because makeblastdb is not found"
else
  echo "[INFO] makeblastdb installed"
fi

# check blastn
wherewIsBlastn=$(whereis blastn)
checkBlastn=${#wherewIsBlastn}
lengthOfBlastn=7
# echo $(whereis cutadapt|#)
if [ $checkBlastn -le $lengthOfBlastn ]; then
  exit "[WARNING] Pipeline terminated because blastn is not found"
else
  echo "[INFO] blastn installed"
fi

# check mafft
wherewIsMafft=$(whereis mafft)
checkMafft=${#wherewIsMafft}
lengthOfMafft=6
# echo $(whereis cutadapt|#)
if [ $checkMafft -le $lengthOfMafft ]; then
  exit "[WARNING] Pipeline terminated because mafft is not found"
else
  echo "[INFO] mafft installed"
fi

# check seqkit
wherewIsSeqkit=$(whereis seqkit)
checkSeqkit=${#wherewIsSeqkit}
lengthOfSeqkit=10
# echo $(whereis cutadapt|#)
if [ $checkSeqkit -le $lengthOfSeqkit ]; then
  exit "[WARNING] Pipeline terminated because seqkit is not found"
else
  echo "[INFO] seqkit installed"
fi

# check seqtk
wherewIsSeqtk=$(whereis seqtk)
checkSeqtk=${#wherewIsSeqtk}
lengthOfSeqtk=10
# echo $(whereis cutadapt|#)
if [ $checkSeqtk -le $lengthOfSeqtk ]; then
  exit "[WARNING] Pipeline terminated because seqtk is not found"
else
  echo "[INFO] seqtk installed"
fi
