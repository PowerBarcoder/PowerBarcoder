"""
@file database_manager.py
@brief This module provides a class to manage SQLite database operations,
including creating tables and inserting data.
"""
import sqlite3

class DatabaseManager:
    """
    A class to manage SQLite database operations.
    """
    def __init__(self, db_path):
        """
        Initialize the DatabaseManager with a database path.

        :param db_path: The path to the SQLite database.
        :type db_path: str
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_sql):
        """
        Create a table in the SQLite database.

        :param create_table_sql: The SQL query to create the table.
        :type create_table_sql: str
        :raises sqlite3.Error: If there is an error executing the SQL query.
        """
        try:
            self.cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, insert_sql, data):
        """
        Insert data into a table in the SQLite database.

        :param insert_sql: The SQL query to insert data.
        :type insert_sql: str
        :param data: The data to be inserted into the table.
        :type data: tuple
        :raises sqlite3.Error: If there is an error executing the SQL query.
        """
        try:
            self.cursor.execute(insert_sql, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def close(self):
        """
        Close the connection to the SQLite database.
        """
        self.conn.close()
