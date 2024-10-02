

from extract import extract
from datetime import datetime

import pandas as pd


def transform(needs_a_clean: pd.DataFrame):

    needs_a_clean["recording_taken"] = pd.to_datetime(
        needs_a_clean["recording_taken"], format="%Y-%m-%d %H:%M:%S", errors='coerce')

    needs_a_clean['last_watered'] = needs_a_clean['last_watered'].apply(
        lambda row: datetime.strptime(row, "%a, %d %b %Y %H:%M:%S %Z"))

    return needs_a_clean


if __name__ == "__main__":
    print(transform(extract()))
