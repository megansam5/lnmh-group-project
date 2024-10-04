"""This script runs the pipeline"""

from dotenv import load_dotenv

from extract import extract
from transform import transform
from load import load


def run():
    """This function runs all the components."""
    load_dotenv()
    load(transform(extract()))


if __name__ == "__main__":
    run()
