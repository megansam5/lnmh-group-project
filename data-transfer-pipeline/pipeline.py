"""The full pipeline for extracting old data and putting it into s3."""

from extract import extract_recordings
from load import load_to_s3
from clean import delete_outdataed_recordings


def full_pipeline():
    """Runs the full pipeline."""
    recordings = extract_recordings()
    load_to_s3(recordings)
    delete_outdataed_recordings()
    print("Pipeline complete.")


if __name__ == "__main__":
    full_pipeline()