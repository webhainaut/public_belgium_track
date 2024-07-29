import os
import sqlite3
from sqlite3 import Error


class DbConnector:

    def __init__(self, path):
        self.os = os
        self.sqlite3 = sqlite3
        self.connection = None
        self.db_path = self.os.path.abspath(os.path.dirname(__file__)) + "/../../" + path

    def create_connection(self):
        try:
            self.connection = self.sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        self.connection.close()

    def execute_query(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            if data is None:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_many_query(self, query, data):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, data)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
