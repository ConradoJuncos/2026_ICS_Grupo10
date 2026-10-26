"""Prepara explicitamente el catalogo de actividades del parque."""

from typing import Any

from django.core.management.base import BaseCommand

from core.models import CUPO_MAXIMO_POR_ACTIVIDAD, Actividad


class Command(BaseCommand):
    """Carga las actividades necesarias para preparar el parque."""

    help = "Carga el catalogo de actividades del parque."

    def handle(self, *args: Any, **options: Any) -> None:
        """Ejecuta la preparacion del catalogo."""
        for nombre, cupo_maximo in CUPO_MAXIMO_POR_ACTIVIDAD.items():
            Actividad.objects.get_or_create(
                nombre=nombre, defaults={"cupo_maximo": cupo_maximo}
            )
