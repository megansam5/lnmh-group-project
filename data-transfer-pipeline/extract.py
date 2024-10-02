"""Script to extract old recordings from the short term storage."""
from datetime import datetime, timedelta
from os import environ as ENV

import pandas as pd
import pyodbc
from dotenv import load_dotenv


def create_connection():
    """Returns a connection to connect to the database. """
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


def extract_recordings() -> pd.DataFrame:
    '''Returns the recordings over 24 hours old as a dataframe.'''
    load_dotenv()

    query = f'''
    SELECT recording_id, plant_id, recording_taken, last_watered, soil_moisture, temperature
    FROM {ENV['SCHEMA_NAME']}.recording
    WHERE recording_taken < ?
    '''

    cutoff_time = datetime.now() - timedelta(days=1)
    conn = create_connection()

    df = pd.read_sql(query, conn, params=[cutoff_time])
    conn.close()
    print("Recordings extracted!")
    return df


if __name__ == '__main__':
    pass
