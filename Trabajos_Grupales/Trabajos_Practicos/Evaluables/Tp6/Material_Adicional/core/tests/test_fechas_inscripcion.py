"""Comprueba las fechas reservables que recibe el formulario de inscripción."""

from datetime import UTC, date, datetime, time
from unittest.mock import patch

import pytest
from django.test import Client

from core.models import Actividad, Horario


@pytest.mark.django_db
def test_inscripcion_ofrece_fechas_reservables_ordenadas_sin_repetir(
    client: Client,
) -> None:
    """Entrega al template fechas con turnos reservables, únicas y ordenadas."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9))
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17))
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(10))
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 22), hora=time(9))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 16, 30, tzinfo=UTC),
    ):
        respuesta = client.get("/inscripcion/?actividad=tirolesa")

    assert respuesta.status_code == 200
    assert respuesta.context.get("fechas_disponibles", []) == [
        date(2026, 10, 20),
        date(2026, 10, 21),
    ]


@pytest.mark.django_db
def test_inscripcion_ofrece_horarios_de_la_actividad_y_fecha_elegidas(
    client: Client,
) -> None:
    """Excluye horarios de otra actividad o fecha al preparar el formulario."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    safari = Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
    horario_elegido = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9)
    )
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17))
    Horario.objects.create(actividad=safari, fecha=date(2026, 10, 21), hora=time(10))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 16, 30, tzinfo=UTC),
    ):
        respuesta = client.get(
            "/inscripcion/", {"actividad": "tirolesa", "fecha": "2026-10-21"}
        )

    assert respuesta.status_code == 200
    assert respuesta.context.get("horarios_disponibles", []) == [horario_elegido]


@pytest.mark.django_db
def test_inscripcion_informa_cuando_no_hay_turnos_reservables(client: Client) -> None:
    """Informa la ausencia de turnos y deshabilita su selección."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(9))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 16, 30, tzinfo=UTC),
    ):
        respuesta = client.get(
            "/inscripcion/", {"actividad": "tirolesa", "fecha": "2026-10-20"}
        )

    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert respuesta.context["horarios_disponibles"] == []
    assert "No hay turnos reservables para esta actividad y fecha." in contenido
    assert 'id="horario" name="horario" required disabled' in contenido
