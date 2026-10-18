"""Verifica la preparacion explicita del catalogo de actividades."""

import pytest
from django.core.management import call_command

from core.models import Actividad


@pytest.mark.django_db
def test_cargar_actividades_crea_tirolesa_con_su_capacidad() -> None:
    """Prepara Tirolesa con la capacidad establecida por el dominio."""
    assert not Actividad.objects.exists()

    call_command("cargar_actividades")

    actividad = Actividad.objects.get(nombre="TIROLESA")
    assert actividad.cupo_maximo == 10
