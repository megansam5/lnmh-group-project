"""This script connects to and extracts data from the plant API"""
import requests
import pandas as pd


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_request(plant_id) -> dict:
    """Gets and returns the data for a specific plant ."""
    result = requests.get(f"{BASE_URL}{plant_id}", timeout=10)
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
    and then turns it into a dataframe ready for cleaning. """
    plant_count = 0
    recordings = []
    while plant_count < 50:
        plant_data = get_request(plant_count)
        if not plant_data.get("error"):
            recordings.append(build_entry(plant_data))
        plant_count += 1

    return pd.DataFrame(recordings)


if __name__ == "__main__":

    print(extract())
