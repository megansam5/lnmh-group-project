"""The streamlit dashboard"""
import streamlit as st
import pandas as pd
import altair as alt
from pyathena import connect
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ as ENV


def create_temp_chart(recordings: pd.DataFrame) -> alt.Chart:
    """Creates a chart of temperature over time for selected plants and dates."""
    return alt.Chart(recordings).mark_line().encode(
        x='recording_taken:T',
        y='temperature:Q',
        color='plant_id:N',
        tooltip=['recording_taken:T', 'temperature:Q', 'plant_id:N']
    ).properties(
        width=700,
        height=400,
        title='Temperature Over Time'
    )


def create_moisture_chart(recordings: pd.DataFrame) -> alt.Chart:
    """Creates a chart of moisture over time for selected plants and dates."""

    return alt.Chart(df).mark_line().encode(
        x='recording_taken:T',
        y='soil_moisture:Q',
        color='plant_id:N',
        tooltip=['recording_taken:T', 'soil_moisture:Q', 'plant_id:N']
    ).properties(
        width=700,
        height=400,
        title='Soil Moisture Over Time'
    )


def load_data_from_athena(conn, start_date: str, end_date: str, plant_ids: list) -> pd.DataFrame:
    """Loads data from AWS Athena based on the selected date range and plant IDs."""
    plant_filter = ",".join(map(str, plant_ids))
    query = f"""
    SELECT plant_id, recording_taken, temperature, soil_moisture
    FROM {ATHENA_TABLE}
    WHERE date(recording_taken) BETWEEN date('{start_date}') AND date('{end_date}')
    AND plant_id IN ({plant_filter})
    ORDER BY recording_taken
    """

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    return pd.DataFrame(data, columns=columns)


if __name__ == "__main__":

    # configuration, is this needed????
    ATHENA_DATABASE = 'c13_dog_botany_db'
    ATHENA_TABLE = 'plant_recordings'
    S3_OUTPUT = 's3://c13-dog-botany-long-term/results/'

    load_dotenv()
    conn = connect(s3_staging_dir=S3_OUTPUT, region_name='us-west-2',
                   aws_access_key_id=ENV['AWS_ACCESS_KEY'],
                   aws_secret_access_key=ENV['AWS_SECRET_KEY'])

    st.title("Plant Monitoring Dashboard")
    st.write(
        "View temperature and soil moisture trends over time for selected plants.")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    start_date = st.date_input("Start Date", start_date)
    end_date = st.date_input("End Date", end_date)

    plant_ids = st.multiselect(
        "Select up to 3 Plants",
        options=[i for i in range(0, 51)],
        default=[1, 2, 3],
        max_selections=3
    )

    # loads the data, so only queries relevant data
    if st.button("Load Data"):
        df = load_data_from_athena(conn, start_date, end_date, plant_ids)

        if not df.empty:

            st.subheader("Temperature Over Time")

            temperature_chart = create_temp_chart(df)
            st.altair_chart(temperature_chart)

            st.subheader("Soil Moisture Over Time")

            moisture_chart = create_moisture_chart(df)
            st.altair_chart(moisture_chart)
        else:
            st.write("No data available for the selected date range or plants.")
