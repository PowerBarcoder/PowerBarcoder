import csv
import sqlite3
import os
import sys

OVERALL_QC_DB = "overallQcReport.db"


def create_overall_qc_report_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS overallQcReport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step TEXT,
            avg_q REAL,
            err_q REAL,
            num_seqs REAL,
            sum_len REAL,
            min_len REAL,
            max_len REAL
        )
    ''')


def insert_overall_qc_report(cursor, data):
    cursor.execute('''
        INSERT INTO overallQcReport (step, avg_q, err_q, num_seqs, sum_len, min_len, max_len)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)


def read_and_store_qc_report(file_path, db_path):
    steps = [
        "Raw data r1",
        "Raw data r2",
        "Fastp quality trim r1",
        "Fastp quality trim r2",
        "Cutadapt demultiplex by locus primer r1",
        "Cutadapt demultiplex by locus primer r2"
    ]

    with open(file_path, 'r') as file:
        lines = file.readlines()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_overall_qc_report_table(cursor)

    step = None  # Current step name
    i = 0  # Line index

    while i < len(lines):
        line = lines[i].strip()
        # 匹配步驟名稱
        if any(step_name in line for step_name in steps):
            step = next((step_name for step_name in steps if step_name in line), None)
            print(f"Found step: {step}")
            if step:
                # Check for "Cutadapt demultiplex ..." and add locus name
                if "Cutadapt demultiplex by locus primer" in step:
                    locus_name = line.split("^|")[1]
                    step = f"{locus_name} Cutadapt demultiplex by locus primer r1"
                # 提取下方兩行數據
                try:
                    avg_q, err_q = map(float, lines[i + 1].strip().split(" "))
                    num_seqs, sum_len, min_len, max_len = map(
                        lambda x: float(x.replace(',', '')),
                        lines[i + 2].strip().split(" ")
                    )
                    # 插入資料到資料庫
                    insert_overall_qc_report(cursor, (step, avg_q, err_q, num_seqs, sum_len, min_len, max_len))
                except (IndexError, ValueError) as e:
                    print(f"Error parsing data for step '{step}': {e}")
                # 跳過處理的兩行數據
                i += 2
        i += 1

    conn.commit()
    conn.close()


# TODO 待與 sql_to_csv 的  method合併
def export_to_csv(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM overallQcReport")
    rows = cursor.fetchall()

    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([i[0] for i in cursor.description])  # write headers
        csvwriter.writerows(rows)

    conn.close()


if __name__ == "__main__":
    result_data_path = sys.argv[1]
    file_path = os.path.join(result_data_path, "overallQcReport.txt")
    db_path = os.path.join(result_data_path, OVERALL_QC_DB)
    csv_path = os.path.join(result_data_path, "overallQcReport.csv")

    read_and_store_qc_report(file_path, db_path)
    export_to_csv(db_path, csv_path)
