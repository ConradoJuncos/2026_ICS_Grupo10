from django.test import TestCase
from core.qr import GenerarQr # En la etapa RED esto no existe todavia

class test_generacion_qr(TestCase):
    def test_generacion_qr_es_imagen(self):
        # Arrange, carga todo lo necesario para hacer el test
        qr = GenerarQr()
        # resultado mockeado, tan solo comprueba que funcione la generacion
        resultado = qr.generate("test")
        
        # Assert, magia de python para comprobar que todo esto funcione
        # revisa que sea instancia de bytes, y que el byte comience con
        # los bytes de png usuales
        assert isinstance(resultado, bytes)
        assert resultado.startswith(b'\x89PNG')