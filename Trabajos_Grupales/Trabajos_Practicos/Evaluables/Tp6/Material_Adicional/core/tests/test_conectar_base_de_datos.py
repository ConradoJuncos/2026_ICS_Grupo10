"""Comprueba la conexión con la base de datos."""

import pytest
from django.db import connection


@pytest.mark.django_db
def test_base_de_datos_actividades() -> None:
    """La aplicación puede abrir una conexión utilizable con la base."""
    connection.ensure_connection()

    assert connection.is_usable()
