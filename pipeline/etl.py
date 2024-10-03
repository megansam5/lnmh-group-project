

from os import environ as ENV
from dotenv import load_dotenv

from extract import extract
from transform import transform
from load import load

if __name__ == "__main__":
    load_dotenv()
    load(transform(extract()))
