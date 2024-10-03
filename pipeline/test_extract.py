"""This file tests the functionality of the extract script."""

from unittest.mock import patch, MagicMock
import pytest
import requests

from extract import get_request, build_entry


@patch("extract.requests.get")
def test_get_request_success(fake_request_get):
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
def test_get_request_timeout(fake_request_get):
    """Tests that a timeout is correctly raised in the event of the API call
    timing out."""
    fake_request_get.side_effect = requests.Timeout

    plant_id = 1

    with pytest.raises(requests.Timeout):
        get_request(plant_id)


def test_build_entry_complete_data():
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


def test_build_entry_missing_data():
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
