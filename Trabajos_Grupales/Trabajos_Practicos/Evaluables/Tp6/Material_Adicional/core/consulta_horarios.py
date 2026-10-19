"""Consulta los horarios persistidos de las actividades."""

from datetime import date

from core.models import Actividad, Horario


def consultar_horarios_por_actividad(
    actividad: Actividad, fecha: date | None = None
) -> list[Horario]:
    """Devuelve los horarios asociados a la actividad seleccionada."""
    return list(Horario.objects.filter(actividad=actividad))
