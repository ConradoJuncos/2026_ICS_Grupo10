"""Comprueba las fechas reservables que recibe el formulario de inscripción."""

import re
from datetime import date, datetime, time
from unittest.mock import patch

import pytest
from django.test import Client
from django.utils import timezone

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
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
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
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
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
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get(
            "/inscripcion/", {"actividad": "tirolesa", "fecha": "2026-10-20"}
        )

    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert respuesta.context["horarios_disponibles"] == []
    assert "No hay turnos reservables para esta actividad y fecha." in contenido
    assert 'id="horario" name="horario" required disabled' in contenido


@pytest.mark.django_db
def test_calendario_limita_la_seleccion_a_fechas_reservables(client: Client) -> None:
    """El campo de fecha usa los límites de los turnos reservables de la BD."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17))
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9))
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 22), hora=time(9))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get("/inscripcion/?actividad=tirolesa")

    campo_fecha = re.search(
        r'<input\b[^>]*\bid="fecha-visita"[^>]*>', respuesta.content.decode()
    )
    assert respuesta.status_code == 200
    assert campo_fecha is not None
    assert 'min="2026-10-20"' in campo_fecha.group()
    assert 'max="2026-10-21"' in campo_fecha.group()


@pytest.mark.django_db
def test_formulario_muestra_turnos_reales_y_conserva_fecha(client: Client) -> None:
    """El selector ofrece el turno persistido y conserva la fecha consultada."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    safari = Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
    horario_elegido = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9)
    )
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17))
    Horario.objects.create(actividad=safari, fecha=date(2026, 10, 21), hora=time(10))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get(
            "/inscripcion/", {"actividad": "tirolesa", "fecha": "2026-10-21"}
        )

    contenido = respuesta.content.decode()
    selector = re.search(
        r'<select\b(?P<atributos>[^>]*\bid="horario"[^>]*)>'
        r"(?P<opciones>.*?)</select>",
        contenido,
        flags=re.DOTALL,
    )
    campo_fecha = re.search(r'<input\b[^>]*\bid="fecha-visita"[^>]*>', contenido)
    assert respuesta.status_code == 200
    assert selector is not None
    assert re.findall(r'<option\b[^>]*\bvalue="([^"]+)"', selector["opciones"]) == [
        str(horario_elegido.pk)
    ]
    assert "09:00" in selector["opciones"]
    assert "disabled" not in selector["atributos"]
    assert campo_fecha is not None
    assert 'value="2026-10-21"' in campo_fecha.group()


@pytest.mark.django_db
def test_formulario_permite_consultar_turnos_por_get(client: Client) -> None:
    """Permite consultar turnos sin completar ni enviar la inscripción."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    Horario.objects.create(actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17))

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get("/inscripcion/?actividad=tirolesa")

    contenido = respuesta.content.decode()
    formulario = re.search(r'<form\b[^>]*\bid="consulta-turnos"[^>]*>', contenido)
    selector_actividad = re.search(r'<select\b[^>]*\bid="actividad"[^>]*>', contenido)
    campo_fecha = re.search(r'<input\b[^>]*\bid="fecha-visita"[^>]*>', contenido)
    campo_correo = re.search(r'<input\b[^>]*\bname="correo"[^>]*>', contenido)
    boton_consulta = re.search(
        r'<button\b[^>]*\bform="consulta-turnos"[^>]*>', contenido
    )
    opcion_actividad = re.search(r'<option\b[^>]*\bvalue="tirolesa"[^>]*>', contenido)
    seccion_actividad = re.search(
        r'<div\b[^>]*\bid="activity-form-content"[^>]*>', contenido
    )
    assert respuesta.status_code == 200
    assert formulario is not None
    assert 'method="get"' in formulario.group()
    assert 'action="/inscripcion/"' in formulario.group()
    assert selector_actividad is not None
    assert 'form="consulta-turnos"' in selector_actividad.group()
    assert campo_fecha is not None
    assert 'form="consulta-turnos"' in campo_fecha.group()
    assert campo_correo is not None
    assert 'form="consulta-turnos"' not in campo_correo.group()
    assert boton_consulta is not None
    assert 'type="submit"' in boton_consulta.group()
    assert opcion_actividad is not None
    assert "selected" in opcion_actividad.group()
    assert seccion_actividad is not None
    assert "hidden" not in seccion_actividad.group()
