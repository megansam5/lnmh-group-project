"""This file tests the functionality of the transform script."""

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
