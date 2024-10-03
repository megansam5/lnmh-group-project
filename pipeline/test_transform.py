"""This file tests the functionality of the transform script."""

from unittest import TestCase
from unittest.mock import patch
import pandas as pd
from datetime import datetime
from transform import transform  # Assuming the script is saved as 'transform.py'


class TestTransformFunction(unittest.TestCase):

    @patch('transform.extract')
    def test_transform_with_valid_data(self, mock_extract):
        # Mock DataFrame returned by extract
        mock_extract.return_value = pd.DataFrame({
            "plant_id": [1, 2],
            "recording_taken": ["2024-10-01 12:34:56", "2024-10-02 14:20:30"],
            "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT", "Tue, 01 Oct 2024 11:00:00 GMT"],
            "soil_moisture": [30.0, 45.0],
            "temperature": [22.5, 23.0]
        })

        # Call the transform function
        result_df = transform(mock_extract())

        # Expected DataFrame after transformation
        expected_df = pd.DataFrame({
            "plant_id": [1, 2],
            "recording_taken": [pd.Timestamp("2024-10-01 12:34:56"), pd.Timestamp("2024-10-02 14:20:30")],
            "last_watered": [datetime(2024, 9, 30, 10, 0), datetime(2024, 10, 1, 11, 0)],
            "soil_moisture": [30.0, 45.0],
            "temperature": [22.5, 23.0]
        })

        # Assert DataFrame equality
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('transform.extract')
    def test_transform_with_invalid_recording_taken(self, mock_extract):
        # Mock DataFrame with an invalid date in recording_taken
        mock_extract.return_value = pd.DataFrame({
            "plant_id": [1],
            "recording_taken": ["Invalid Date String"],
            "last_watered": ["Mon, 30 Sep 2024 10:00:00 GMT"],
            "soil_moisture": [30.0],
            "temperature": [22.5]
        })

        # Call the transform function
        result_df = transform(mock_extract())

        # Expected DataFrame with NaT (Not a Time) for invalid recording_taken
        expected_df = pd.DataFrame({
            "plant_id": [1],
            # Invalid date should be converted to NaT
            "recording_taken": [pd.NaT],
            "last_watered": [datetime(2024, 9, 30, 10, 0)],
            "soil_moisture": [30.0],
            "temperature": [22.5]
        })

        # Assert DataFrame equality
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('transform.extract')
    def test_transform_with_invalid_last_watered(self, mock_extract):
        # Mock DataFrame with an invalid last_watered date
        mock_extract.return_value = pd.DataFrame({
            "plant_id": [1],
            "recording_taken": ["2024-10-01 12:34:56"],
            "last_watered": ["Invalid Date String"],
            "soil_moisture": [30.0],
            "temperature": [22.5]
        })

        # Call the transform function with exception handling for invalid last_watered
        with self.assertRaises(ValueError):
            transform(mock_extract())


if __name__ == '__main__':
    unittest.main()
