"""Prueba la integración HTTP del catálogo y sus enlaces de inscripción."""

import pytest
from django.test import Client

from core.models import Actividad


@pytest.mark.django_db
def test_catalogo_muestra_actividades_sin_crear_registros(client: Client) -> None:
    respuesta = client.get("/")
    contenido = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert "Jardinería" in contenido
    assert contenido.count('href="/inscripcion/" class="button button-dark">Inscribirme') == 4
    assert "Consultar edad" not in contenido
    assert 'id="id_edad"' not in contenido
    assert Actividad.objects.count() == 0


@pytest.mark.django_db
def test_catalogo_no_acepta_envios_de_formulario(client: Client) -> None:
    respuesta = client.post("/")
    assert respuesta.status_code == 405


@pytest.mark.django_db
def test_catalogo_muestra_capacidad_configurada(client: Client) -> None:
    Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
    respuesta = client.get("/")
    assert "8 personas por turno" in respuesta.content.decode()
