from unittest.mock import patch, MagicMock
from django.test import TestCase
from core.email import enviar_mail_confirmacion_registro_a_actividad

class Servicio_Email_Test(TestCase):
    @patch('core.email.smtplib.SMTP')
    def test_enviar_mail_registro_actividad(self, mock_smtp):
        # Mock the context manager so it doesn't hit a real server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Act
        enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"fake-qr-bytes")
        
        # Assert that send_message was called on our mock server
        mock_server.send_message.assert_called_once()