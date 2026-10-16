from unittest.mock import patch
from django.test import TestCase
from core.email import enviar_mail_confirmacion_registro_a_actividad

class ServicioEmailTest(TestCase):
    # Mockeamos la clase SMTP para evitar enviar correos reales durante las pruebas
    @patch('core.email.smtplib.SMTP')
    def test_enviar_mail_registro_actividad_calls_smtp(self, mock_smtp):
        # Arrange: Configuramos el mock para simular el comportamiento de SMTP
        enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"fake-qr-bytes")
        
        # Assert: Revisar que la conexion SMTP fue llamada una vez
        mock_smtp.assert_called_once()