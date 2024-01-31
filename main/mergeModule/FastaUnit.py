# 直接用NCBI的fasta即可，這裡會轉出edit版，再用edit版生成seqID&seqlist

import linecache
import os


class FastaUnit:

    def __init__(self):
        self.seq_map = {}

    # 把fasta存成一行一行的檔案
    def save_fasta_unit_as_file(self, load_path, save_dir):
        file = load_path
        file_name = ""
        if "/" in file:
            file_name = file.split("/")[-1]
        elif "\\" in file:
            file_name = file.split("\\")[-1]

        count = len(open(file).readlines())
        for i in range(1, count + 1):
            text = linecache.getline(file, i)
            x = text.replace("\n", "")
            # print(x)
            with open(save_dir + file_name, "a") as file_edit:
                if ">" in x and i != 1:
                    file_edit.write("\n" + x + "\n")
                elif ">" in x and i == 1:
                    file_edit.write(x + "\n")
                else:
                    file_edit.write(x)

    # 把fasta轉成一行一行的map物件

    def fasta_unit(self, load_path):
        seq_map = {}
        # 製作所有序列的map
        seq_header = ""
        seq_read = ""
        count = len(open(load_path).readlines())
        for i in range(1, count + 1):
            text = linecache.getline(load_path, i)
            x = text.replace("\n", "")
            # 不是第一行的header
            if ">" in x and i != 1:
                seq_header = x
                seq_read = ""
            # 第一行的header
            elif ">" in x and i == 1:
                seq_header = x
                seq_read = ""
            else:
                seq_read = seq_read + x
                seq_map[seq_header] = seq_read
            # seq_map = dict(zip(seq_header, seq_read))
        self.seq_map = seq_map
        return self

    """
    get file name from path without extension
    """

    def get_file_name_from_path(self, path):
        file_name = ""
        if "/" in path:
            file_name = path.split("/")[-1]
        elif "\\" in path:
            file_name = path.split("\\")[-1]
        return ".".join(file_name.split(".")[:-1])

    """
    get file extension from path
    """

    def get_file_extension_from_path(self, path):
        extension = ""
        if "/" in path:
            extension = path.split(".")[-1]
        return extension

    """
    Split a fasta with multiple sequences into separated file with one line header and one line sequence data.
    Input supported for sequence data with multiple lines (such as the alignment result file in MAFFT).  
    """

    def split_multiple_seq_fasta_into_files(self, load_path, save_dir):
        file_name = self.get_file_name_from_path(load_path)
        extension = self.get_file_extension_from_path(load_path)
        count = len(open(load_path).readlines())
        file_serial_number = 1
        with open(load_path, "r") as file:
            buffered_text = ""
            for i, line in enumerate(file, start=1):
                text = line.rstrip("\n")
                if ">" in text and i != 1:  # not first line header
                    with open(save_dir + file_name + "_" + str(file_serial_number) + "." + extension, "w") as file_edit:
                        file_edit.write(buffered_text)
                        file_serial_number += 1
                    buffered_text = ""
                    buffered_text += (text + "\n")
                elif ">" in text and i == 1:  # first line header
                    buffered_text = ""
                    buffered_text += (text + "\n")
                elif ">" not in text and i != count:  # not last line seq
                    buffered_text += text
                else:  # last line seq
                    buffered_text += text
                    with open(save_dir + file_name + "_" + str(file_serial_number) + "." + extension, "w") as file_edit:
                        file_edit.write(buffered_text)
                        file_serial_number += 1

    """
    Replace filename with the sequence header at the first line.
    Notice: If you have multiple sequences, we only parse the file one's header 
    """

    def replace_filename_with_header(self, load_path, output_dir, delete_original_file=False):
        extension = self.get_file_extension_from_path(load_path)
        with open(load_path, "r") as input_file:
            header_text = linecache.getline(load_path, 1)[1:].replace("\n", "")
            with open(output_dir + header_text + "." + extension, "w") as output_file:
                for line in input_file:
                    output_file.write(line)
        if delete_original_file:
            os.remove(load_path)

    # input_path = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/raw/KTHU2220_Wade5673_Tectaria_pleiosora_.fas'
    # output_dir = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/'
    # input_path2 = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/raw/KTHU1778_Liu9858_Cephalomanes_oblongifolium_.fas_r2.al'
    # output_dir2 = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/'

    # input_path3 = 'C:/Users/kwz50/Desktop/i18n/workTool/seq/1Tectaria_pleiosora_Wade5673_KTHU2220_01_0.491_abundance_276_10Ncat.fas'

    # split_multiple_seq_fasta_into_files(input_path2, output_dir2)

    # replace_filename_with_header(input_path3,output_dir,True)
