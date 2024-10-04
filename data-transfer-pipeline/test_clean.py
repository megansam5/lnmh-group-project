from unittest.mock import patch, MagicMock
import pandas as pd

from clean import delete_outdataed_recordings, fetch_current_averages, update_plant_average, \
    insert_new_plant_average, calculate_new_averages, process_and_update_averages


@patch('clean.create_connection')
def test_delete_outdated_recordings(fake_create_connection):
    fake_conn = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    delete_outdataed_recordings()

    assert fake_cursor.execute.called
    assert fake_conn.commit.called


@patch('clean.create_connection')
def test_fetch_current_averages(fake_create_connection):
    fake_conn = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    fake_cursor.fetchone.return_value = (25.0, 30.0, 100)

    result = fetch_current_averages(fake_conn, plant_id=1)

    assert fake_cursor.execute.called
    assert result == (25.0, 30.0, 100)


@patch('clean.create_connection')
def test_update_plant_average(fake_create_connection):
    fake_conn = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    update_plant_average(fake_conn, plant_id=1, avg_temp=22.5,
                         avg_soil_moisture=40.0, recordings=50)

    assert fake_cursor.execute.called
    assert fake_conn.commit.called


@patch('clean.create_connection')
def test_insert_new_plant_average(fake_create_connection):
    fake_conn = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    insert_new_plant_average(
        fake_conn, plant_id=1, avg_temp=22.5, avg_soil_moisture=40.0, recordings=50)

    assert fake_cursor.execute.called
    assert fake_conn.commit.called


def test_calculate_new_averages():
    data = {
        'plant_id': [1, 1, 2, 2],
        'temperature': [25.0, 26.0, 30.0, 32.0],
        'soil_moisture': [40.0, 42.0, 50.0, 52.0]
    }
    recordings = pd.DataFrame(data)

    result_df = calculate_new_averages(recordings)

    expected_data = {
        'plant_id': [1, 2],
        'new_avg_temp': [25.5, 31.0],
        'new_avg_soil_moisture': [41.0, 51.0],
        'new_recordings': [2, 2]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result_df, expected_df)


@patch('clean.create_connection')
@patch('clean.fetch_current_averages')
@patch('clean.update_plant_average')
@patch('clean.insert_new_plant_average')
def test_process_and_update_averages(mock_insert_new, mock_update, mock_fetch_current, mock_create_connection):

    fake_conn = MagicMock()
    mock_create_connection.return_value = fake_conn

    mock_fetch_current.side_effect = [
        {'average_temperature': 25.0,
            'average_soil_moisture': 40.0, 'recording_count': 100},
        None
    ]

    data = {
        'plant_id': [1, 2],
        'temperature': [26.0, 32.0],
        'soil_moisture': [42.0, 52.0]
    }
    recordings = pd.DataFrame(data)

    process_and_update_averages(recordings)

    mock_fetch_current.assert_any_call(fake_conn, 1)
    mock_fetch_current.assert_any_call(fake_conn, 2)

    assert mock_update.called

    assert mock_insert_new.called

    fake_conn.commit.assert_called_once()
