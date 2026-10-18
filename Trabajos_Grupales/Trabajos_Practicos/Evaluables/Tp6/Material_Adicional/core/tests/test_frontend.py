"""Prueba la integración HTTP del catálogo y sus enlaces de inscripción."""

from pathlib import Path

import pytest
from django.test import Client


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


def test_formulario_inscripcion_no_acepta_envios(client: Client) -> None:
    respuesta = client.post("/inscripcion/")
    assert respuesta.status_code == 405


def test_inscripcion_ya_no_tiene_ruta_por_actividad(client: Client) -> None:
    respuesta = client.get("/inscripcion/safari/")
    assert respuesta.status_code == 404
