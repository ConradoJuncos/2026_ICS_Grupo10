from django.test import TestCase
from core.email import send_qr_email  # En la etapa RED esto todavia no existe

class Servicio_Email_Test(TestCase):
    def test_enviar_mail_registro_actividad(self):
        enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"fake-qr-bytes")