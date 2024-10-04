from unittest import TestCase
from unittest.mock import patch, MagicMock

from emailing import send_email, generate_html, get_botanist_info


class TestEmailingFunction(TestCase):
    """Tests for emailing.py functions"""

    @patch('emailing.boto3.client')
    @patch('emailing.generate_html')
    @patch.dict('emailing.ENV', {'FROM_EMAIL': 'test_from@example.com', 'TO_EMAIL': 'test_to@example.com'})
    def test_send_email(self, fake_generate_html, fake_boto_client):
        """Test that send_email sends an email with the correct parameters."""
        fake_generate_html.return_value = "<html>Test Email Content</html>"

        fake_ses_client = MagicMock()
        fake_boto_client.return_value = fake_ses_client

        send_email(plant_id=1, value=75.0,
                   value_type='temperature', condition='exceeded')

        fake_generate_html.assert_called_once_with(
            1, 75.0, 'temperature', 'exceeded')

        fake_ses_client.send_raw_email.assert_called_once_with(
            Source='test_from@example.com',
            Destinations=['test_to@example.com'],
            RawMessage={
                'Data': fake_ses_client.send_raw_email.call_args[1]['RawMessage']['Data']}
        )

    def test_generate_html(self):
        """Test that generate_html returns the correct HTML content."""
        fake_botanist_info = {
            'botanist_name': 'Dr. Green',
            'botanist_email': 'dr.green@example.com',
            'plant_name': 'Aloe Vera'
        }

        with patch('emailing.get_botanist_info', return_value=fake_botanist_info):
            html_output = generate_html(
                plant_id=1, value=75.0, value_type='temperature', condition='exceeded')

        self.assertIn('Dr. Green', html_output)
        self.assertIn('dr.green@example.com', html_output)
        self.assertIn('Aloe Vera', html_output)
        self.assertIn('75.0°C', html_output)
        self.assertIn('higher', html_output)

    @patch.dict('os.environ', {'SCHEMA_NAME': 'fake_schema'})
    @patch('emailing.create_connection')
    def test_get_botanist_info(self, fake_create_connection):
        """Test that get_botanist_info returns correct data from the database."""

        fake_conn = MagicMock()
        fake_cursor = MagicMock()
        fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
        fake_create_connection.return_value = fake_conn

        fake_cursor.fetchone.return_value = {
            'botanist_name': 'Dr. Green',
            'botanist_email': 'dr.green@example.com',
            'plant_name': 'Aloe Vera'
        }

        result = get_botanist_info(1)

        fake_cursor.execute.assert_called

        self.assertEqual(result, {
            'botanist_name': 'Dr. Green',
            'botanist_email': 'dr.green@example.com',
            'plant_name': 'Aloe Vera'
        })
