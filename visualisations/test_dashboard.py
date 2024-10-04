"""This file tests the functionality of the dashboard script."""

from unittest import TestCase
from unittest.mock import patch, MagicMock
import pandas as pd
import altair as alt
from dashboard import (fetch_plant_data, fetch_plant_averages, create_temp_chart,
                       create_temp_avg_chart, create_soil_moisture_chart,
                       create_soil_moisture_avg_chart, display_dashboard)


class TestFetchPlantData(TestCase):
    """Tests for the fetch plant data function."""

    @patch("dashboard.create_connection")
    def test_fetch_plant_data(self, fake_create_connection):
        """Test fetching plant data from the database."""
        fake_conn = MagicMock()
        fake_cursor = MagicMock()
        fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
        fake_create_connection.return_value = fake_conn

        fake_cursor.fetchall.return_value = [{"plant_id": 1,
                                              "plant_name": "Rose",
                                              "recording_taken": "2023-01-01 12:00:00",
                                              "temperature": 20, "soil_moisture": 50}]

        plant_ids = [1, 2]
        result_df = fetch_plant_data(plant_ids)

        fake_cursor.execute.assert_called_once()
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(result_df.iloc[0]["plant_name"], "Rose")


class TestFetchPlantAverages(TestCase):
    """Tests for the fetch plant averages function."""

    @patch("dashboard.create_connection")
    def test_fetch_plant_averages(self, fake_create_connection):
        """Test fetching plant averages from the database."""
        fake_conn = MagicMock()
        fake_cursor = MagicMock()
        fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
        fake_create_connection.return_value = fake_conn

        fake_cursor.fetchall.return_value = [{"plant_id": 1,
                                              "average_temperature": 20.5,
                                              "average_soil_moisture": 55}]

        plant_ids = [1]
        result_df = fetch_plant_averages(plant_ids)

        fake_cursor.execute.assert_called_once()
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(result_df.iloc[0]["average_temperature"], 20.5)


class TestCreateTempChart(TestCase):
    """Tests for the create temp chart function."""

    def test_create_temp_chart(self):
        """Test temperature chart creation with plant data."""
        plant_data = pd.DataFrame({"plant_name": ["Rose"],
                                   "recording_taken": ["2023-01-01 12:00:00"],
                                   "temperature": [20]})

        chart = create_temp_chart(plant_data)
        self.assertIsInstance(chart, alt.Chart)


class TestCreateTempAvgChart(TestCase):
    """Tests for the create temp avg chart function."""

    def test_create_temp_avg_chart(self):
        """Test average temperature line creation on the chart."""
        plant_data = pd.DataFrame({"recording_taken": ["2023-01-01 12:00:00"],
                                   "temperature": [20]})
        row = pd.Series({"average_temperature": 21})

        chart = create_temp_avg_chart(plant_data, row)
        self.assertIsInstance(chart, alt.Chart)


class TestCreateSoilMoistureChart(TestCase):
    """Tests for the create soil moisture chart function."""

    def test_create_soil_moisture_chart(self):
        """Test soil moisture chart creation with plant data."""
        plant_data = pd.DataFrame({"plant_name": ["Rose"],
                                   "recording_taken": ["2023-01-01 12:00:00"],
                                   "soil_moisture": [50]})

        chart = create_soil_moisture_chart(plant_data)
        self.assertIsInstance(chart, alt.Chart)


class TestCreateSoilMoistureAvgChart(TestCase):
    """Tests for the create soil moisture avg chart function."""

    def test_create_soil_moisture_avg_chart(self):
        """Test average soil moisture line creation on the chart."""
        plant_data = pd.DataFrame({"recording_taken": ["2023-01-01 12:00:00"],
                                   "soil_moisture": [50]})
        row = pd.Series({"average_soil_moisture": 55})

        chart = create_soil_moisture_avg_chart(plant_data, row)
        self.assertIsInstance(chart, alt.Chart)


class TestDisplayDashboard(TestCase):
    """Tests for the display dashboard function."""

    @patch("dashboard.st")
    @patch("dashboard.fetch_plant_data")
    @patch("dashboard.fetch_plant_averages")
    @patch("dashboard.create_connection")
    def test_display_dashboard(self, fake_create_connection, fake_fetch_plant_data,
                               fake_fetch_plant_averages, fake_st):
        """Test display dashboard logic."""
        fake_conn = MagicMock()
        fake_create_connection.return_value = fake_conn

        plant_data_mock = [{"plant_id": 1, "plant_name": "Rose"}]

        fake_conn.cursor.return_value.__enter__.return_value.fetchall.return_value = plant_data_mock

        fake_fetch_plant_data.return_value = pd.DataFrame({"plant_id": [1],
                                                           "plant_name": ["Rose"],
                                                           "recording_taken": ["2023-01-01 12:00:00"],
                                                           "temperature": [20],
                                                           "soil_moisture": [50],
                                                           "average_temperature": [18],
                                                           "average_soil_moisture": [55]})

        fake_fetch_plant_averages.return_value = pd.DataFrame({"plant_id": [1],
                                                               "average_temperature": [21],
                                                               "average_soil_moisture": [55],
                                                               "recording_taken": ["2023-01-01 12:00:00"]})

        fake_st.multiselect.return_value = ["Rose"]
        fake_st.selectbox.return_value = "Rose"
        fake_st.columns.return_value = MagicMock(), MagicMock()

        display_dashboard()

        fake_st.title.assert_called_once_with("Plant Recordings Dashboard")
        fake_st.altair_chart.assert_called()
        fake_st.multiselect.assert_called_once_with("Select Plants (Max 5)",
                                                    options=["Rose"],
                                                    default=["Venus Flytrap"],
                                                    max_selections=5)
