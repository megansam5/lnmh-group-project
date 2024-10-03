"""This file tests the functionality of the extract script."""

from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
import pytest
import requests

from concurrent.futures import Future
import pandas as pd

from extract import get_request, build_entry, extract


class TestGetRequest(TestCase):
    """Tests for the get request function."""

    @patch("extract.requests.get")
    def test_get_request_success(self, fake_request_get):
        """Tests that the get_request function calls the correct requests method and returns
        an appropriate dictionary."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "test"}
        fake_request_get.return_value = mock_response

        plant_id = 1
        expected_result = {"id": 1, "name": "test"}
        result = get_request(plant_id)

        assert fake_request_get.called
        assert isinstance(result, dict)
        assert result == expected_result

    @patch("extract.requests.get")
    def test_get_request_timeout(self, fake_request_get):
        """Tests that a timeout is correctly raised in the event of the API call
        timing out."""
        fake_request_get.side_effect = requests.Timeout

        plant_id = 1

        with pytest.raises(requests.Timeout):
            get_request(plant_id)


class TestBuildEntry(TestCase):
    """Tests for the build entry function."""

    def test_build_entry_complete_data(self):
        """Tests that build entry returns a dict with the correct information when given all values."""
        input = {
            "plant_id": 1,
            "recording_taken": "2024-10-03 12:43:48",
            "last_watered": "Wed, 02 Oct 2024 13:54:32 GMT",
            "soil_moisture": 30.5,
            "temperature": 22.5,
            "useless": "test"
        }

        expected_output = {
            "plant_id": 1,
            "recording_taken": "2024-10-03 12:43:48",
            "last_watered": "Wed, 02 Oct 2024 13:54:32 GMT",
            "soil_moisture": 30.5,
            "temperature": 22.5
        }

        result = build_entry(input)

        assert result == expected_output

    def test_build_entry_missing_data(self):
        """Tests that build entry still returns a dict even if given missing values."""
        input_data = {
            "plant_id": 1,
            "soil_moisture": 20.5
        }

        expected_output = {
            "plant_id": 1,
            "recording_taken": None,
            "last_watered": None,
            "soil_moisture": 20.5,
            "temperature": None
        }

        result = build_entry(input_data)

        assert result == expected_output


class TestExtractFunction(TestCase):
    """Tests for the extract function."""

    @patch('extract.build_entry')
    @patch('extract.get_request')
    @patch('extract.as_completed')
    @patch('extract.ThreadPoolExecutor')
    def test_extract_success(self, fake_executor, fake_as_completed, fake_get_request, fake_build_entry):
        plant_data_1 = {"plant_id": 1,
                        "recording_taken": "2024-10-01", "soil_moisture": 30.0}
        plant_data_2 = {"plant_id": 2,
                        "recording_taken": "2024-10-01", "soil_moisture": 45.0}
        plant_data_3 = {"plant_id": 3,
                        "recording_taken": "2024-10-01", "soil_moisture": 25.0}

        fake_build_entry.side_effect = [
            {"plant_id": 1, "recording_taken": "2024-10-01", "soil_moisture": 30.0},
            {"plant_id": 2, "recording_taken": "2024-10-01", "soil_moisture": 45.0},
            {"plant_id": 3, "recording_taken": "2024-10-01", "soil_moisture": 25.0},
        ]

        fake_executor.return_value.__enter__.return_value = fake_executor

        future1 = MagicMock(spec=Future)
        future1.result.return_value = plant_data_1

        future2 = MagicMock(spec=Future)
        future2.result.return_value = plant_data_2

        future3 = MagicMock(spec=Future)
        future3.result.return_value = plant_data_3

        fake_as_completed.return_value = [future1, future2, future3]

        result_df = extract()

        expected_df = pd.DataFrame([
            {"plant_id": 1, "recording_taken": "2024-10-01", "soil_moisture": 30.0},
            {"plant_id": 2, "recording_taken": "2024-10-01", "soil_moisture": 45.0},
            {"plant_id": 3, "recording_taken": "2024-10-01", "soil_moisture": 25.0}
        ]).sort_values("plant_id").reset_index(drop=True)

        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('extract.get_request')
    @patch('extract.as_completed')
    @patch('extract.ThreadPoolExecutor')
    def test_extract_with_error_handling(self, fake_executor, fake_as_completed, fake_get_request):
        """Tests that the extract function works as intended if one of the plants has an error."""
        fake_get_request.side_effect = [{"error": "Plant not found"},
                                        {"plant_id": 1, "recording_taken": "2024-10-01",
                                         "soil_moisture": 30.0},]

        fake_executor.return_value.__enter__.return_value = fake_executor

        future1 = Mock(spec=Future)
        future1.result.return_value = {"error": "Plant not found"}

        future2 = Mock(spec=Future)
        future2.result.return_value = {
            "plant_id": 1, "recording_taken": "2024-10-03 12:43:48",
            "last_watered": "Wed, 02 Oct 2024 13: 54: 32 GMT", "soil_moisture": 30.0, "temperature": 20.0}

        fake_as_completed.return_value = [future1, future2]

        result_df = extract()

        expected_df = pd.DataFrame([
            {"plant_id": 1, "recording_taken": "2024-10-03 12:43:48",
                "last_watered": "Wed, 02 Oct 2024 13: 54: 32 GMT", "soil_moisture": 30.0, "temperature": 20.0}
        ]).sort_values("plant_id").reset_index(drop=True)

        print(result_df)
        pd.testing.assert_frame_equal(result_df, expected_df)
