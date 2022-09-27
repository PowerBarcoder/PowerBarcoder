#! /bin/bash

# 傳參寫法
# one=1
# two=2
# three=3
# python3 ./mergeModule/test.py $one $two $three
# sh ./mergeModule/00_blastForRef.sh $one $two $three

. ./config.sh

sh ./mergeModule/00_blastForRef.sh
python3 ./mergeModule/BlastResult.py $mainDataPath
python3 ./mergeModule/BeforeAlignment.py $mainDataPath $sseqidFileName
python3 ./mergeModule/Alignment.py $mainDataPath
python3 ./mergeModule/merge.py $mainDataPath







# # 不需要For loop，我裡面已經處理好了
# # for File in *r1.fq
# # 	do
# #     python3 ./mergeModule/BeforeAlignment.py
# #     python3 ./mergeModule/Alignment.py
# #     python3 ./mergeModule/merge.py
# # 	done
# # 不需要For loop，我裡面已經處理好了