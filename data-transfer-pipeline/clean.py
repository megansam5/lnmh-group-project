"""A script to remove out of date data from the RDS."""
import pymssql
from typing import Tuple, Optional
import pandas as pd
from datetime import datetime, timedelta
from os import environ as ENV


from dotenv import load_dotenv

from extract import create_connection


def delete_outdataed_recordings() -> None:
    """Removes the recordings over 24 hours old from the RDS."""
    load_dotenv()
    query = f"""
    DELETE FROM {ENV['SCHEMA_NAME']}.recording
    WHERE recording_taken < %s
    """

    cutoff_time = datetime.now() - timedelta(days=1)
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (cutoff_time,))
        conn.commit()
    conn.close()
    print("Old recordings deleted")


def fetch_current_averages(conn: pymssql.Connection, plant_id: int) -> Optional[Tuple[float, float, int]]:
    """
    Fetch the current average temperature, soil moisture, and recording count for a specific plant.
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT average_temperature, average_soil_moisture, recording_count
            FROM {ENV['SCHEMA_NAME']}.plant_average
            WHERE plant_id = %s
        """, (plant_id,))
        data = cursor.fetchone()

    return data


def update_plant_average(conn: pymssql.Connection, plant_id: int, avg_temp: float, avg_soil_moisture: float, recordings: int) -> None:
    """
    Updates the average temperature, soil moisture, and recording count for a specific plant.
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""
            UPDATE {ENV['SCHEMA_NAME']}.plant_average
            SET average_temperature = %s, average_soil_moisture = %s, recording_count = %s
            WHERE plant_id = %s
        """, (avg_temp, avg_soil_moisture, recordings, plant_id))
    conn.commit()


def insert_new_plant_average(conn: pymssql.Connection, plant_id: int, avg_temp: float, avg_soil_moisture: float, recordings: int) -> None:
    """
    Inserts a new record for the plant with its average temperature, soil moisture, and recording count.
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {ENV['SCHEMA_NAME']}.plant_average (plant_id, average_temperature, average_soil_moisture, recording_count)
            VALUES (%s, %s, %s, %s)
        """, (plant_id, avg_temp, avg_soil_moisture, recordings))


def calculate_new_averages(recordings: pd.DataFrame) -> pd.DataFrame:
    """
    Groups the dataframe by plant_id and calculates new averages for temperature and soil moisture.
    """
    return recordings.groupby('plant_id').agg(
        new_avg_temp=('temperature', 'mean'),
        new_avg_soil_moisture=('soil_moisture', 'mean'),
        new_recordings=('plant_id', 'size')
    ).reset_index()


def process_and_update_averages(recordings: pd.DataFrame) -> None:
    """
    Processes the plant data and updates or inserts average records into the SQL Server database.
    """
    conn = create_connection()
    if not recordings.empty:

        grouped_df = calculate_new_averages(recordings)

        # Iterate over each plant and update or insert records
        for _, row in grouped_df.iterrows():
            plant_id = int(row['plant_id'])
            new_avg_temp = float(row['new_avg_temp'])
            new_avg_soil_moisture = float(row['new_avg_soil_moisture'])
            new_recordings = int(row['new_recordings'])

            current_averages = fetch_current_averages(conn, plant_id)

            if current_averages:
                # If the plant exists, calculate the updated averages
                old_avg_temp = current_averages['average_temperature']
                old_avg_soil_moisture = current_averages['average_soil_moisture']
                old_recordings = current_averages['recording_count']
                total_recordings = old_recordings + new_recordings

                # Calculate the weighted average
                updated_avg_temp = ((old_avg_temp * old_recordings) +
                                    (new_avg_temp * new_recordings)) / total_recordings
                updated_avg_soil_moisture = ((old_avg_soil_moisture * old_recordings) + (
                    new_avg_soil_moisture * new_recordings)) / total_recordings

                # Update the record in the database
                update_plant_average(
                    conn, plant_id, updated_avg_temp, updated_avg_soil_moisture, total_recordings)
            else:
                # If the plant doesn't exist, insert a new record
                insert_new_plant_average(
                    conn, plant_id, new_avg_temp, new_avg_soil_moisture, new_recordings)

        conn.commit()
        conn.close()
        print("Averages updated.")


if __name__ == "__main__":
    pass
