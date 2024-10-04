"""This file tests the functionality of the etl script."""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from etl import run


class TestRun(TestCase):
    """Tests for the run function."""

    @patch('etl.load')
    @patch('etl.transform')
    @patch('etl.extract')
    @patch('etl.load_dotenv')
    def test_run_success(self, mock_load_dotenv, mock_extract, mock_transform, mock_load):
        """Test the run function to ensure it correctly orchestrates the etl."""
        mock_extracted_data = MagicMock()
        mock_transformed_data = MagicMock()

        mock_extract.return_value = mock_extracted_data
        mock_transform.return_value = mock_transformed_data

        run()

        mock_load_dotenv.assert_called_once()
        mock_extract.assert_called_once()

        mock_transform.assert_called_once_with(mock_extracted_data)
        mock_load.assert_called_once_with(mock_transformed_data)
