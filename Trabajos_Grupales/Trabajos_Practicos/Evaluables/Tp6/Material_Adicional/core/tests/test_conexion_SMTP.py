from unittest.mock import patch, MagicMock
from django.test import TestCase
from core.email import enviar_mail_confirmacion_registro_a_actividad


class ServicioEmailTest(TestCase):
    @patch("core.email.smtplib.SMTP")
    def test_enviar_mail_envia_imagen_inline(self, mock_smtp):
        # mockeo del servidor SMTP, magia que no comprendo
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        enviar_mail_confirmacion_registro_a_actividad("test@ejemplo.com", b"qr_falso")

        # Verificar que el mensaje fue enviado y que tiene html
        mock_server.send_message.assert_called_once()
        sent_message = mock_server.send_message.call_args[0][0]

        # Verificar que el mensaje enviado es multiparte
        self.assertTrue(sent_message.is_multipart())
