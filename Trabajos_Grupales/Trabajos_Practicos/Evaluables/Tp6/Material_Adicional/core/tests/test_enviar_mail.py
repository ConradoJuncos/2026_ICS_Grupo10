from unittest.mock import patch, MagicMock
from django.test import TestCase
from core.email import enviar_mail_confirmacion_registro_a_actividad

class Servicio_Email_Test(TestCase):
    @patch('core.email.smtplib.SMTP')
    def test_enviar_mail_registro_actividad(self, mock_smtp):
        # Mockeo del servidor para no tocar un servidor de mail real
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Act, enviar el mail
        enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"fake-qr-bytes")
        
        # Assert, revisar que el servidor haya sido llamado
        mock_server.send_message.assert_called_once()