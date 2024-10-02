'''Load functionality of the LMNH plant measurement ETL pipeline.`'''

#pylint:disable= line-too-long, unused-variable, c-extension-no-member,invalid-name

import os
import random
from datetime import datetime, timedelta

import pandas as pd
import pyodbc
from dotenv import load_dotenv



def generate_test_data(num_rows: int) -> pd.DataFrame:
    '''
    Generates and returns test data with the specified number of rows. We will only
    be expecting 50 rows of recording data at a time, but this function allows us to 
    stress-test our load functionality, for larger insertion batches.
    '''

    base_time = datetime.now() 
    available_plant_ids = [i for i in range(0, 51) if i not in [7, 43]]

    test_data = {
        # Assuming with have 50 individual plants, with IDs starting from 0.
        'plant_id': [random.choice(available_plant_ids) for _ in range(num_rows)],  

        # Generating somee random time in the future, in multiples of 5 minute periods.
        'recording_taken': [base_time + timedelta(minutes=5*i) for i in range(num_rows)],

        # Generating random times in the past, in decrements of 30 minute periods.
        'last_watered': [base_time - timedelta(days=2, minutes=30*i) for i in range(num_rows)],

        # Finally for float values, a uniformly random figure is chosen within a predefined range.
        # Rounding is applied to 2.d.p for moisture adn temperature values, as we don't want potentially 3+ d.p.
        'soil_moisture': [round(random.uniform(30.0, 45.0), 2) for _ in range(num_rows)],
        'temperature': [round(random.uniform(20.0, 25.0), 2) for _ in range(num_rows)]
    }
    return pd.DataFrame(test_data)




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
        f'PWD={DB_PASSWORD};'
        f'Encrypt=yes;'
        f'TrustServerCertificate=yes;'
    )


    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()

        # Generating placeholders for each row of data, needed for insertion.
        placeholders = ', '.join(['(?, ?, ?, ?, ?)'] * len(recordings))

        # Base query for inserting into the recording table, for all columns.
        # We are only expecting 50 rows / plant recordings at a given time, so we
        # don't have to consider batch size bottlenecks or chunks.
        insert_query = f'''
        INSERT INTO {DB_SCHEMA}.recording
        (plant_id, recording_taken, last_watered, soil_moisture, temperature)
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

    # test = generate_test_data(50)
    # print(test.tail())
    test_cases = {
        # '5': generate_test_data(5),
        '50': generate_test_data(50),
        # '100': generate_test_data(100), 
        # '150': generate_test_data(50)

    }

    for num, df in test_cases.items():
        print(f'--- Inserting {num} records ---')
        upload_transaction_data(df)