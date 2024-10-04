"""A script to send an email if the plant has too high temp or too low moisture."""
from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from dotenv import load_dotenv
import boto3

from load import create_connection


def send_email(plant_id: int, value: float, value_type: str) -> None:
    """Sends an email to the correct botanist if the plants conditions are worrying."""
    load_dotenv()
    html = generate_html(plant_id, value, value_type)
    client = boto3.client("ses", region_name="eu-west-2")
    message = MIMEMultipart()
    message["Subject"] = f"Plant {plant_id} Alert!"
    body = MIMEText(
        html,
        "html")
    message.attach(body)

    client.send_raw_email(
        Source=ENV['FROM_EMAIL'],
        Destinations=[
            ENV['TO_EMAIL1'],
            ENV['TO_EMAIL2'],
            ENV['TO_EMAIL3'],
            ENV['TO_EMAIL4']
        ],
        RawMessage={
            'Data': message.as_string()
        }
    )


def generate_html(plant_id: int, value: float, value_type: str) -> str:
    """Generates the html report to email."""
    extra_info = get_botanist_info(plant_id)
    botanist_name = extra_info['botanist_name']
    botanist_email = extra_info['botanist_email']
    plant_name = extra_info['plant_name']
    if value_type == 'temperature':
        unit = '°C'
    else:
        unit = '%'
    value = round(value, 2)
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
            <h2>Automated Botany Alert</h2>
            <p>Dear {botanist_name} ({botanist_email}),</p>
            <p>
                This is an automated email to inform you that the {value_type} for the plant
                <strong>{plant_name}</strong> with the ID <strong>{plant_id}</strong> has recorded a value of <strong>{value}{unit}</strong>.
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

    send_email(13, 76.2, 'temperature')
