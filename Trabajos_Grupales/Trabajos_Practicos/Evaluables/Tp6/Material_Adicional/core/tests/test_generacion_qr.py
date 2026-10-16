from django.test import TestCase
from core.qr import GenerarQr # En la etapa RED esto no existe todavia

class QrGenerationTest(TestCase):
    def test_qr_generator_returns_png_bytes(self):
        qr = GenerarQr()
        result = qr.generate("test")
        
        #magia de python para comprobar que todo esto funcione
        assert isinstance(result, bytes)
        assert result.startswith(b'\x89PNG')