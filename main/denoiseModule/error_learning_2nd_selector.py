"""
 此腳本預計置於 dada2_denoise_PE_newprimer.r 後執行，
    用以篩選出供第二次error learning 使用的序列，並將符合條件之置檔名其輸出至一txt檔案中。

 運行邏輯：
    1. 按以下指標從 {$resultDataPath}\{$loci}_result\denoiseResult中，找出DADA2 denoise r1 與 r2 的結果中篩選出符合條件之序列
    - [ ]  best ASV reads number：r1/r2>0.05 且 r2/r1>20
    - [ ]  best ASV reads number：r1或r2至少有一個要>20
    - [ ]  best ASV propotion：r1或r2至少有一個>0.95
    2. 將符合條件之序列檔名輸出至一txt檔案中，供第二次error learning使用
"""

