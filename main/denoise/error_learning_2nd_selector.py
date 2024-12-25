"""
此腳本預計置於 dada2_denoise.r 後執行，
    用以篩選出潛在的污染序列，並將符合條件之置檔名其輸出至一 txt 檔案中。
"""

import os
import sys
import shutil


def parse_abundance_from_filename(filename):
    """Parse abundance number from filename."""
    try:
        # Example filename: Sample_01_r1_0.950_abundance_100.fas
        abundance = float(filename.split('_abundance_')[1].split('.fas')[0])
        proportion = float(filename.split('_r')[1].split('_')[1])
        return abundance, proportion
    except:
        return 0, 0


def select_potential_contaminants(result_data_path, locus):
    """Select sequences meeting criteria for potential contaminants."""
    contaminant_files = set()
    denoise_path = os.path.join(result_data_path, f"{locus}_result", "denoiseResult")

    # Get all files from r1 and r2 directories
    r1_files = {f for f in os.listdir(os.path.join(denoise_path, "r1")) if f.endswith('.fas')}
    r2_files = {f for f in os.listdir(os.path.join(denoise_path, "r2")) if f.endswith('.fas')}

    # Find common samples between r1 and r2
    common_samples = {f.replace('_r1_', '_') for f in r1_files} & {f.replace('_r2_', '_') for f in r2_files}

    for sample in common_samples:
        r1_file = [f for f in r1_files if sample.replace('_', '_r1_') in f][0]
        r2_file = [f for f in r2_files if sample.replace('_', '_r2_') in f][0]

        # Get abundance and proportion for r1 and r2
        r1_abund, r1_prop = parse_abundance_from_filename(r1_file)
        r2_abund, r2_prop = parse_abundance_from_filename(r2_file)

        # Apply selection criteria:
        # 1. reads number：r1/r2 > 0.05 and r2/r1 > 20 (20241212 Deprecated)
        # 2. reads number：r1 or r2 reads > 20 (20241212 Deprecated)
        # 3. proportion： r1 or r2 proportion > 0.95 (20241212保留，用於刪掉 contamination)

        if r1_abund > 0 and r2_abund > 0:
            if r1_prop > 0.95 or r2_prop > 0.95:
                contaminant_files.add(r1_file)
                contaminant_files.add(r2_file)

    return contaminant_files, r1_files | r2_files


def copy_contaminant_files(result_data_path, locus, contaminant_files):
    """Copy contaminant files to a new directory for further analysis."""
    contaminant_dir = os.path.join(result_data_path, "potential_contaminants")
    os.makedirs(contaminant_dir, exist_ok=True)

    denoise_path = os.path.join(result_data_path, f"{locus}_result", "denoiseResult")
    for filename in contaminant_files:
        if '_r1_' in filename:
            src = os.path.join(denoise_path, "r1", filename)
            dst = os.path.join(contaminant_dir, filename)
        else:
            src = os.path.join(denoise_path, "r2", filename)
            dst = os.path.join(contaminant_dir, filename)
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            print(f"[WARNING] Failed to copy {filename}: {str(e)}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python error_learning_2nd_selector.py <result_data_path> <locus>")
        sys.exit(1)

    result_data_path = sys.argv[1]
    locus = sys.argv[2]

    try:
        contaminant_files, all_files = select_potential_contaminants(result_data_path, locus)
        non_contaminant_files = all_files - contaminant_files

        # Write selected filenames to output files
        output_path_contaminants = os.path.join(result_data_path, f"{locus}_result", "denoiseResult",
                                                "potential_contaminants.txt")
        with open(output_path_contaminants, 'w') as f:
            for filename in sorted(contaminant_files):
                f.write(f"{filename}\n")

        output_path_non_contaminants = os.path.join(result_data_path, f"{locus}_result", "denoiseResult",
                                                    "non_contaminants.txt")
        with open(output_path_non_contaminants, 'w') as f:
            for filename in sorted(non_contaminant_files):
                f.write(f"{filename}\n")

        # Copy selected files to new directory
        copy_contaminant_files(result_data_path, locus, contaminant_files)

        print(f"[INFO] Successfully selected {len(contaminant_files)} files as potential contaminants")
        print(f"[INFO] Results written to {output_path_contaminants}")
        print(f"[INFO] Results written to {output_path_non_contaminants}")
        print(f"[INFO] Files copied to {os.path.join(result_data_path, 'potential_contaminants')}")

    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
