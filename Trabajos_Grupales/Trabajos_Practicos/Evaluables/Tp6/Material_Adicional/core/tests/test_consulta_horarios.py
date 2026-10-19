"""Comprueba la consulta de horarios desde la base de datos."""

from collections.abc import Iterator
from datetime import UTC, date, datetime, time
from unittest.mock import patch

import pytest

from core.consulta_horarios import consultar_horarios_por_actividad
from core.models import Actividad, Horario


@pytest.fixture(autouse=True)
def reloj_controlado() -> Iterator[None]:
    """Fija el reloj para que las consultas no dependan del día de ejecución."""
    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 8, tzinfo=UTC),
    ):
        yield


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "fecha_cierre",
    [
        pytest.param(date(2026, 10, 19), id="lunes"),
        pytest.param(date(2027, 1, 1), id="anio_nuevo"),
        pytest.param(date(2026, 12, 25), id="navidad"),
    ],
)
def test_consulta_excluye_horarios_en_dias_de_cierre(fecha_cierre: date) -> None:
    """No ofrece horarios persistidos en días en que el parque está cerrado."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    Horario.objects.create(actividad=tirolesa, fecha=fecha_cierre, hora=time(9))

    horarios = consultar_horarios_por_actividad(tirolesa)

    assert horarios == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "hora_invalida",
    [
        pytest.param(time(8), id="antes_del_primer_turno"),
        pytest.param(time(18), id="despues_del_ultimo_turno"),
        pytest.param(time(9, 30), id="hora_fraccionada"),
    ],
)
def test_consulta_excluye_horas_de_inicio_no_permitidas(hora_invalida: time) -> None:
    """Conserva el turno de las 17:00 y excluye los inicios no permitidos."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    fecha = date(2026, 10, 20)
    horario_valido = Horario.objects.create(
        actividad=tirolesa, fecha=fecha, hora=time(17)
    )
    Horario.objects.create(actividad=tirolesa, fecha=fecha, hora=hora_invalida)

    horarios = consultar_horarios_por_actividad(tirolesa, fecha=fecha)

    assert horarios == [horario_valido]


@pytest.mark.django_db
def test_consulta_excluye_turnos_a_mas_de_24_horas() -> None:
    """Conserva un turno a una hora y excluye otro a veinticinco horas."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    horario_cercano = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(9)
    )
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9))

    horarios = consultar_horarios_por_actividad(tirolesa)

    assert horarios == [horario_cercano]
