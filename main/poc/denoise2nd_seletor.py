import os
import shutil

input_path = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738/trnLF_result/demultiplexResult/filtered"

# 202310281735 filter跟denoise兩個很pure的，拿去做2nd denoise的learn error samples (39個)
candidate_list_pure = ["trnLF_L5675_br12_F4121_br11", "trnLF_L5675_br18_F4121_br11", "trnLF_L5675_br03_F4121_br11",
                       "trnLF_L5675_br07_F4121_br03", "trnLF_L5675_br08_F4121_br05", "trnLF_L5675_br01_F4121_br05",
                       "trnLF_L5675_br08_F4121_br10", "trnLF_L5675_br01_F4121_br06", "trnLF_L5675_br04_F4121_br15",
                       "trnLF_L5675_br05_F4121_br03", "trnLF_L5675_br14_F4121_br10", "trnLF_L5675_br13_F4121_br03",
                       "trnLF_L5675_br05_F4121_br16", "trnLF_L5675_br07_F4121_br05", "trnLF_L5675_br12_F4121_br17",
                       "trnLF_L5675_br16_F4121_br13", "trnLF_L5675_br04_F4121_br16", "trnLF_L5675_br02_F4121_br15",
                       "trnLF_L5675_br09_F4121_br12", "trnLF_L5675_br17_F4121_br06", "trnLF_L5675_br04_F4121_br04",
                       "trnLF_L5675_br07_F4121_br11", "trnLF_L5675_br06_F4121_br02", "trnLF_L5675_br08_F4121_br12",
                       "trnLF_L5675_br14_F4121_br06", "trnLF_L5675_br16_F4121_br15", "trnLF_L5675_br08_F4121_br07",
                       "trnLF_L5675_br01_F4121_br03", "trnLF_L5675_br13_F4121_br17", "trnLF_L5675_br17_F4121_br01",
                       "trnLF_L5675_br15_F4121_br07", "trnLF_L5675_br18_F4121_br10", "trnLF_L5675_br18_F4121_br14",
                       "trnLF_L5675_br10_F4121_br16", "trnLF_L5675_br07_F4121_br14", "trnLF_L5675_br18_F4121_br01",
                       "trnLF_L5675_br05_F4121_br14", "trnLF_L5675_br13_F4121_br15", "trnLF_L5675_br17_F4121_br13"
                       ]
output_path_pure = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738/trnLF_result/demultiplexResult/filtered_selected_pure"

#  202310281735 DADA2失敗，merger成功 (8)
candidate_list_failed = ["trnLF_L5675_br01_F4121_br11", "trnLF_L5675_br04_F4121_br08", "trnLF_L5675_br04_F4121_br11",
                         "trnLF_L5675_br05_F4121_br11", "trnLF_L5675_br13_F4121_br08", "trnLF_L5675_br14_F4121_br11",
                         "trnLF_L5675_br15_F4121_br11", "trnLF_L5675_br17_F4121_br11"
                         ]
output_path_failed = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202310290738/trnLF_result/demultiplexResult/filtered_selected_failed"


def copy_folder_content(output_path, candidate_list):
    # get all file name in input_url
    file_list = os.listdir(input_path)
    print(file_list)  # 'trim_trnLF_L5675_br01_F4121_br01_r1.fq'

    # filter file name by candidate list
    selected_list = []
    for file_name in file_list:
        if file_name.replace('filtered_trim_', '').replace('_r1.fq', '').replace('_r2.fq', '') in candidate_list:
            # print(file_name)
            selected_list.append(file_name)
    print(selected_list)
    print(f'len(selected_list): {len(selected_list)}')

    # create trimmed_selected folder and copy selected file to output_url by python method
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file_name in selected_list:
        # Use the shutil.copy() function to copy the file
        shutil.copy(f'{input_path}/{file_name}', f'{output_path}/')

    # print file name in output_url folder
    output_file_list = os.listdir(output_path)
    print(output_file_list)

def atcg_checker(output_path):
    # print file name in output_url folder
    output_file_list = os.listdir(output_path)
    # check if files in output_url folder have any alphabet not in ['A', 'T', 'C', 'G'] in 2, 6, 10, 14, 18, 22, 26, 30, 34, 38... lines
    for file_name in output_file_list:
        print(f'checking {file_name}')
        with open(f'{output_path}/{file_name}', 'r') as f:
            lines = f.readlines()
            for i in range(1, len(lines), 4):
                # print(f'checking line {i}')
                # print(lines[i].strip())
                for j in range(0, len(lines[i].strip())):
                    if lines[i].strip()[j] not in ['A', 'T', 'C', 'G']:
                        print(f'{file_name} has alphabet not in ["A", "T", "C", "G"] in line {i} and position {j}')
                        break




copy_folder_content(output_path_pure, candidate_list_pure)
atcg_checker(output_path_pure)
copy_folder_content(output_path_failed, candidate_list_failed)
atcg_checker(output_path_failed)
