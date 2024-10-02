"""Script to extract old recordings from the short term storage."""
from datetime import datetime, timedelta
from os import environ as ENV

import pandas as pd
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


def fake_insert():
    query = '''
        INSERT INTO alpha.recording (plant_id, recording_taken, last_watered, soil_moisture, temperature) VALUES
        (2, '2024-09-30 17:23:02', '2024-09-30 12:23:02', 82.765, 10.456),
        (30, '2024-09-30 12:23:02', '2024-09-30 10:23:02', 80.765, 13.456),
        (20, '2024-10-01 17:23:02', '2024-09-30 13:23:02', 83.765, 11.456),
        (22, '2024-10-01 17:24:02', '2024-09-30 14:23:02', 84.765, 12.456)
        '''
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
    conn.close()
    print('inserted')


if __name__ == '__main__':
    load_dotenv()
    extract_recordings()
