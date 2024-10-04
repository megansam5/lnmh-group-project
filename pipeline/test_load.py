"""This file tests the functionality of the load script."""

from unittest import TestCase
from unittest.mock import patch, MagicMock

import pandas as pd

from load import load


class TestLoad(TestCase):
    """Tests for the load function."""

    @patch('load.create_connection')
    def test_load_function(self, mock_create_connection):
        """Test that the load function correctly calls the correct methods and functions."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_create_connection.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_data = pd.DataFrame({
            'plant_id': [1, 2],
            'recording_taken': ['2024-10-01 12:34:56', '2024-10-02 14:20:30'],
            'last_watered': ['2024-09-30 10:00:00', '2024-10-01 11:00:00'],
            'soil_moisture': [30.0, 45.0],
            'temperature': [22.5, 23.0]
        })

        load(mock_data)

        mock_cursor.executemany.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
