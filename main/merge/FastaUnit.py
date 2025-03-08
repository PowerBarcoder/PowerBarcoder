# 直接用NCBI的fasta即可，這裡會轉出edit版，再用edit版生成seqID&seqlist

import linecache
import os


def save_fasta_unit_as_file(load_path, save_dir):
    """
    Saves a FASTA file as a series of line-by-line files.

    :param load_path: Path to the input FASTA file.
    :type load_path: str
    :param save_dir: Directory where the line-by-line files will be saved.
    :type save_dir: str
    """
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


def get_file_name_from_path(path):
    """
    Gets the file name from a path without the extension.

    :param path: The file path.
    :type path: str
    :return: The file name without the extension.
    :rtype: str
    """
    file_name = ""
    if "/" in path:
        file_name = path.split("/")[-1]
    elif "\\" in path:
        file_name = path.split("\\")[-1]
    return ".".join(file_name.split(".")[:-1])


def get_file_extension_from_path(path):
    """
    Gets the file extension from a path.

    :param path: The file path.
    :type path: str
    :return: The file extension.
    :rtype: str
    """
    extension = ""
    if "/" in path:
        extension = path.split(".")[-1]
    return extension


def replace_filename_with_header(load_path, output_dir, delete_original_file=False):
    """
    Replaces the filename with the sequence header from the first line of the file. Notice: If you have multiple sequences, we only parse the first file's header

    :param load_path: Path to the input file.
    :type load_path: str
    :param output_dir: Directory where the renamed file will be saved.
    :type output_dir: str
    :param delete_original_file: Whether to delete the original file after renaming. Defaults to False.
    :type delete_original_file: bool, optional
    """
    extension = get_file_extension_from_path(load_path)
    with open(load_path, "r") as input_file:
        header_text = linecache.getline(load_path, 1)[1:].replace("\n", "")
        with open(output_dir + header_text + "." + extension, "w") as output_file:
            for line in input_file:
                output_file.write(line)
    if delete_original_file:
        os.remove(load_path)


def split_multiple_seq_fasta_into_files(load_path, save_dir):
    """
    Splits a FASTA file containing multiple sequences (such as the alignment result file from MAFFT) into separate files.

    :param load_path: Path to the input FASTA file.
    :type load_path: str
    :param save_dir: Directory where the split files will be saved.
    :type save_dir: str
    """
    file_name = get_file_name_from_path(load_path)
    extension = get_file_extension_from_path(load_path)
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


class FastaUnit:
    """
    Represents a FASTA unit with a sequence map.
    """

    def __init__(self):
        """
        Initializes a FastaUnit object.
        """
        self.seq_map = {}

    def fasta_unit(self, load_path):
        """
        Converts a FASTA file into a map object.

        :param load_path: Path to the input FASTA file.
        :type load_path: str
        :return: The FastaUnit object with the populated sequence map.
        :rtype: FastaUnit
        """
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
