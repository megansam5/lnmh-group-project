'''Load functionality of the LMNH plant measurement ETL pipeline.`'''

#pylint:disable= line-too-long, unused-variable, c-extension-no-member,invalid-name

import os

import pandas as pd
import pyodbc
from dotenv import load_dotenv



def upload_transaction_data(recordings:pd.DataFrame) -> None:
    '''
    Uploads LMNH plant recording data to 
    the recording table in the database.
    '''

    # Loading in environment variables needed for local development.
    # This is placed alongside the environment constants within the function
    # itself, so when this function is called in the pipeline script, it
    # uses the environment variables of that particular session.
    load_dotenv()

    # Database constants for connecting to the LMNH plant recordings RDS.
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_SCHEMA = os.getenv('SCHEMA_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')


    connection_string = (
        # Note that to run the load script locally using pyodbc,
        # you will have to download a driver using the terminal.
        # This can be easily copy and pasted from the docs.
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={DB_HOST},{DB_PORT};'
        f'DATABASE={DB_NAME};'
        f'UID={DB_USER};'
        f'PWD={DB_PASSWORD}'
    )


    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()

        # Generating placeholders for each row of data, needed for insertion.
        placeholders = ', '.join(['(?, ?, ?, ?, ?, ?)'] * len(recordings))

        # Base query for inserting into the recording table, for all columns.
        # We are only expecting 50 rows / plant recordings at a given time, so we
        # don't have to consider batch size bottlenecks or chunks.
        insert_query = f'''
        INSERT INTO {DB_SCHEMA}.recording
        (recording_id, plant_id, recording_taken, last_watered, soil_moisture, temperature)
        VALUES {placeholders};
        '''

        # Flattening the values from the DataFrame to fit the placeholder list.
        flat_values = [value for row in recordings.itertuples(index=False, name=None) for value in row]

        # Executing the insert query for all flattened values, essentially bulk inserting into the RDS.
        cursor.execute(insert_query, flat_values)

        # Commiting the transaction (so the RDS is actually updated).
        connection.commit()

        print(f'Inserted {len(recordings)} values to {DB_SCHEMA}.recording table')



if __name__ == '__main__':

    # For future testing purposes, with an
    # example MS SQL database or similar.

    pass
