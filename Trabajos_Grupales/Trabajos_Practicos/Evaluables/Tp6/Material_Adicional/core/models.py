from typing import ClassVar

from django.db import models


class Actividad(models.Model):
    """Actividad del parque con su capacidad por turno."""

    OPCIONES_ACTIVIDAD: ClassVar[list[tuple[str, str]]] = [
        ("TIROLESA", "Tirolesa"),
        ("SAFARI", "Safari"),
        ("PALESTRA", "Palestra"),
        ("JARDINERIA", "Jardinería"),
    ]

    nombre = models.CharField(max_length=50, choices=OPCIONES_ACTIVIDAD, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.get_nombre_display()


class Horario(models.Model):
    """Turno de una actividad en una fecha y hora."""

    fecha = models.DateField()
    hora = models.TimeField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    def cupos_disponibles(self) -> int:
        """Devuelve los lugares que quedan libres en el turno."""
        ocupados = Participante.objects.filter(inscripcion__horario=self).count()
        return self.actividad.cupo_maximo - ocupados


class Inscripcion(models.Model):
    """Reserva de un grupo de participantes en un horario."""

    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, related_name="inscripciones"
    )
    correo = models.EmailField(blank=True, default="")


class Participante(models.Model):
    """Persona incluida en una inscripción."""

    inscripcion = models.ForeignKey(
        Inscripcion, on_delete=models.CASCADE, related_name="participantes"
    )
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    edad = models.PositiveSmallIntegerField()
    talle = models.CharField(max_length=3, blank=True, default="")
