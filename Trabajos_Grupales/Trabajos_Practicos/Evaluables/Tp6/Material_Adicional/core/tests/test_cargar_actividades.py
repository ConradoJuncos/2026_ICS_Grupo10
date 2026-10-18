"""Verifica la preparacion explicita del catalogo de actividades."""

import pytest
from django.core.management import call_command

from core.models import Actividad


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nombre, capacidad",
    [("TIROLESA", 10), ("SAFARI", 8), ("PALESTRA", 12), ("JARDINERIA", 12)],
)
def test_cargar_actividades_crea_actividad_con_su_capacidad(
    nombre: str, capacidad: int
) -> None:
    """Prepara cada actividad con la capacidad establecida por el dominio."""
    assert not Actividad.objects.exists()

    call_command("cargar_actividades")

    actividad = Actividad.objects.get(nombre=nombre)
    assert actividad.cupo_maximo == capacidad


@pytest.mark.django_db
def test_repetir_carga_conserva_el_catalogo_sin_duplicados() -> None:
    """Repetir la preparacion conserva los mismos registros y capacidades."""
    call_command("cargar_actividades")
    catalogo_inicial = list(
        Actividad.objects.order_by("nombre").values_list("pk", "nombre", "cupo_maximo")
    )

    call_command("cargar_actividades")

    assert Actividad.objects.count() == 4
    assert (
        list(
            Actividad.objects.order_by("nombre").values_list(
                "pk", "nombre", "cupo_maximo"
            )
        )
        == catalogo_inicial
    )
