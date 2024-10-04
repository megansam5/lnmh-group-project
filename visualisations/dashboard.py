import pymssql
import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv
from os import environ as ENV
<< << << < HEAD
"""Streamlit dashboard."""


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
        """, (tuple(plant_ids),))
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


def create_temp_chart(plant_data: pd.DataFrame) -> alt.Chart:
    """Returns a chart of temperature over time."""
    return alt.Chart(plant_data).mark_line().encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(
                title='Time Recorded')),
        y=alt.Y('temperature:Q', axis=alt.Axis(
                title='Temperature (°C)')),
        color=alt.Color(
            'plant_name:N', legend=alt.Legend(title='Plant Name'))
    ).properties(title='Temperature Over the Last 24 Hours')


def create_temp_avg_chart(plant_data: pd.DataFrame, row: pd.Series) -> alt.Chart:
    """Returns the average temperature on the chart."""
    return alt.Chart(pd.DataFrame({
        'average_temperature': [row['average_temperature']],
        'recording_taken': [plant_data['recording_taken'].min()]
    })).mark_rule(color='red', strokeDash=[10, 5]).encode(
        y='average_temperature:Q'
    )


def create_soil_moisture_chart(plant_data: pd.DataFrame) -> alt.Chart:
    """Returns a chart of soil moisture over time."""
    return alt.Chart(plant_data).mark_line().encode(
        x=alt.X('recording_taken:T', axis=alt.Axis(
            title='Time Recorded')),
        y=alt.Y('soil_moisture:Q', axis=alt.Axis(
            title='Soil Moisture (%)'
        )),
        color=alt.Color(
            'plant_name:N', legend=alt.Legend(title='Plant Name'))
    ).properties(title='Soil Moisture Over the Last 24 Hours')


def create_soil_moisture_avg_chart(plant_data: pd.DataFrame, row: pd.Series) -> alt.Chart:
    """Returns the average soil moisture on the chart."""
    return alt.Chart(pd.DataFrame({
        'average_soil_moisture': [row['average_soil_moisture']],
        'recording_taken': [plant_data['recording_taken'].min()]
    })).mark_rule(color='red', strokeDash=[10, 5]).encode(
        y='average_soil_moisture:Q'
    )


def display_dashboard():
    """Displays the dashboard."""
    st.title("Plant Recordings Dashboard")

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

    selected_plant_ids = plant_df[plant_df['plant_name'].isin(
        selected_plants)]['plant_id'].tolist()

    if selected_plant_ids:
        plant_data = fetch_plant_data(selected_plant_ids)
        average_data = fetch_plant_averages(selected_plant_ids)
        row = average_data.iloc[0] if not average_data.empty else None

        temp_chart = create_temp_chart(plant_data)
        if len(selected_plant_ids) == 1 and row is not None:
            temp_chart += create_temp_avg_chart(plant_data, row)

        moisture_chart = create_soil_moisture_chart(plant_data)

        if len(selected_plant_ids) == 1 and row is not None:
            moisture_chart += create_soil_moisture_avg_chart(plant_data, row)

        st.altair_chart(temp_chart, use_container_width=True)
        st.altair_chart(moisture_chart, use_container_width=True)

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
                    l.latitude,
                    l.longitude, 
                    b.botanist_name, 
                    b.botanist_email,
                    b.botanist_phone_no,
                    p.scientific_name,
                    p.image_url
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
                col1, col2 = st.columns([1, 3])

                if info['image_url']:
                    with col1:
                        st.image(info['image_url'],
                                 caption="Scientific Image", use_column_width=True)

                with col2:
                    st.write(f"**Scientific Name:** {info['scientific_name']}")
                    st.write(
                        f"**Origin Location:** {info['city_name']}, {info['country_code']}")
                    st.write(
                        f"**Origin Lat/Long:** {info['latitude']}/{info['longitude']}")
                    st.write(f"**Botanist:** {info['botanist_name']}")
                    st.write(f"**Email:** {info['botanist_email']}")
                    st.write(f"**Phone No:** {info['botanist_phone_no']}")

            else:
                st.write("No additional information found.")


if __name__ == "__main__":
    display_dashboard()
