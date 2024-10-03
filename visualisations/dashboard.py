"""The streamlit dashboard"""
import streamlit as st
import altair as alt
import pandas as pd

# Sample data for a plant
data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=24, freq=''),
    'soil_moisture': [70, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46],
})

# Streamlit dashboard layout
st.title("Plant Monitoring Dashboard")

# Dropdown to select plant
plant = st.selectbox("Select Plant", ["Plant 1", "Plant 2", "Plant 3"])

# Altair chart for soil moisture
soil_moisture_chart = alt.Chart(data).mark_line().encode(
    x='timestamp:T',
    y='soil_moisture:Q',
).properties(
    title=f"Soil Moisture for {plant}"
)

# Display chart
st.altair_chart(soil_moisture_chart, use_container_width=True)
