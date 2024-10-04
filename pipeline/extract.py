"""This script connects to and extracts data from the plant API"""

from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import pandas as pd


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_request(plant_id) -> dict:
    """Gets and returns the data for a specific plant ."""
    result = requests.get(f"{BASE_URL}{plant_id}", timeout=30)
    return result.json()


def build_entry(data: dict) -> dict:
    """This function extracts the vital information and returns an entry containing it."""
    return {"plant_id": data.get("plant_id"),
            "recording_taken": data.get("recording_taken"),
            "last_watered": data.get("last_watered"),
            "soil_moisture": data.get("soil_moisture"),
            "temperature": data.get("temperature")
            }


def extract() -> pd.DataFrame:
    """This function goes through all the plants, extracting the key information,
    and then turns it into a dataframe ready for cleaning."""
    plant_count = 50
    recordings = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_request, plant_id):
                   plant_id for plant_id in range(plant_count+1)}

        for future in as_completed(futures):
            plant_data = future.result()
            if not plant_data.get("error"):
                recordings.append(build_entry(plant_data))

    return pd.DataFrame(recordings).sort_values("plant_id").reset_index(drop=True)


if __name__ == "__main__":
    print(extract())
