from typing import ClassVar

from django.db import models


class Actividad(models.Model):
    OPCIONES_ACTIVIDAD: ClassVar[list[tuple[str, str]]] = [
        ("TIROLESA", "Tirolesa"),
        ("SAFARI", "Safari"),
        ("PALESTRA", "Palestra"),
        ("JARDINERIA", "Jardinería"),
    ]

    nombre = models.CharField(max_length=50, choices=OPCIONES_ACTIVIDAD, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.get_nombre_display()


class Horario(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    def cupos_disponibles(self):
        inscritos = (
            self.inscripciones.count()
        )  # Cuenta cuántas inscripciones tiene este horario
        return self.actividad.cupo_maximo - inscritos

    def registrar_inscripcion(self, nombre_participante):
        if self.cupos_disponibles() <= 0:
            raise ValueError("No hay cupos disponibles para este horario.")

        return self.inscripciones.create(nombre_participante=nombre_participante)


class Inscripcion(models.Model):
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, related_name="inscripciones"
    )
    nombre_participante = models.CharField(max_length=100, blank=True, default="")
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
