import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

DATAWAREHOUSE_SERVER = os.getenv("DATAWAREHOUSE_SERVER")


class DataWarehouse:
    def __init__(self):
        self.server = DATAWAREHOUSE_SERVER

    def connect_to_db(self):
        return pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            f"Server={self.server};"
            "Database=TS.DSO;"
            "Trusted_Connection=yes;"
        )

    def get_table_schema(self, table_name):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """)
            schema = cursor.fetchall()
            return {row[0]: row[1] for row in schema}
        finally:
            conn.close()



    def execute_query(self, query):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()  # Data rows
            if not rows:
                return {"columns": [], "rows": []}

            # Extract column names from cursor.description
            columns = [desc[0] for desc in cursor.description]

            # Ensure rows are in the correct format (list of tuples)
            rows = [list(row) for row in rows]

            return {"columns": columns, "rows": rows}
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

