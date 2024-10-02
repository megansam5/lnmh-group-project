# pylint: skip-file
from unittest.mock import patch, MagicMock

import pandas as pd

from load import load_to_s3


@patch('load.client')
@patch.dict('os.environ', {
    'AWS_ACCESS_KEY': 'fake_access_key',
    'AWS_SECRET_KEY': 'fake_secret_key',
    'BUCKET_NAME': 'test-bucket'
})
def test_load_to_s3(fake_boto_client):
    fake_s3_client = MagicMock()
    fake_boto_client.return_value = fake_s3_client

    df = pd.DataFrame({
        'recording_id': [1],
        'plant_id': [1],
        'recording_taken': ['2024-01-01 12:00:00'],
        'last_watered': ['2024-01-01 08:00:00'],
        'soil_moisture': [80.5],
        'temperature': [20.3]
    })

    load_to_s3(df)

    fake_boto_client.assert_called_once_with(
        service_name='s3',
        aws_access_key_id='fake_access_key',
        aws_secret_access_key='fake_secret_key'
    )
    fake_s3_client.upload_fileobj.assert_called_once()
