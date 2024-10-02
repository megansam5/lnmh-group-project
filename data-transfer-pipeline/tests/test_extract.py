from unittest.mock import patch, MagicMock
import pandas as pd
from extract import extract_recordings


@patch('extract.create_connection')
@patch('extract.pd.read_sql')
def test_extract_recordings(mock_read_sql, mock_create_connection):
    mock_conn = MagicMock()
    mock_create_connection.return_value = mock_conn

    mock_df = pd.DataFrame({
        'recording_id': [1, 2],
        'plant_id': [1, 2],
        'recording_taken': ['2024-01-01 12:00:00', '2024-01-01 13:00:00'],
        'last_watered': ['2024-01-01 08:00:00', '2024-01-01 09:00:00'],
        'soil_moisture': [80.5, 82.1],
        'temperature': [20.3, 21.5]
    })
    mock_read_sql.return_value = mock_df
    result = extract_recordings()
    mock_read_sql.assert_called_once()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result['recording_id'].iloc[0] == 1
