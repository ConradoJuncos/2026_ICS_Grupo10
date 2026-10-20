"""Prueba la integración HTTP del catálogo y sus enlaces de inscripción."""

from collections.abc import Iterator
from datetime import date, datetime, time
from pathlib import Path
from unittest.mock import patch

import pytest
from django.test import Client
from django.utils import timezone

from core.models import Actividad, Horario, Inscripcion


@pytest.fixture
def reloj_controlado() -> Iterator[None]:
    """Fija el reloj una hora antes del turno de las pruebas."""
    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 9, tzinfo=timezone.get_current_timezone()),
    ):
        yield


@pytest.fixture
def horario_tirolesa(reloj_controlado: None) -> Horario:
    """Crea un turno reservable de Tirolesa."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    return Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(10)
    )


def datos_de_inscripcion(horario: Horario) -> dict[str, str]:
    """Arma los campos que envía el formulario para un grupo de dos personas."""
    return {
        "horario": str(horario.pk),
        "cantidad_personas": "2",
        "participante_1_nombre": "Ana Pérez",
        "participante_1_dni": "30111222",
        "participante_1_edad": "35",
        "participante_1_talle": "M",
        "participante_2_nombre": "Juan Pérez",
        "participante_2_dni": "50111222",
        "participante_2_edad": "10",
        "participante_2_talle": "S",
        "correo": "ana@ejemplo.com",
        "acepta_terminos": "on",
    }


def test_catalogo_muestra_actividades_con_enlaces_de_inscripcion(
    client: Client,
) -> None:
    respuesta = client.get("/")
    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert "Jardinería" in contenido
    assert contenido.count('class="button button-dark">Inscribirme') == 4
    assert 'href="/inscripcion/?actividad=safari"' in contenido
    assert 'href="/inscripcion/?actividad=jardineria"' in contenido
    assert "Consultar edad" not in contenido
    assert 'id="id_edad"' not in contenido


def test_catalogo_no_acepta_envios_de_formulario(client: Client) -> None:
    respuesta = client.post("/")
    assert respuesta.status_code == 405


def test_catalogo_muestra_capacidad_por_actividad(client: Client) -> None:
    respuesta = client.get("/")
    contenido = respuesta.content.decode()
    assert "8 personas por turno" in contenido
    assert "10 personas por turno" in contenido
    assert contenido.count("12 personas por turno") == 2


@pytest.mark.django_db
def test_formulario_muestra_fecha_horarios_y_precios(client: Client) -> None:
    respuesta = client.get("/inscripcion/?actividad=safari")
    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert 'id="fecha-visita" name="fecha" type="date" required' in contenido
    assert "No se admiten reservas con más de 24 horas de anticipación" in contenido
    assert "Los turnos se habilitan hasta 15 minutos antes" in contenido
    assert "Entrada común" in contenido
    assert "$10.000" in contenido
    assert "Entrada VIP" in contenido
    assert "$20.000" in contenido
    assert "50% de descuento" in contenido
    javascript = Path("core/static/core/inscripcion.js").read_text(encoding="utf-8")
    assert "Solo se puede reservar dentro de las 24 horas previas" in javascript


@pytest.mark.django_db
@pytest.mark.parametrize(
    "codigo",
    [
        "safari",
        "tirolesa",
        "palestra",
        "jardineria",
    ],
)
def test_una_pagina_de_inscripcion_preselecciona_actividad_por_query(
    client: Client, codigo: str
) -> None:
    respuesta = client.get(f"/inscripcion/?actividad={codigo}")
    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert contenido.count("<legend>Participante ") == 12
    assert f'value="{codigo}"' in contenido
    assert 'id="actividad"' in contenido
    capacidades = {"safari": 8, "tirolesa": 10, "palestra": 12, "jardineria": 12}
    assert f'data-capacity="{capacidades[codigo]}"' in contenido
    assert 'name="horario" required' in contenido
    assert 'value="17:00">' not in contenido
    assert 'type="date"' in contenido
    assert 'name="cantidad_personas"' in contenido
    assert 'name="participante_1_talle"' in contenido
    assert "inscripcion.js" in contenido
    assert "Condiciones preliminares" in contenido
    assert "código QR" in contenido
    assert "inscripcion.js" in contenido


def test_formulario_inscripcion_rechaza_metodos_no_admitidos(client: Client) -> None:
    respuesta = client.put("/inscripcion/")
    assert respuesta.status_code == 405


def test_inscripcion_ya_no_tiene_ruta_por_actividad(client: Client) -> None:
    respuesta = client.get("/inscripcion/safari/")
    assert respuesta.status_code == 404


@pytest.mark.django_db
def test_formulario_registra_la_inscripcion_enviada(
    client: Client, horario_tirolesa: Horario
) -> None:
    """Guarda la inscripción del grupo y muestra la confirmación."""
    respuesta = client.post(
        "/inscripcion/?actividad=tirolesa&fecha=2026-10-20",
        datos_de_inscripcion(horario_tirolesa),
    )

    assert respuesta.status_code == 200
    assert "Inscripción confirmada" in respuesta.content.decode()
    inscripcion = Inscripcion.objects.get()
    assert inscripcion.horario == horario_tirolesa
    assert inscripcion.correo == "ana@ejemplo.com"
    assert list(
        inscripcion.participantes.order_by("dni").values_list(
            "nombre", "dni", "edad", "talle"
        )
    ) == [
        ("Ana Pérez", "30111222", 35, "M"),
        ("Juan Pérez", "50111222", 10, "S"),
    ]


@pytest.mark.django_db
def test_formulario_muestra_el_error_de_una_inscripcion_rechazada(
    client: Client, horario_tirolesa: Horario
) -> None:
    """Vuelve al formulario con el motivo del rechazo y no guarda nada."""
    datos = datos_de_inscripcion(horario_tirolesa) | {"participante_2_dni": "123"}

    respuesta = client.post("/inscripcion/?actividad=tirolesa&fecha=2026-10-20", datos)

    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert 'id="registration-form"' in contenido
    assert "El DNI debe tener 7 u 8 dígitos, sin puntos." in contenido
    assert not Inscripcion.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "edad",
    [
        pytest.param("", id="vacia"),
        pytest.param("diez", id="en_letras"),
    ],
)
def test_formulario_rechaza_una_edad_no_numerica(
    client: Client, horario_tirolesa: Horario, edad: str
) -> None:
    """Informa que la edad debe ser un número en lugar de fallar."""
    datos = datos_de_inscripcion(horario_tirolesa) | {"participante_1_edad": edad}

    respuesta = client.post("/inscripcion/?actividad=tirolesa&fecha=2026-10-20", datos)

    assert "La edad debe ser un número entero." in respuesta.content.decode()
    assert not Inscripcion.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "cantidad",
    [
        pytest.param("", id="vacia"),
        pytest.param("dos", id="en_letras"),
    ],
)
def test_formulario_rechaza_una_cantidad_de_participantes_no_numerica(
    client: Client, horario_tirolesa: Horario, cantidad: str
) -> None:
    """Pide indicar la cantidad de participantes en lugar de fallar."""
    datos = datos_de_inscripcion(horario_tirolesa) | {"cantidad_personas": cantidad}

    respuesta = client.post("/inscripcion/?actividad=tirolesa&fecha=2026-10-20", datos)

    assert "Indicá la cantidad de participantes." in respuesta.content.decode()
    assert not Inscripcion.objects.exists()
