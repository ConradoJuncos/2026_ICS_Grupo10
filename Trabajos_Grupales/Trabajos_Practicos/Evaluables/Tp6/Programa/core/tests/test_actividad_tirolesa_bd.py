"""Comprueba la persistencia de las actividades."""

import pytest

from core.models import Actividad


@pytest.mark.django_db
def test_crear_actividad_tirolesa() -> None:
    """Guarda la Tirolesa con su nombre y su cupo máximo."""
    actividad = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)

    assert actividad.nombre == "TIROLESA"
    assert actividad.cupo_maximo == 10
