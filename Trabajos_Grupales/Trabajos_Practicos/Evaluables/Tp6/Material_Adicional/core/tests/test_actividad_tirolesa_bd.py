from django.test import TestCase
from core.models import Actividad  # This model doesn't exist yet

class TestActividades(TestCase):
    def test_crear_actividad_tirolesa(self):
        actividad = Actividad.objects.create(nombre='TIROLESA', cupo_maximo=10)
        self.assertEqual(actividad.nombre, 'TIROLESA')
        self.assertEqual(actividad.cupo_maximo, 10)