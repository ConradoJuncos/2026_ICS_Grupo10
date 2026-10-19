from django.test import TestCase

from core.qr import GenerarQr


class test_generacion_qr(TestCase):
    def test_generacion_qr_es_imagen(self):
        qr = GenerarQr()
        resultado = qr.generate("test")

        # Todo archivo PNG comienza con esta firma.
        assert isinstance(resultado, bytes)
        assert resultado.startswith(b"\x89PNG")
