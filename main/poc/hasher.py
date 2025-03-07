import hashlib


def get_file_hash(file_path: str) -> str:
    with open(file_path, "r") as file:
        file_content_hash = hashlib.md5(file.read().encode()).hexdigest()
        return file_content_hash


file_path_1 = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738/trnLF_result/demultiplexResult/test/filtered_trim_trnLF_L5675_br01_F4121_br03_r1.fq"
file_path_2 = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310291246/trnLF_result/demultiplexResult/filtered/filtered_trim_trnLF_L5675_br01_F4121_br03_r1.fq"


def get_line_hash(file_path: str) -> str:
    # 計算best seq. hash，須獨立拿出讀，不然readlines讀完指針就已經讀到底了，後面hash等於拿空的東西去算
    line_number = 2
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            if i + 1 == line_number:
                line_hash = hashlib.md5(line.encode()).hexdigest()
                break
        return line_hash


def get_string_hash(test_string: str) -> str:
    return hashlib.md5(test_string.encode()).hexdigest()


if __name__ == "__main__":
    fasta_string = "AAGCTGGTGTCAAAGATTATCGGCTGAACTATTACACCCCCGAGTACAAGACCAAAGATACCGATATATTAGCAGCCTCCAGAATGACCCCACAACCCGGAGTACCGGCTGAGGAGGCCGGAGCTGCGGTAGCTGCAGAATCCTCTACGGGTACGTGGACCACCGTATGGACAGATGGGTTGACTAGTCTTGATCGTTACAAGGGCCGATGCTACGACATCGAACCCGTCGCCGGGGAAGAGAACCAGTATATCGCATATGTAGCTNNNNNNNNNNAGCTTATCCTTTGGATCTCTTCGAAGAAGGTTCCGTCACCAATTTGTTCACCTCCATTGTAGGTAATGTTTTCGGATTTAAAGCTCTACGCGCCTTACGCTTGGAAGACCTTCGAATTCCTCCTGCTTATTCTAAAACTTTCATTGGACCGCCTCACGGTATTCAGGTCGAAAGGGATAAATTGAACAAATATGGACGCCCTTTATTGGGATGTACAATCAAGCCAAAATTAGGTCTGTCTGCTAAAAATTATGGTAGAGCCGTCTAC"
    print(get_string_hash(fasta_string))
