"""This script transforms the data to be loaded into a database"""

from datetime import datetime

import pandas as pd

from extract import extract


def transform(needs_a_clean: pd.DataFrame):
    """This function returns a clean dataframe ready for insertion. """
    needs_a_clean["recording_taken"] = pd.to_datetime(
        needs_a_clean["recording_taken"], format="%Y-%m-%d %H:%M:%S", errors='coerce')

    needs_a_clean['last_watered'] = needs_a_clean['last_watered'].apply(
        lambda row: datetime.strptime(row, "%a, %d %b %Y %H:%M:%S %Z"))

    return needs_a_clean


if __name__ == "__main__":
    print(transform(extract()))
