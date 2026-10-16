from django.test import TestCase
from core.email import enviar_mail_confirmacion_registro_a_actividad

class Servicio_Email_Test(TestCase):
    def test_enviar_mail_registro_actividad(self):
        enviar_mail_confirmacion_registro_a_actividad("test@example.com", b"fake-qr-bytes")