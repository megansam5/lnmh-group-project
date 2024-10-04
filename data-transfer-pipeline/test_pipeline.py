# pylint: skip-file
from unittest.mock import patch
import pandas as pd
import os

from pipeline import full_pipeline


@patch('pipeline.extract_recordings')
@patch('pipeline.load_to_s3')
@patch('pipeline.delete_outdataed_recordings')
def test_full_pipeline(fake_delete, fake_load, fake_extract):

    fake_extract.return_value = pd.DataFrame()

    full_pipeline()

    fake_extract.assert_called_once()
    fake_load.assert_called_once()
    fake_delete.assert_called_once()
