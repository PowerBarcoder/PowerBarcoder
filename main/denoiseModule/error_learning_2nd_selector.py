"""
此腳本預計置於 dada2_denoise_PE_newprimer.r 後執行，
    用以篩選出供第二次error learning 使用的序列，並將符合條件之置檔名其輸出至一txt檔案中。
"""

import os
import sys

def parse_abundance_from_filename(filename):
    """Parse abundance number from filename."""
    try:
        # Example filename: Sample_01_r1_0.950_abundance_100.fas
        abundance = float(filename.split('_abundance_')[1].split('.fas')[0])
        proportion = float(filename.split('_r')[1].split('_')[1])
        return abundance, proportion
    except:
        return 0, 0

def select_sequences_for_learning(result_data_path, locus):
    """Select sequences meeting criteria for second error learning."""
    selected_files = set()
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
        # 1. r1/r2 > 0.05 and r2/r1 > 20
        # 2. r1 or r2 reads > 20
        # 3. r1 or r2 proportion > 0.95
        if r1_abund > 0 and r2_abund > 0:
            ratio_1_to_2 = r1_abund / r2_abund
            ratio_2_to_1 = r2_abund / r1_abund
            
            if (ratio_1_to_2 > 0.05 and ratio_2_to_1 > 0.05 and
                (r1_abund > 20 or r2_abund > 20) and
                (r1_prop > 0.95 or r2_prop > 0.95)):
                selected_files.add(r1_file)
                selected_files.add(r2_file)
    
    return selected_files

def copy_selected_files(result_data_path, locus, selected_files):
    """Copy selected files to a new directory for second error learning."""
    error_learn_dir = os.path.join(result_data_path, "error_learning_2nd")
    os.makedirs(error_learn_dir, exist_ok=True)
    
    denoise_path = os.path.join(result_data_path, f"{locus}_result", "denoiseResult")
    for filename in selected_files:
        if '_r1_' in filename:
            src = os.path.join(denoise_path, "r1", filename)
            dst = os.path.join(error_learn_dir, filename)
        else:
            src = os.path.join(denoise_path, "r2", filename)
            dst = os.path.join(error_learn_dir, filename)
        try:
            import shutil
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
        selected_files = select_sequences_for_learning(result_data_path, locus)
        
        # Write selected filenames to output file
        output_path = os.path.join(result_data_path, f"{locus}_result", "denoiseResult", "error_learning_2nd.txt")
        with open(output_path, 'w') as f:
            for filename in sorted(selected_files):
                f.write(f"{filename}\n")
        
        # Copy selected files to new directory
        copy_selected_files(result_data_path, locus, selected_files)
        
        print(f"[INFO] Successfully selected {len(selected_files)} files for second error learning")
        print(f"[INFO] Results written to {output_path}")
        print(f"[INFO] Files copied to {os.path.join(result_data_path, 'error_learning_2nd')}")
        
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

