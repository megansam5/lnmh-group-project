"""This file tests the functionality of the transform script."""
from unittest.mock import patch
from unittest import TestCase

import pandas as pd
import pytest

from transform import transform, clean, check_conditions


class TestTransformFunction(TestCase):
    """Tests for the transform function."""

    def test_transform_with_valid_data(self):
        """Tests that transform returns a correct dataframe given the provided
        data."""
        input_data = pd.DataFrame({"plant_id": [1, 2],
                                   "recording_taken": ["2024-10-01 12:34:56",
                                                       "2024-10-02 14:20:30"],
                                   "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT",
                                                    "Tue, 01 Oct 2024 11:00:00 GMT"],
                                   "soil_moisture": [30.0, 45.0],
                                   "temperature": [22.5, 23.0]})

        result_df = transform(input_data)

        expected_df = pd.DataFrame({"plant_id": [1, 2],
                                    "recording_taken": ["2024-10-01 12:34:56",
                                                        "2024-10-02 14:20:30"],
                                    "last_watered": ["2024-09-30 10:00:00",
                                                     "2024-10-01 11:00:00"],
                                    "soil_moisture": [30.0, 45.0],
                                    "temperature": [22.5, 23.0]})

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_clean_with_valid_data(self):
        """Tests that transform returns a correct dataframe given the provided
        data."""
        input_data = pd.DataFrame({"plant_id": [1, 2],
                                   "recording_taken": ["2024-10-01 12:34:56",
                                                       "2024-10-02 14:20:30"],
                                   "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT",
                                                    "Tue, 01 Oct 2024 11:00:00 GMT"],
                                   "soil_moisture": [30.0, 45.0],
                                   "temperature": [22.5, 23.0]})

        result_df = clean(input_data)

        expected_df = pd.DataFrame({"plant_id": [1, 2],
                                    "recording_taken": ["2024-10-01 12:34:56",
                                                        "2024-10-02 14:20:30"],
                                    "last_watered": ["2024-09-30 10:00:00",
                                                     "2024-10-01 11:00:00"],
                                    "soil_moisture": [30.0, 45.0],
                                    "temperature": [22.5, 23.0]})

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_transform_with_invalid_data(self):
        """Tests that an error is raised when the last watered value is
        not a valid date"""
        input_data = pd.DataFrame({"plant_id": [1],
                                   "recording_taken": ["2024-10-01 12:34:56"],
                                   "last_watered": ["Invalid Date"],
                                   "soil_moisture": [30.0],
                                   "temperature": [22.5]})

        with pytest.raises(ValueError):
            transform(input_data)

    def test_clean_with_invalid_data(self):
        """Tests that an error is raised when the last watered value is
        not a valid date"""
        input_data = pd.DataFrame({"plant_id": [1],
                                   "recording_taken": ["2024-10-01 12:34:56"],
                                   "last_watered": ["Invalid Date"],
                                   "soil_moisture": [30.0],
                                   "temperature": [22.5]})

        with pytest.raises(ValueError):
            clean(input_data)

    @patch('transform.send_email')
    def test_check_conditions_temperature_exceeded(self, fake_send_email):
        """Tests that an email is sent when the temperature exceeds 50."""
        input_data = pd.DataFrame({"plant_id": [1],
                                   "recording_taken": ["2024-10-01 12:34:56"],
                                   "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT"],
                                   "soil_moisture": [45.0],
                                   "temperature": [55.0]})

        check_conditions(input_data)

        # Check if send_email is called for high temperature
        fake_send_email.assert_called_with(1, 55.0, 'temperature', 'exceeded')

    @patch('transform.send_email')
    def test_check_conditions_temperature_not_met(self, fake_send_email):
        """Tests that an email is sent when the temperature is below or equal to 5."""
        input_data = pd.DataFrame({"plant_id": [2],
                                   "recording_taken": ["2024-10-02 14:20:30"],
                                   "last_watered": ["Tue, 01 Oct 2024 11:00:00 GMT"],
                                   "soil_moisture": [50.0],
                                   "temperature": [3.0]})

        check_conditions(input_data)

        # Check if send_email is called for low temperature
        fake_send_email.assert_called_with(2, 3.0, 'temperature', 'not met')

    @patch('transform.send_email')
    def test_check_conditions_soil_moisture_exceeded(self, fake_send_email):
        """Tests that an email is sent when the soil moisture exceeds 90."""
        input_data = pd.DataFrame({"plant_id": [1],
                                   "recording_taken": ["2024-10-01 12:34:56"],
                                   "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT"],
                                   "soil_moisture": [95.0],
                                   "temperature": [25.0]})

        check_conditions(input_data)

        # Check if send_email is called for high soil moisture
        fake_send_email.assert_called_with(
            1, 95.0, 'soil moisture', 'exceeded')

    @patch('transform.send_email')
    def test_check_conditions_soil_moisture_not_met(self, fake_send_email):
        """Tests that an email is sent when the soil moisture is below 30."""
        input_data = pd.DataFrame({"plant_id": [2],
                                   "recording_taken": ["2024-10-02 14:20:30"],
                                   "last_watered": ["Tue, 01 Oct 2024 11:00:00 GMT"],
                                   "soil_moisture": [25.0],
                                   "temperature": [22.0]})

        check_conditions(input_data)

        # Check if send_email is called for low soil moisture
        fake_send_email.assert_called_with(2, 25.0, 'soil moisture', 'not met')
