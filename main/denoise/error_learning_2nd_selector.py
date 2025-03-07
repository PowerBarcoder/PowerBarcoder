"""
DADA2 Second Error Learning Sequence Selector

This script is designed to be executed after dada2_denoise.r to identify and filter potential contamination sequences.
It analyzes the denoised sequences from both R1 and R2 reads and categorizes them based on specific criteria.

The script performs the following tasks:
1. Reads denoised sequence files from R1 and R2 directories
2. Identifies common samples between R1 and R2
3. Applies filtering criteria to detect potential contaminants
4. Outputs three categorized lists: potential non-contaminants, contaminants, and unique sequences
    - non_contaminants_r1.txt
    - non_contaminants_r2.txt
    - potential_contaminants_r1.txt
    - potential_contaminants_r2.txt
    - unique_r1.txt
    - unique_r2.txt
5. Copies non-contaminant files to a separate directory for 2nd error learning
6. Checks if the fastq files in validate_list have enough total base pair or total reads

Usage:
    python error_learning_2nd_selector.py <result_data_path> <locus>

Arguments:
    result_data_path (str): Path to the result data directory
    locus (str): Name of the locus being analyzed

Output Files:
    - non_contaminants.txt: List of files that passed contamination checks
    - potential_contaminants.txt: List of files identified as potential contaminants
    - unique.txt: List of files that are unique to either R1 or R2

Selection Criteria:
    - Proportion threshold: Sequences with proportion > 0.95 in either R1 or R2 are marked as potential contaminants
"""

import logging
import shutil
import sys
import traceback
import os

from main.qc.csvParser import process_abundance_file, parsing_denoise_pair_into_dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init():
    """
    Initialize the script by processing command line arguments.
    
    Sets up global variables:
        SYS_ARGS (list): Command line arguments
        RESULT_DATA_PATH (str): Path to result data directory
        LOCUS (str): Name of the locus being analyzed
        DADA2_DENOISE_R1_FILE_PATH (str): Path to the R1 denoised files
        DADA2_DENOISE_R2_FILE_PATH (str): Path to the R2 denoised files
        OUTPUT_PATH_BASE (str): Base path for output files
        SECOND_ERROR_LEARN_PATH (str): Path for second error learning files
        DENOISE_PAIR_PATH (str): Path to the denoise pairs file
        DEMULTIPLEX_RESULT_OUTPUT_PATH (str): Path to the demultiplex result output
        DEMULTIPLEX_RESULT_OUTPUT_PATH_FILTERED (str): Path to the filtered demultiplex result output
        
    Exits with code 1 if required arguments are missing.
    """
    global SYS_ARGS, RESULT_DATA_PATH, LOCUS, DADA2_DENOISE_R1_FILE_PATH, DADA2_DENOISE_R2_FILE_PATH, OUTPUT_PATH_BASE, \
        SECOND_ERROR_LEARN_PATH, DENOISE_PAIR_PATH, DEMULTIPLEX_RESULT_OUTPUT_PATH, DEMULTIPLEX_RESULT_OUTPUT_PATH_FILTERED

    SYS_ARGS = sys.argv  # example ['error_learning_2nd_selector.py', 'my <result_data_path>', 'trnLF']

    logging.info(f"error_learning_2nd_selector.py - sys_args: {SYS_ARGS}")

    if len(SYS_ARGS) != 3:
        logging.error("Usage: python error_learning_2nd_selector.py <result_data_path> <locus>")
        sys.exit(1)

    RESULT_DATA_PATH = SYS_ARGS[1]
    LOCUS = SYS_ARGS[2]

    DADA2_DENOISE_R1_FILE_PATH = os.path.join(RESULT_DATA_PATH, f"{LOCUS}_result", "denoiseResult", "r1")
    DADA2_DENOISE_R2_FILE_PATH = os.path.join(RESULT_DATA_PATH, f"{LOCUS}_result", "denoiseResult", "r2")
    OUTPUT_PATH_BASE = os.path.join(RESULT_DATA_PATH, f"{LOCUS}_result", "denoiseResult")

    # SECOND_ERROR_LEARN_PATH (use non-contaminant files)
    DEMULTIPLEX_RESULT_OUTPUT_PATH = os.path.join(RESULT_DATA_PATH, f"{LOCUS}_result", "demultiplexResult")
    DEMULTIPLEX_RESULT_OUTPUT_PATH_FILTERED = os.path.join(DEMULTIPLEX_RESULT_OUTPUT_PATH, "filtered")
    SECOND_ERROR_LEARN_PATH = os.path.join(DEMULTIPLEX_RESULT_OUTPUT_PATH, "error_learning_2nd")
    DENOISE_PAIR_PATH = os.path.join(RESULT_DATA_PATH, f"{LOCUS}_result", "denoiseResult", "denoise_pairs.txt")


def copy_files(files: list, output_data_path: str) -> None:
    """
    Copy identified files to a separate directory for further analysis.
    
    Args:
        files (list): List of filenames to copy
        output_data_path (str): Path to the output directory
        
    Creates:
        A new directory with the specified name and copies relevant files there
    """
    os.makedirs(output_data_path, exist_ok=True)
    for filepath in files:
        try:
            shutil.copy2(filepath, output_data_path)
        except Exception as e:
            logging.warning(f"Failed to copy {filepath}: {str(e)}")


def get_filename_list_from_path_by_extension(path: str, extension: str) -> list:
    """
    Retrieve a list of files with specified extension from given directory.
    
    Args:
        path (str): Directory path to search
        extension (str): File extension to filter by (e.g., '.fas')
        
    Returns:
        list: List of filenames matching the specified extension
    """
    file_list = []
    for filename in os.listdir(path):
        if filename.endswith(extension):
            file_list.append(filename)
    return file_list


def write_output_files(output_path, filename_set, suffix):
    """
    Write the filenames to the specified output file with the given suffix.
    
    Args:
        output_path (str): Base path to result directory
        filename_set (set): Set of filenames to write
        suffix (str): Suffix to append to the output file name
    """
    with open(f"{os.path.join(output_path, suffix + '.txt')}", 'w') as f:
        for filename in sorted(filename_set):
            f.write(f"{filename}\n")


def batch_clean():
    """
    Remove all files or folders that main() created.
    """
    try:
        # Remove non-contaminants directory
        if os.path.exists(SECOND_ERROR_LEARN_PATH):
            shutil.rmtree(SECOND_ERROR_LEARN_PATH)
            logging.info(f"Removed directory: {SECOND_ERROR_LEARN_PATH}")

        # Remove output files
        output_files = [
            os.path.join(OUTPUT_PATH_BASE, "non_contaminants.txt"),
            os.path.join(OUTPUT_PATH_BASE, "potential_contaminants.txt"),
            os.path.join(OUTPUT_PATH_BASE, "unique_r1.txt"),
            os.path.join(OUTPUT_PATH_BASE, "unique_r2.txt")
        ]
        for file in output_files:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Removed file: {file}")

    except Exception as e:
        logging.error(f"Failed to clean up: {str(e)}")
        logging.error(traceback.print_exc())


def get_common_and_unique_samples(r1_files, r2_files):
    """
    Identify common and unique samples between R1 and R2 files.
    
    Args:
        r1_files (list): List of R1 filenames
        r2_files (list): List of R2 filenames
        
    Returns:
        tuple: Sets of common filenames, unique R1 filenames, and unique R2 filenames
    """
    common_filename_set = set()
    unique_r1_set = set()
    unique_r2_set = set()

    for f1 in r1_files:
        sample1 = f1.replace('_r1_', '_')
        found = False
        for f2 in r2_files:
            sample2 = f2.replace('_r2_', '_')
            if sample1 == sample2:
                common_filename_set.add(sample1)
                found = True
                break
        if not found:
            unique_r1_set.add(sample1)

    for f2 in r2_files:
        sample2 = f2.replace('_r2_', '_')
        if sample2 not in common_filename_set:
            unique_r2_set.add(sample2)

    return common_filename_set, unique_r1_set, unique_r2_set


def apply_selection_criteria(common_samples):
    """
    Apply selection criteria to identify non-contaminants and potential contaminants.
    
    Args:
        common_samples (set): Set of common sample filenames
        
    Returns:
        tuple: Sets of non-contaminant filenames and potential contaminant filenames
    """
    non_contaminant_set = set()
    potential_contaminant_set = set()
    for sample in common_samples:
        asv_count_index = 0
        best_asv_proportion_index = 1
        # read file content: [ASV count, best ASV proportion, best ASV number, hash value]
        r1_file_content = process_abundance_file(os.path.join(DADA2_DENOISE_R1_FILE_PATH, sample))
        r2_file_content = process_abundance_file(os.path.join(DADA2_DENOISE_R2_FILE_PATH, sample))
        # apply selection criteria
        if r1_file_content[asv_count_index] > 0 and r2_file_content[asv_count_index] > 0:
            if r1_file_content[best_asv_proportion_index] > 0.95 or r2_file_content[best_asv_proportion_index] > 0.95:
                potential_contaminant_set.add(sample)
            else:
                non_contaminant_set.add(sample)
    return non_contaminant_set, potential_contaminant_set


def check_fastq_nbase_and_nread(validate_list, min_base_pairs=10000, min_reads=30):
    """
    Check if the fastq files in validate_list have enough total base pair or total reads.
    
    Args:
        validate_list (list): List of fastq file paths to validate
        min_base_pairs (int): Minimum total base pairs required
        min_reads (int): Minimum total reads required
        
    Logs a warning if the total base pair or total reads is less than the threshold.
    """
    total_base_pair = 0
    total_reads = 0
    for filename in validate_list:
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i % 4 == 1:
                    total_base_pair += len(line.strip())
                    total_reads += 1
    if total_base_pair < min_base_pairs or total_reads < min_reads:
        logging.warning(f"Total base pair: {total_base_pair}, total reads: {total_reads}")
        logging.warning(f"Total base pair or total reads is less than {min_base_pairs} or {min_reads}, respectively.")
        logging.warning("\n" + "=" * 50 + "\n" +
                        "!!! WARNING: Data volume is too low !!!\n" +
                        "Please consider using default error learning.\n" +
                        "=" * 50)
    else:
        logging.info(f"Total base pair: {total_base_pair}, total reads: {total_reads}")


def main():
    """
    Main execution function for the sequence selector.

    Workflow:
    1. Get lists of R1 and R2 files
    2. Identify common samples between R1 and R2
    3. Apply contamination detection criteria
    4. Write results to three separate output files
    5. Copy non-contaminant files to a separate directory for 2nd error learning
    6. Check if the fastq files in validate_list have enough total base pair or total reads

    Raises:
        Exception: If any error occurs during execution

    Output Files:
        - non_contaminants.txt: Files that passed contamination checks
        - potential_contaminants.txt: Files identified as potential contaminants
        - unique.txt: Files unique to either R1 or R2
    """
    try:
        # Step 1: Get all files from r1 and r2 directories
        denoise_r1_filename_list = get_filename_list_from_path_by_extension(DADA2_DENOISE_R1_FILE_PATH, '.fas')
        denoise_r2_filename_list = get_filename_list_from_path_by_extension(DADA2_DENOISE_R2_FILE_PATH, '.fas')

        # Step 2: Find common samples between r1 and r2 and add unique filenames to unique_filename_set
        common_filename_set, unique_r1_set, unique_r2_set = get_common_and_unique_samples(
            denoise_r1_filename_list, denoise_r2_filename_list)

        # Step 3: Apply selection criteria to identify non-contaminants and potential contaminants
        non_contaminant_set, potential_contaminant_set = apply_selection_criteria(common_filename_set)

        # Step 4: Write results to output files
        write_output_files(OUTPUT_PATH_BASE, non_contaminant_set, "non_contaminants")
        write_output_files(OUTPUT_PATH_BASE, potential_contaminant_set, "potential_contaminants")
        write_output_files(OUTPUT_PATH_BASE, unique_r1_set, "unique_r1")
        write_output_files(OUTPUT_PATH_BASE, unique_r2_set, "unique_r2")

        # Step 5: Copy non-contaminant files to a separate directory for 2nd error learning
        sequence_info_dict = parsing_denoise_pair_into_dict(DENOISE_PAIR_PATH)
        reverse_sequence_info_dict = {v + "_.fas": k for k, v in sequence_info_dict.items()}
        non_contaminant_set = {reverse_sequence_info_dict[filename] for filename in non_contaminant_set}
        validate_list = list()
        for filename in non_contaminant_set:
            if filename in sequence_info_dict:
                validate_list.append(
                    os.path.join(DEMULTIPLEX_RESULT_OUTPUT_PATH_FILTERED, "filtered_trim_" + filename + "_r1.fq"))
                validate_list.append(
                    os.path.join(DEMULTIPLEX_RESULT_OUTPUT_PATH_FILTERED, "filtered_trim_" + filename + "_r2.fq"))
            else:
                logging.warning(f"{filename} not found in sequence_info_dict")
        copy_files(validate_list, SECOND_ERROR_LEARN_PATH)

        # Step 6: Check if the fastq files in validate_list have enough total base pair or total reads
        check_fastq_nbase_and_nread(validate_list)

        # Log the results
        logging.info(f"Successfully selected {len(non_contaminant_set)} files as non-contaminants")
        logging.info(f"Results written to {OUTPUT_PATH_BASE}_non_contaminants.txt")
        logging.info(f"Results written to {OUTPUT_PATH_BASE}_potential_contaminants.txt")
        logging.info(f"Results written to {OUTPUT_PATH_BASE}_unique_r1.txt")
        logging.info(f"Results written to {OUTPUT_PATH_BASE}_unique_r2.txt")

    except Exception as e:
        logging.error(traceback.print_exc())
        sys.exit(1)


if __name__ == "__main__":
    init()
    # batch_clean()
    main()
