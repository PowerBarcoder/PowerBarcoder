import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def close(self):
        self.conn.close()
