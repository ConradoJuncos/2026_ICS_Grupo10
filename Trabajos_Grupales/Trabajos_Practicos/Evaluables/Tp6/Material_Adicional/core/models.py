from django.db import models

class Actividad(models.Model):
    OPCIONES_ACTIVIDAD = [
        ('TIROLESA', 'Tirolesa'),
        ('SAFARI', 'Safari'),
        ('PALESTRA', 'Palestra'),
        ('JARDINERIA', 'Jardinería'),
    ]

    nombre = models.CharField(
        max_length=50, 
        choices=OPCIONES_ACTIVIDAD, 
        unique=True
    )
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.get_nombre_display()


class Horario(models.Model):
    pass