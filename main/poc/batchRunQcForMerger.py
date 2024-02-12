import csv

"""
有缺陷，dada2_identicl_row_index在不同config下絕對位置可能會不同
"""

CSV_FILE_PATH_PREFIX = '/PowerBarcoder/data/result/batchRun/'
CSV_FILE_PATH_SUFFIX = '_result/qcResult/qcReport.csv'
CONCAT_CSV_FILE_PATH = '/PowerBarcoder/data/result/batchRun/matrix_data.csv'


def get_csv_cell_content(file_path: str, row_index: int, col_index: int):
    """
    # Function to get the content of a specific cell in a CSV file
    :param file_path: the file path of the CSV file
    :param row_index: the row index of the cell
    :param col_index: the column index of the cell
    :return: the content of the cell
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        try:
            # Skip to the desired row
            for _ in range(row_index):
                next(reader)

            # Read the row and get the content of the specific cell
            row = next(reader)
            cell_content = row[col_index]
            return cell_content
        except IndexError:
            return None
        except StopIteration:
            return None


def get_csv_cell_content_in_batch(batch_mane: str, loci_name: str, desired_row_index: int, desired_col_index: int,
                                  run_number: int) -> list:
    """
    # Function to get the content of a specific cell in a CSV file
    :param batch_mane: the batch name of the run
    :param loci_name: the loci name of the run
    :param desired_row_index: the row index of the cell
    :param desired_col_index: the column index of the cell
    :param run_number: the number of the run
    :return: list of the content of the cell
    """
    batch_result_list = list()
    for i in range(0, run_number):
        file_path = CSV_FILE_PATH_PREFIX + batch_mane + str(run_number) + loci_name + CSV_FILE_PATH_SUFFIX
        single_run_result = get_csv_cell_content(file_path, desired_row_index, desired_col_index)
        batch_result_list.append(single_run_result)
    return batch_result_list


def parsing_results_into_csv(batch_name_list: list, loci_name: str, desired_row_index: int, desired_col_index: int,
                             run_number: int):
    """
    # Function to parse the results of multiple runs into a CSV file
    :param batch_name_list:
    :param loci_name:
    :param desired_row_index:
    :param desired_col_index:
    :param run_number:
    :return:
    """
    # Header for the columns
    run_number_list = [str(i + 1) for i in range(run_number)]

    # column names
    column_name_list = batch_name_list

    # File path to save the CSV
    csv_file_path = CONCAT_CSV_FILE_PATH

    # Writing the matrix into the CSV file
    with open(csv_file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow([''] + run_number_list)

        # Write the data rows with row names
        for column_name in column_name_list:
            # Given cell content
            batch_result_list = get_csv_cell_content_in_batch(column_name, loci_name, desired_row_index,
                                                              desired_col_index,
                                                              run_number)
            for i in range(0, len(batch_result_list)):
                if batch_result_list[i] is None:
                    batch_result_list[i] = 'None'

            writer.writerow([column_name] + batch_result_list)

    print("CSV file 'matrix_data.csv' has been created successfully.")


if __name__ == '__main__':
    csv_file_batch_run_name_list = [
        'SuperRed_35',
        'filtered',
        'filtered_selected_pure',
        'no_learn_error'
    ]
    csv_file_path_midfield = '/trnLF'
    batch_run_number = 15
    dada2_identical_row_index = 333  # 334-1
    dada2_identical_col_index = 23  # 24-1

    parsing_results_into_csv(csv_file_batch_run_name_list, csv_file_path_midfield, dada2_identical_row_index,
                             dada2_identical_col_index, batch_run_number)
