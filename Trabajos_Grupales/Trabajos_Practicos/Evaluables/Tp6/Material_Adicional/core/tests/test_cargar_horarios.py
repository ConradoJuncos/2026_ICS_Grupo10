"""Verifica la carga repetible de horarios de muestra."""

from datetime import date, time
from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command

from core.models import Horario


@pytest.mark.django_db
def test_cargar_horarios_respeta_dias_feriados_y_turnos_de_apertura() -> None:
    """Carga turnos en siete días abiertos sin duplicarlos al repetir."""
    fecha_base = date(2026, 12, 23)
    dias_esperados = [
        date(2026, 12, 24),
        date(2026, 12, 26),
        date(2026, 12, 27),
        date(2026, 12, 29),
        date(2026, 12, 30),
        date(2026, 12, 31),
        date(2027, 1, 2),
    ]
    with patch(
        "core.management.commands.cargar_horarios.timezone.localdate",
        return_value=fecha_base,
    ):
        call_command("cargar_horarios", stdout=StringIO())
        cantidad_inicial = Horario.objects.count()
        call_command("cargar_horarios", stdout=StringIO())

    horarios = Horario.objects.all()
    assert cantidad_inicial == 7 * 9 * 4
    assert horarios.count() == cantidad_inicial
    assert set(horarios.values_list("fecha", flat=True)) == set(dias_esperados)
    assert set(horarios.values_list("hora", flat=True)) == {
        time(hour=hora) for hora in range(9, 18)
    }
