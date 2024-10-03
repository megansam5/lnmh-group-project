"""A script to remove out of date data from the RDS."""
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


if __name__ == "__main__":
    pass
