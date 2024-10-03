'''Load functionality of the LMNH plant measurement ETL pipeline.`'''


import os
import random
from datetime import datetime, timedelta

from os import environ as ENV

from extract import extract
from transform import transform

import pandas as pd
import pymssql
from dotenv import load_dotenv


def create_connection():
    """Returns a connection to connect to the database. """
    return pymssql.connect(
        server=ENV['DB_HOST'],
        database=ENV['DB_NAME'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=1433,
        as_dict=True)


def load(recordings: pd.DataFrame) -> None:
    '''
    Uploads LMNH plant recording data to 
    the recording table in the database.
    '''

    nice = [tuple(x) for x in recordings.values]
    insert_query = '''
    INSERT INTO alpha.recording VALUES (%d, %s, %s, %s, %s)
    '''

    conn = create_connection()

    with conn.cursor() as cursor:
        cursor.executemany(insert_query, nice)

    print(f'Inserted {len(recordings)} values')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    load_dotenv()
    load(transform(extract()))
