import pyodbc
from dotenv import load_dotenv
from os import environ as ENV


def check_db():
    load_dotenv()

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={ENV['DB_HOST']};'
        f'DATABASE={ENV['DB_NAME']};'  # Now specifying the new database
        f'UID={ENV['DB_USER']};'
        f'PWD={ENV['DB_PASSWORD']}'
    )
    with conn.cursor() as cursor:
        cursor.execute("SELECT DB_NAME()")  # To check the current database

        current_db = cursor.fetchone()[0]
        print(f"Switched to database: {current_db}")
    conn.close()
