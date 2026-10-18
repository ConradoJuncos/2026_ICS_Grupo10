"""Prepara explicitamente el catalogo de actividades del parque."""

from typing import Any

from django.core.management.base import BaseCommand

from core.models import Actividad


class Command(BaseCommand):
    """Carga las actividades necesarias para preparar el parque."""

    help = "Carga el catalogo de actividades del parque."

    def handle(self, *args: Any, **options: Any) -> None:
        """Ejecuta la preparacion del catalogo."""
        Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
        Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
