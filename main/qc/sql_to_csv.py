"""
@file sql_to_csv.py
@brief This module exports data from SQLite databases to CSV files.
It includes functions to export specific tables from the databases.
"""
import sqlite3
import csv
import sys
import os

def export_table_to_csv(db_path, table_name, csv_path):
    """
    Export a SQLite table to a CSV file.

    :param db_path: Path to the SQLite database.
    :type db_path: str
    :param table_name: Name of the table to export.
    :type table_name: str
    :param csv_path: Path to the output CSV file.
    :type csv_path: str
    :raises sqlite3.Error: If there is an error executing the SQL queries.
    :raises IOError: If there is an error writing to the CSV file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    cursor.execute(f"PRAGMA table_info({table_name})")
    headers = [description[1] for description in cursor.fetchall()]

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()

def main(result_data_path):
    """
    Main function to export QC reports from SQLite databases to CSV files.

    :param result_data_path: Path to the directory containing the SQLite databases.
    :type result_data_path: str
    """
    qc_report_db = os.path.join(result_data_path, "qcReport.db")
    overall_qc_report_db = os.path.join(result_data_path, "overallQcReport.db")

    # Export each sample QCReport
    export_table_to_csv(qc_report_db, "qcReport", os.path.join(result_data_path, "qcReport.csv"))


if __name__ == "__main__":
    main(sys.argv[1])
