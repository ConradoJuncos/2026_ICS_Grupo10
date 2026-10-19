"""Comprueba la consulta de horarios desde la base de datos."""

from datetime import date, time

import pytest

from core.consulta_horarios import consultar_horarios_por_actividad
from core.models import Actividad, Horario


@pytest.mark.django_db
def test_consulta_devuelve_solo_horarios_de_la_actividad_seleccionada() -> None:
    """Incluye el horario elegido y excluye el de otra actividad."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    safari = Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
    horario_tirolesa = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(9)
    )
    Horario.objects.create(actividad=safari, fecha=date(2026, 10, 20), hora=time(9))

    horarios = consultar_horarios_por_actividad(tirolesa)

    assert horarios == [horario_tirolesa]


@pytest.mark.django_db
def test_consulta_devuelve_solo_horarios_de_la_fecha_seleccionada() -> None:
    """Excluye horarios de la misma actividad en otra fecha."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    fecha_seleccionada = date(2026, 10, 20)
    horario_seleccionado = Horario.objects.create(
        actividad=tirolesa, fecha=fecha_seleccionada, hora=time(9)
    )
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9))

    horarios = consultar_horarios_por_actividad(tirolesa, fecha=fecha_seleccionada)

    assert horarios == [horario_seleccionado]
