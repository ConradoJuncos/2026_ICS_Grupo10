"""Comprueba las fechas reservables que recibe el formulario de inscripción."""

import re
from datetime import date, datetime, time
from unittest.mock import patch

import pytest
from django.test import Client
from django.utils import timezone

from core.models import Actividad, Horario, Inscripcion


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
    assert 'name="horario"' not in contenido


@pytest.mark.django_db
def test_formulario_ofrece_solo_fechas_reservables(client: Client) -> None:
    """Presenta como opciones las fechas que tienen turnos reservables."""
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

    contenido = respuesta.content.decode()
    fechas = re.findall(r'<input\b[^>]*\bname="fecha" value="([^"]+)"', contenido)
    assert respuesta.status_code == 200
    assert fechas == ["2026-10-20", "2026-10-21"]
    assert '<span class="choice-title">Hoy</span>' in contenido
    assert '<span class="choice-title">Mañana</span>' in contenido


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
    turnos = re.findall(
        r'<label class="choice-chip time-chip">\s*<input\b[^>]*\bname="horario" '
        r'value="([^"]+)"[^>]*>(.*?)</label>',
        contenido,
        flags=re.DOTALL,
    )
    campo_fecha = re.search(
        r'<input\b[^>]*\bname="fecha" value="2026-10-21"[^>]*>', contenido
    )
    assert respuesta.status_code == 200
    assert [valor for valor, _ in turnos] == [str(horario_elegido.pk)]
    assert "09:00" in turnos[0][1]
    assert campo_fecha is not None
    assert "checked" in campo_fecha.group()


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
    campo_fecha = re.search(r'<input\b[^>]*\bname="fecha"[^>]*>', contenido)
    campo_correo = re.search(r'<input\b[^>]*\bname="correo"[^>]*>', contenido)
    boton_consulta = re.search(
        r'<button\b[^>]*\bform="consulta-turnos"[^>]*>', contenido
    )
    opcion_actividad = re.search(
        r'<input\b[^>]*\bname="actividad" value="tirolesa"[^>]*>', contenido
    )
    seccion_actividad = re.search(
        r'<div\b[^>]*\bid="activity-form-content"[^>]*>', contenido
    )
    assert respuesta.status_code == 200
    assert formulario is not None
    assert 'method="get"' in formulario.group()
    assert 'action="/inscripcion/"' in formulario.group()
    assert campo_fecha is not None
    assert 'form="consulta-turnos"' in campo_fecha.group()
    assert campo_correo is not None
    assert 'form="consulta-turnos"' not in campo_correo.group()
    assert boton_consulta is not None
    assert 'type="submit"' in boton_consulta.group()
    assert opcion_actividad is not None
    assert 'type="radio"' in opcion_actividad.group()
    assert 'form="consulta-turnos"' in opcion_actividad.group()
    assert "checked" in opcion_actividad.group()
    assert seccion_actividad is not None
    assert "hidden" not in seccion_actividad.group()


@pytest.mark.django_db
def test_selector_muestra_cupos_restantes_del_turno(client: Client) -> None:
    """Cada opción de horario informa los lugares que quedan en ese turno."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    horario = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 21), hora=time(9)
    )
    Inscripcion.objects.create(horario=horario).participantes.create(
        nombre="Ana Pérez", dni="30111222", edad=35, talle="M"
    )
    Inscripcion.objects.create(horario=horario).participantes.create(
        nombre="Beto Gómez", dni="31222333", edad=40, talle="L"
    )
    Inscripcion.objects.create(horario=horario).participantes.create(
        nombre="Carla Díaz", dni="32333444", edad=28, talle="S"
    )

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(
            2026, 10, 20, 16, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get(
            "/inscripcion/", {"actividad": "tirolesa", "fecha": "2026-10-21"}
        )

    opcion = re.search(
        rf'<input\b[^>]*\bvalue="{horario.pk}"[^>]*>(?P<texto>.*?)</label>',
        respuesta.content.decode(),
        flags=re.DOTALL,
    )
    assert opcion is not None
    assert "7 lugares" in opcion["texto"]


@pytest.mark.django_db
def test_formulario_preselecciona_la_unica_fecha_reservable(client: Client) -> None:
    """Muestra los turnos sin pedir que se elija la única fecha posible."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    horario = Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(17)
    )

    with patch(
        "django.utils.timezone.now",
        return_value=datetime(
            2026, 10, 20, 9, 30, tzinfo=timezone.get_current_timezone()
        ),
    ):
        respuesta = client.get("/inscripcion/?actividad=tirolesa")

    assert respuesta.context["horarios_disponibles"] == [horario]
    assert (
        'name="fecha" value="2026-10-20" form="consulta-turnos" required checked>'
        in (respuesta.content.decode())
    )
