import streamlit as st
import altair as alt
import pandas as pd
import pymssql
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ as ENV


def create_connection():
    """Returns a connection to connect to the database. """
    load_dotenv()
    conn = pymssql.connect(
        server=ENV['DB_HOST'],
        database=ENV['DB_NAME'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=1433,
        as_dict=True)
    return conn


def fetch_plant_data(plant_ids):
    """Fetches plant recording data for selected plant IDs."""
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.plant_id, 
                p.plant_name, 
                r.recording_taken, 
                r.temperature, 
                r.soil_moisture 
            FROM 
                alpha.plant p 
            JOIN 
                alpha.recording r ON p.plant_id = r.plant_id 
            WHERE 
                p.plant_id IN %s 
            ORDER BY 
                r.recording_taken ASC
        """, (tuple(plant_ids),))  # Use a tuple for the SQL IN clause
        data = cursor.fetchall()
    return pd.DataFrame(data)


def fetch_plant_averages(plant_ids):
    """Fetches average temperature and soil moisture for selected plant IDs."""
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                plant_id, 
                average_temperature, 
                average_soil_moisture 
            FROM 
                alpha.plant_average 
            WHERE 
                plant_id IN %s
        """, (tuple(plant_ids),))
        averages = cursor.fetchall()
    return pd.DataFrame(averages)


def main():
    st.title("Plant Recordings Dashboard")

    # Multi-select for plant selection
    conn = create_connection()
    plant_query = "SELECT plant_id, plant_name FROM alpha.plant"
    with conn.cursor() as cursor:
        cursor.execute(plant_query)
        res = cursor.fetchall()

    plant_df = pd.DataFrame(res)
    conn.close()

    selected_plants = st.multiselect(
        "Select Plants (Max 5)",
        options=plant_df['plant_name'].tolist(),
        default=['Venus Flytrap'],  # Default plant by name
        max_selections=5
    )

    # Map selected plant names to IDs
    selected_plant_ids = plant_df[plant_df['plant_name'].isin(
        selected_plants)]['plant_id'].tolist()

    # Fetch data for the selected plants
    if selected_plant_ids:
        plant_data = fetch_plant_data(selected_plant_ids)
        average_data = fetch_plant_averages(selected_plant_ids)

        # Create Temperature Chart
        temp_chart = (
            alt.Chart(plant_data)
            .mark_line()
            .encode(
                x='recording_taken:T',
                y='temperature:Q',
                color='plant_name:N'
            )
            .properties(title='Temperature Over the Last 24 Hours')
        )
        for index, row in average_data.iterrows():

            temp_chart += alt.Chart(pd.DataFrame({
                'average_temperature': [row['average_temperature']],
                # Align with the time axis
                'recording_taken': [plant_data['recording_taken'].min()]
            })).mark_rule(color='red', strokeDash=[10, 5]).encode(
                y='average_temperature:Q'
            ).properties(
                title=f'Average Temp: {
                    row["average_temperature"]} for Plant ID: {row["plant_id"]}'
            )

        # Create Soil Moisture Chart
        moisture_chart = (
            alt.Chart(plant_data)
            .mark_line()
            .encode(
                x='recording_taken:T',
                y='soil_moisture:Q',
                color='plant_name:N'
            )
            .properties(title='Soil Moisture Over the Last 24 Hours')
        )
        for index, row in average_data.iterrows():

            moisture_chart += alt.Chart(pd.DataFrame({
                'average_soil_moisture': [row['average_soil_moisture']],
                # Align with the time axis
                'recording_taken': [plant_data['recording_taken'].min()]
            })).mark_rule(color='red', strokeDash=[10, 5]).encode(
                y='average_soil_moisture:Q'
            ).properties(
                title=f'Average Soil Moisture: {
                    row["average_soil_moisture"]} for Plant ID: {row["plant_id"]}'
            )

        # Display Charts
        st.altair_chart(temp_chart, use_container_width=True)
        st.altair_chart(moisture_chart, use_container_width=True)

        # Dropdown to select a plant for more info
        selected_plant_info = st.selectbox(
            "Select a Plant for More Info", options=plant_df['plant_name'].tolist())

        if selected_plant_info:
            plant_info = plant_df[plant_df['plant_name']
                                  == selected_plant_info].iloc[0]
            plant_id = int(plant_info['plant_id'])

            location_query = """
                SELECT 
                    l.city_name, 
                    l.country_code, 
                    b.botanist_name, 
                    b.botanist_email 
                FROM 
                    alpha.plant p 
                JOIN 
                    alpha.location l ON p.location_id = l.location_id 
                JOIN 
                    alpha.botanist b ON p.botanist_id = b.botanist_id 
                WHERE 
                    p.plant_id = %s
            """
            conn = create_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(location_query, (plant_id,))
                    info = cursor.fetchone()
            finally:
                conn.close()

            if info:
                st.write(
                    f"**Location:** {info['city_name']}, {info['country_code']}")
                st.write(f"**Botanist:** {info['botanist_name']}")
                st.write(f"**Email:** {info['botanist_email']}")
            else:
                st.write("No additional information found.")


if __name__ == "__main__":
    main()
