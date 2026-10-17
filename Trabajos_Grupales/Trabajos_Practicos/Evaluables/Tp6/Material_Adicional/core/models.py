from django.db import models

class Actividad(models.Model):
    nombre = models.CharField(max_length=50)
    cupo_maximo = models.PositiveIntegerField()