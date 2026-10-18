"""Verifica la preparacion explicita del catalogo de actividades."""

import pytest
from django.core.management import call_command

from core.models import Actividad


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nombre, capacidad", [("TIROLESA", 10), ("SAFARI", 8), ("PALESTRA", 12)]
)
def test_cargar_actividades_crea_actividad_con_su_capacidad(
    nombre: str, capacidad: int
) -> None:
    """Prepara cada actividad con la capacidad establecida por el dominio."""
    assert not Actividad.objects.exists()

    call_command("cargar_actividades")

    actividad = Actividad.objects.get(nombre=nombre)
    assert actividad.cupo_maximo == capacidad
