"""Consulta los horarios persistidos de las actividades."""

from datetime import date

from core.models import Actividad, Horario


def consultar_horarios_por_actividad(
    actividad: Actividad, fecha: date | None = None
) -> list[Horario]:
    """Devuelve los horarios asociados a la actividad seleccionada."""
    horarios = Horario.objects.filter(actividad=actividad)
    if fecha is not None:
        horarios = horarios.filter(fecha=fecha)
    return [horario for horario in horarios if horario.admite_inscripciones()]
