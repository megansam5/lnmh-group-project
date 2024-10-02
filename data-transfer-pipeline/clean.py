"""A script to remove out of date data from the RDS."""
from datetime import datetime, timedelta
from os import environ as ENV

import pyodbc
from dotenv import load_dotenv


def create_connection():
    '''Returns a connection to connect to the database. '''
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        f'SERVER={ENV['DB_HOST']};'
        f'DATABASE={ENV['DB_NAME']};'
        f'UID={ENV['DB_USER']};'
        f'PWD={ENV['DB_PASSWORD']};'
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'
        # this workings in production but should be:
        # f'TrustStore={path to pem certificate}' when deployed
        # check how this would work in docker image
    )
    return conn


def delete_outdataed_recordings() -> None:
    """Removes the recordings over 24 hours old from the RDS."""
    load_dotenv()
    query = f"""
    DELETE FROM {ENV['SCHEMA_NAME']}.recording
    WHERE recording_taken < ?
    """

    cutoff_time = datetime.now() - timedelta(days=1)
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, cutoff_time)
        conn.commit()
    conn.close()
    print("Old recordings deleted")


if __name__ == "__main__":
    pass
