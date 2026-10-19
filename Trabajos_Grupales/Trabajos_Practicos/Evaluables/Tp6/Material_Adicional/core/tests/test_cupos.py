from django.test import TestCase
from core.models import Actividad, Horario, Inscripcion
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

    def test_reserva_reduce_disponibilidad(self):
        # Creamos una inscripción para ese horario
        Inscripcion.objects.create(horario=self.horario, nombre_participante="Ana")
        
        # Ahora el cupo debería ser 9
        self.assertEqual(self.horario.cupos_disponibles(), 9)

    def test_no_se_puede_reservar_si_no_hay_cupo(self):
        # Llenamos el cupo (supongamos que es 1 para este test)
        actividad_pequena = Actividad.objects.create(nombre='PALESTRA', cupo_maximo=1)
        h1 = Horario.objects.create(actividad=actividad_pequena, fecha=date(2024, 10, 10), hora=time(12, 0))
        
        Inscripcion.objects.create(horario=h1, nombre_participante="Ana")
        
        # El siguiente intento debería fallar (podemos lanzar una excepción personalizada)
        with self.assertRaises(ValueError): 
            # Aquí llamaremos a un método que "valide y guarde"
            h1.registrar_inscripcion("Juan")
            