from django.db import connection
from django.test import TestCase

class ConexionBaseDeDatosActividades(TestCase):
    def test_base_de_datos_actividades(self):
        # Asegurarse que la conección puede realizarse
        connection.ensure_connection()
        
        # Verificar que la conexión exista y sea usable
        self.assertTrue(connection.is_usable())