"""A script to send an email if the plant has too high temp or too low moisture."""
from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from dotenv import load_dotenv
import boto3

from load import create_connection


def send_email(plant_id: int, value: float, value_type: str, condition:str ) -> None:
    """
    Sends an email to the correct botanist if the plants conditions are worrying.
    Example inputs - plant_id: 1, value: 10000, value_type: 'temperature', condition: 'exceeded'.
    """

    load_dotenv()
    html = generate_html(plant_id, value, value_type, condition)
    client = boto3.client("ses", region_name="eu-west-2")
    message = MIMEMultipart()
    
    message["Subject"] = f"PLANT ALERT! ACCEPTABLE {value_type.upper()} LEVEL {condition.upper()}"
    body = MIMEText(
        html,
        "html")
    message.attach(body)

    # client.send_raw_email(
    #     Source=ENV['FROM_EMAIL'],
    #     Destinations=[
    #         ENV['TO_EMAIL1'],
    #         ENV['TO_EMAIL2'],
    #         ENV['TO_EMAIL3'],
    #         ENV['TO_EMAIL4']
    #     ],
    #     RawMessage={
    #         'Data': message.as_string()
    #     }
    # )

    client.send_raw_email(
        Source='trainee.andrew.mcwilliam@sigmalabs.co.uk',
        Destinations=[
        'trainee.andrew.mcwilliam@sigmalabs.co.uk'
        ],
        RawMessage={
            'Data': message.as_string()
        }
    )


def generate_html(plant_id: int, value: float, value_type: str, condition:str) -> str:
    """
    Generates the html report to email.
    Example inputs - plant_id: 1, value: 10000, value_type: 'temperature', condition: 'exceeded'.
    """

    extra_info = get_botanist_info(plant_id)
    botanist_name = extra_info['botanist_name']
    botanist_email = extra_info['botanist_email']
    plant_name = extra_info['plant_name']
    if value_type == 'temperature':
        unit = '°C'
    else:
        unit = '%'

    if condition == 'exceeded':
        implication = 'higher'
    else:
        implication = 'lower'

    value = round(value, 2)

    # 'soil moisture' is a string of two items, so in order to capitalise 
    # in this case, it's necessary to split the items in to a list, iterate
    # over it to and capitalise, then join the list into a final string.
    capitalised_value_type = ' '.join(word.capitalize() for word in value_type.split())

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                padding: 20px;
                background-color: #f4f4f9;
                border-radius: 8px;
                width: 600px;
                margin: auto;
            }}
            h2 {{
                color: #4CAF50;
            }}
            p {{
                margin: 0 0 20px;
            }}
            .footer {{
                font-size: 0.9em;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Automated Botany Alert: Acceptable {capitalised_value_type} Range {condition.capitalize()}</h2>
            <p>Dear {botanist_name} ({botanist_email}),</p>
            <p>
                This is an automated email to inform you that the {value_type} for the plant
                <strong>{plant_name}</strong> with the ID <strong>{plant_id}</strong> has recorded a value of <strong>{value}{unit}</strong>, 
                which is <strong>{implication}</strong> than what we expect on our system.
            </p>
            <p>Kind regards,</p>
            <p>The Botany Team</p>
            <div class="footer">
                <p>Please do not reply to this email. This is an automated message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def get_botanist_info(plant_id: int):
    """Gets the correct botanist name and email."""
    load_dotenv()

    query = f"""
        SELECT b.botanist_name, b.botanist_email, p.plant_name
        FROM {ENV['SCHEMA_NAME']}.plant as p
        JOIN {ENV['SCHEMA_NAME']}.botanist as b
        ON b.botanist_id=p.botanist_id
        WHERE p.plant_id = %s"""

    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, (plant_id,))
        data = cursor.fetchone()

    return data


if __name__ == "__main__":
    # Test cases, simulating emails being sent when 
    # upper and lower boundaries are exceeded

    # Soil moisture exceed upper bound of 90. 
    send_email(13, 95.2, 'soil moisture', 'exceeded')

    # # Soil moisture doesn't meet lower bound of 30. 
    # send_email(13, 12, 'soil moisture', 'not met')

    # # Temperature exceeds upper bound of 50.
    # send_email(13, 55, 'temperature', 'exceeds')

    # # Temperature exceeds lower bound of 5.
    # send_email(13, 2, 'temperature', 'not met')
