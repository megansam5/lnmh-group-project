"""Script to load the data as a parquet file to the s3 bucket."""
from io import BytesIO
from os import environ as ENV
from datetime import datetime, timedelta

import pandas as pd
from boto3 import client
from dotenv import load_dotenv


def create_filepath() -> str:
    """Creates a file path for yesterdays date."""
    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.strftime("%Y")
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    filepath = f'plant_recordings/{year}/{month}/{day}/recording.parquet'
    return filepath


def load_to_s3(recordings: pd.DataFrame) -> None:
    """Loads the dataframe to the s3 bucket as a parquet file."""

    recording_parquet = BytesIO()

    recordings.to_parquet(recording_parquet, index=False)
    recording_parquet.seek(0)
    load_dotenv()
    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_KEY"])
    bucket_name = ENV['BUCKET_NAME']
    key = create_filepath()
    s3.upload_fileobj(Fileobj=recording_parquet, Bucket=bucket_name, Key=key)
    print("Recordings uploaded.")


if __name__ == "__main__":
    pass
