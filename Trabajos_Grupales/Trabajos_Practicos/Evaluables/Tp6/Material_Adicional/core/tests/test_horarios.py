"""Verifica la existencia de la tabla de horarios."""

import pytest
from django.db import connection


@pytest.mark.django_db
def test_tabla_horarios_existe() -> None:
    """La base de datos incluye la tabla destinada a los horarios."""
    assert "core_horario" in connection.introspection.table_names()
