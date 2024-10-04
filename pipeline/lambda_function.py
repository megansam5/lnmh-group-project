"""this script is a lambda handler and handles events."""

from etl import run


def lambda_handler(event: dict, context) -> dict:
    """This function processes events"""
    run()
    return {}
