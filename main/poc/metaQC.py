# import csv
#
# # Replace the file path with your actual CSV file path
# csv_file_path_prefix = '/PowerBarcoder/data/result/batchRun/blasttest'
# csv_file_path_midfield = '/trnLF'
# csv_file_path_suffix = '_result/qcResult/qcReport.csv'
#
#
# # Function to get the content of a specific cell in a CSV file
# def get_csv_cell_content(file_path, row_index, col_index):
#     with open(file_path, newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         try:
#             # Skip to the desired row
#             for _ in range(row_index):
#                 next(reader)
#
#             # Read the row and get the content of the specific cell
#             row = next(reader)
#             cell_content = row[col_index]
#             return cell_content
#         except IndexError:
#             return None
#         except StopIteration:
#             return None
#
#
# def parsing_all_dir_in_single_run(desired_row_index, desired_col_index, current_run_id: int, total_loci_number: int):
#     single_run_result = list()
#
#     # DADA2 identical cell
#     # Specify the row and column indices of the cell you want to retrieve (0-indexed)
#     row_index = desired_row_index
#     col_index = desired_col_index
#
#     for i in range(0, total_loci_number + 1):
#         # Get the content of the desired cell
#         if i == 0:
#             cell_content = get_csv_cell_content(
#                 csv_file_path_prefix + str(current_run_id) + csv_file_path_midfield + csv_file_path_suffix,
#                 row_index,
#                 col_index)
#         else:
#             cell_content = get_csv_cell_content(
#                 csv_file_path_prefix + str(current_run_id) + csv_file_path_midfield + str(i) + csv_file_path_suffix,
#                 row_index,
#                 col_index)
#
#         # Display the content of the cell
#         if cell_content is not None:
#             single_run_result.append(cell_content)
#             # print(f"Content of cell at row {desired_row_index + 1}, column {desired_col_index + 1}: {cell_content}")
#         else:
#             print("Cell not found or file error.")
#
#     return single_run_result
#
#
# def parsing_all_dir_in_batch_run(desired_row_index, desired_col_index, run_number: int, total_loci_number: int):
#     batch_result_list = list()
#     for i in range(0, run_number):
#         single_run_result = parsing_all_dir_in_single_run(desired_row_index, desired_col_index, i, total_loci_number)
#         batch_result_list.append(single_run_result)
#     return batch_result_list
#
#
# def parsing_results_into_csv(desired_row_index, desired_col_index, run_number: int, total_loci_number: int):
#     # Given matrix
#     matrix = parsing_all_dir_in_batch_run(desired_row_index, desired_col_index, run_number, total_loci_number)
#
#     # Header for the columns
#     header = ['trnLF' + str(i) for i in range(total_loci_number + 1)]
#
#     # Row names
#     row_names = ['blasttest' + str(i) for i in range(total_loci_number + 1)]
#
#     # File path to save the CSV
#     csv_file_path = '/PowerBarcoder/data/result/batchRun/matrix_data.csv'
#
#     # Writing the matrix into the CSV file
#     with open(csv_file_path, mode='w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#
#         # Write the header row
#         writer.writerow([''] + header)
#
#         # Write the data rows with row names
#         for i, row in enumerate(matrix):
#             writer.writerow([row_names[i]] + row)
#
#     print("CSV file 'matrix_data.csv' has been created successfully.")
#
#
# batch_run_number = 5
# total_loci_number = 9
# dada2_identicl_row_index = 333  # 334-1
# dada2_identicl_col_index = 23  # 24-1
#
# parsing_results_into_csv(dada2_identicl_row_index, dada2_identicl_col_index, batch_run_number, total_loci_number)
