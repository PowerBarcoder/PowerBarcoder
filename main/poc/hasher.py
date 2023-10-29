import hashlib

file_path_1 = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738/trnLF_result/demultiplexResult/test/filtered_trim_trnLF_L5675_br01_F4121_br03_r1.fq"
file_path_2 = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310291246/trnLF_result/demultiplexResult/filtered/filtered_trim_trnLF_L5675_br01_F4121_br03_r1.fq"

with open(file_path_1, "r") as file:  # 計算hash，須獨立拿出讀，不然readlines讀完指針就已經讀到底了，後面hash等於拿空的東西去算
    file_content_hash = hashlib.md5(file.read().encode()).hexdigest()
    print(file_content_hash)

with open(file_path_2, "r") as file:
    file_content_hash = hashlib.md5(file.read().encode()).hexdigest()
    print(file_content_hash)
