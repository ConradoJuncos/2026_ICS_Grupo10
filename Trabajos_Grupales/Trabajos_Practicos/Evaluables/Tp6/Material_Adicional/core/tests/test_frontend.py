"""Prueba la integración HTTP del catálogo y la validación existente."""

import pytest
from django.test import Client

from core.models import Actividad


@pytest.mark.django_db
def test_catalogo_muestra_actividades_sin_crear_registros(client: Client) -> None:
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "Jardinería" in respuesta.content.decode()
    assert Actividad.objects.count() == 0


@pytest.mark.django_db
def test_catalogo_muestra_capacidad_configurada(client: Client) -> None:
    Actividad.objects.create(nombre="SAFARI", cupo_maximo=8)
    respuesta = client.get("/")
    assert "8 personas por turno" in respuesta.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("actividad", "edad", "mensaje"),
    [
        ("TIROLESA", "7", "Tirolesa es para mayores de 8 años"),
        ("TIROLESA", "8", "Tenés la edad para participar"),
        ("PALESTRA", "11", "Palestra es para mayores de 12 años"),
        ("SAFARI", "0", "Tenés la edad para participar"),
        ("OTRA", "20", "Elegí una actividad válida"),
        ("SAFARI", "8.5", "Ingresá una edad en años enteros"),
        ("SAFARI", "-1", "Ingresá una edad en años enteros"),
    ],
)
def test_consulta_edad(
    client: Client, actividad: str, edad: str, mensaje: str
) -> None:
    respuesta = client.post("/", {"actividad": actividad, "edad": edad})
    assert respuesta.status_code == 200
    assert mensaje in respuesta.content.decode()
    assert Actividad.objects.count() == 0
