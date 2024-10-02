# pylint: skip-file
from unittest.mock import patch, MagicMock

from clean import delete_outdataed_recordings


@patch('clean.create_connection')
def test_delete_outdated_recordings(fake_create_connection):
    fake_conn = MagicMock()
    fake_create_connection.return_value = fake_conn
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor

    delete_outdataed_recordings()

    fake_cursor.execute.assert_called_once()
    fake_conn.commit.assert_called_once()
