"""Prepara explicitamente el catalogo de actividades del parque."""

from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Carga las actividades necesarias para preparar el parque."""

    help = "Carga el catalogo de actividades del parque."

    def handle(self, *args: Any, **options: Any) -> None:
        """Ejecuta la preparacion del catalogo."""
