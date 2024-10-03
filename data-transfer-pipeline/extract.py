"""Script to extract old recordings from the short term storage."""
from datetime import datetime, timedelta
from os import environ as ENV

import pandas as pd
import pymssql
from dotenv import load_dotenv


def create_connection():
    """Returns a connection to connect to the database. """
    conn = pymssql.connect(
        server=ENV['DB_HOST'],
        database=ENV['DB_NAME'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=1433,
        as_dict=True)
    return conn


def extract_recordings() -> pd.DataFrame:
    '''Returns the recordings over 24 hours old as a dataframe.'''
    load_dotenv()
    cutoff_time = datetime.now() - timedelta(days=1)
    query = f'''
    SELECT recording_id, plant_id, recording_taken, last_watered, soil_moisture, temperature
    FROM {ENV['SCHEMA_NAME']}.recording
    WHERE recording_taken < %s
    '''

    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (cutoff_time,))
        res = cursor.fetchall()

    conn.close()
    df = pd.DataFrame(res)
    print("Recordings extracted!")

    return df


if __name__ == '__main__':
    pass
