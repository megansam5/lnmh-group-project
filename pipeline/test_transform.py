"""This file tests the functionality of the transform script."""

from unittest import TestCase
from unittest.mock import patch
from datetime import datetime

import pandas as pd
import pytest

from transform import transform


class TestTransformFunction(TestCase):
    """Tests for the transform function."""

    @patch('transform.extract')
    def test_transform_with_valid_data(self, fake_extract):
        """Tests that transform returns a correct dataframe given the provided
        data."""
        fake_extract.return_value = pd.DataFrame({"plant_id": [1, 2],
                                                  "recording_taken": ["2024-10-01 12:34:56",
                                                                      "2024-10-02 14:20:30"],
                                                  "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT",
                                                                   "Tue, 01 Oct 2024 11:00:00 GMT"],
                                                  "soil_moisture": [30.0, 45.0],
                                                  "temperature": [22.5, 23.0]})

        result_df = transform(fake_extract())

        expected_df = pd.DataFrame({"plant_id": [1, 2],
                                    "recording_taken": [pd.Timestamp("2024-10-01 12:34:56"),
                                                        pd.Timestamp("2024-10-02 14:20:30")],
                                    "last_watered": [datetime(2024, 9, 30, 10, 0),
                                                     datetime(2024, 10, 1, 11, 0)],
                                    "soil_moisture": [30.0, 45.0],
                                    "temperature": [22.5, 23.0]})

        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('transform.extract')
    def test_transform_with_invalid_data(self, fake_extract):
        """Tests that an error is raised when the last watered value is
        not a valid date"""
        fake_extract.return_value = pd.DataFrame({"plant_id": [1],
                                                  "recording_taken": ["2024-10-01 12:34:56"],
                                                  "last_watered": ["Invalid Date"],
                                                  "soil_moisture": [30.0],
                                                  "temperature": [22.5]})

        with pytest.raises(ValueError):
            transform(fake_extract())
