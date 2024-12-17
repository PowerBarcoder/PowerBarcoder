import sqlite3
import csv
import sys
import os

def export_table_to_csv(db_path, table_name, csv_path):
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
    qc_report_db = os.path.join(result_data_path, "qcReport.db")
    overall_qc_report_db = os.path.join(result_data_path, "overallQcReport.db")

    # Export each sample QCReport
    export_table_to_csv(qc_report_db, "qcReport", os.path.join(result_data_path, "qcReport.csv"))


if __name__ == "__main__":
    main(sys.argv[1])
