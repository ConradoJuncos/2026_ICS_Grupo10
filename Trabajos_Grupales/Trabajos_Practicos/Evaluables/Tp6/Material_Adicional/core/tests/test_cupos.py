from django.test import TestCase
from core.models import Actividad, Horario
from datetime import date, time

class CuposTest(TestCase):
    def setUp(self):
        # Configuramos una actividad con 10 cupos
        self.tirolesa = Actividad.objects.create(nombre='TIROLESA', cupo_maximo=10)
        self.horario = Horario.objects.create(
            actividad=self.tirolesa, 
            fecha=date(2024, 10, 10), 
            hora=time(10, 0)
        )

    def test_horario_nuevo_tiene_disponibilidad_total(self):
        # El cupo disponible debería ser igual al cupo máximo de la actividad
        self.assertEqual(self.horario.cupos_disponibles(), 10)

