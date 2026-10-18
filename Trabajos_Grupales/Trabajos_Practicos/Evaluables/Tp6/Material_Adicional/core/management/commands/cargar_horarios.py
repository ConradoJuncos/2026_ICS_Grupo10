"""Carga horarios de muestra para los próximos siete días abiertos."""

from datetime import time, timedelta
from typing import Any

from django.core.management import BaseCommand, call_command
from django.utils import timezone

from core.models import Actividad, Horario


class Command(BaseCommand):
    """Genera horarios de muestra respetando los días y horas de apertura."""

    help = "Carga horarios de muestra para los próximos siete días abiertos."

    def handle(self, *args: Any, **options: Any) -> None:
        call_command("cargar_actividades")
        actividades = Actividad.objects.all()
        fecha = timezone.localdate() + timedelta(days=1)
        dias_abiertos = 0
        horarios_creados = 0

        while dias_abiertos < 7:
            es_feriado = (fecha.month, fecha.day) in {(1, 1), (12, 25)}
            if fecha.weekday() != 0 and not es_feriado:
                dias_abiertos += 1
                for actividad in actividades:
                    for hora in range(9, 18):
                        _, creado = Horario.objects.get_or_create(
                            fecha=fecha,
                            hora=time(hour=hora),
                            actividad=actividad,
                        )
                        horarios_creados += creado
            fecha += timedelta(days=1)

        self.stdout.write(f"Horarios de muestra creados: {horarios_creados}")
