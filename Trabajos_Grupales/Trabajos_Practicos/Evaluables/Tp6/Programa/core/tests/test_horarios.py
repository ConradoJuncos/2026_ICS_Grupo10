"""Verifica la existencia de la tabla de horarios."""

import pytest
from django.db import connection


@pytest.mark.django_db
def test_tabla_horarios_existe() -> None:
    """La base de datos incluye la tabla destinada a los horarios."""
    assert "core_horario" in connection.introspection.table_names()


@pytest.mark.django_db
def test_tabla_horarios_tiene_fecha_hora_y_actividad_asociada() -> None:
    """Cada horario guarda fecha, hora y una referencia a su actividad."""
    with connection.cursor() as cursor:
        columnas = {
            columna.name
            for columna in connection.introspection.get_table_description(
                cursor, "core_horario"
            )
        }
        restricciones = connection.introspection.get_constraints(cursor, "core_horario")

    assert {"fecha", "hora", "actividad_id"} <= columnas
    assert any(
        restriccion.get("foreign_key") == ("core_actividad", "id")
        for restriccion in restricciones.values()
    )
