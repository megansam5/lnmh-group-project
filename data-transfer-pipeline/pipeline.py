"""The full pipeline for extracting old data and putting it into s3."""
from time import perf_counter

from extract import extract_recordings
from load import load_to_s3
from clean import delete_outdataed_recordings


def full_pipeline():
    """Runs the full pipeline."""
    start = perf_counter()
    recordings = extract_recordings()
    load_to_s3(recordings)
    delete_outdataed_recordings()
    end = perf_counter()
    print("Pipeline complete.")
    print(end - start)


if __name__ == "__main__":
    full_pipeline()
