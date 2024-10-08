# pylint: skip-file
from unittest.mock import patch, MagicMock

import pandas as pd

from extract import extract_recordings, create_connection


@patch('pymssql.connect')
@patch.dict('clean.ENV', {
    'DB_HOST': 'fake_host',
    'DB_NAME': 'fake_db',
    'DB_USER': 'fake_user',
    'DB_PASSWORD': 'fake_password'
})
def test_create_connection(fake_connect):
    fake_conn = MagicMock()
    fake_connect.return_value = fake_conn
    conn = create_connection()

    fake_connect.assert_called_once_with(
        server='fake_host',
        database='fake_db',
        user='fake_user',
        password='fake_password',
        port=1433,
        as_dict=True
    )

    assert conn == fake_conn


@patch('extract.create_connection')
def test_extract_recordings(fake_create_connection):
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    fake_cursor.fetchall.return_value = [
        {'recording_id': 1, 'plant_id': 1, 'recording_taken': '2024-01-01 12:00:00',
            'last_watered': '2024-01-01 08:00:00', 'soil_moisture': 80.5, 'temperature': 20.3},
        {'recording_id': 2, 'plant_id': 2, 'recording_taken': '2024-01-01 13:00:00',
            'last_watered': '2024-01-01 09:00:00', 'soil_moisture': 82.1, 'temperature': 21.5},
    ]

    result = extract_recordings()

    assert fake_cursor.execute.called
    assert fake_cursor.fetchall.called

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'recording_id' in result.columns
    assert 'plant_id' in result.columns
    assert 'recording_taken' in result.columns
    assert 'last_watered' in result.columns
    assert 'soil_moisture' in result.columns
    assert 'temperature' in result.columns
