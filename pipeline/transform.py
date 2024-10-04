"""This script transforms the data to be loaded into a database"""

from datetime import datetime

import pandas as pd

from extract import extract
from emailing import send_email


def clean(needs_a_clean: pd.DataFrame) -> pd.DataFrame:
    """This function returns a clean dataframe ready for insertion. """
    needs_a_clean["recording_taken"] = pd.to_datetime(
        needs_a_clean["recording_taken"], format="%Y-%m-%d %H:%M:%S", errors='coerce')

    needs_a_clean['last_watered'] = needs_a_clean['last_watered'].apply(
        lambda row: datetime.strptime(row, "%a, %d %b %Y %H:%M:%S %Z"))

    needs_a_clean['last_watered'] = needs_a_clean['last_watered'].apply(
        lambda row: row.strftime("%Y-%m-%d %H:%M:%S"))

    needs_a_clean['recording_taken'] = needs_a_clean['recording_taken'].apply(
        lambda row: row.strftime("%Y-%m-%d %H:%M:%S"))

    return needs_a_clean


def check_conditions(clean: pd.DataFrame):
    for index, row in clean.iterrows():
        if row['temperature'] > 50:
            send_email(row['plant_id'], row['temperature'],
                       'temperature', 'exceeded')

        if row['temperature'] <= 5:
            send_email(row['plant_id'], row['temperature'],
                       'temperature', 'not met')

        if row['soil_moisture'] >= 90:
            send_email(row['plant_id'], row['soil_moisture'],
                       'soil moisture', 'exceeded')

        if row['soil_moisture'] < 30:
            send_email(row['plant_id'], row['soil_moisture'],
                       'soil moisture', 'not met')


def transform(needs_a_clean: pd.DataFrame) -> pd.DataFrame:
    """This function returns a clean dataframe ready for insertion. """

    fresh_and_clean = clean(needs_a_clean)
    check_conditions(fresh_and_clean)

    return fresh_and_clean


if __name__ == "__main__":
    print(transform(extract()))
