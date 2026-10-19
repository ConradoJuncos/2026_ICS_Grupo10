"""Consulta los horarios persistidos de las actividades."""

from datetime import date, datetime, time, timedelta

from django.utils import timezone

from core.models import Actividad, Horario

DIA_LUNES = 0
FERIADOS_DE_CIERRE = {(1, 1), (12, 25)}
HORAS_DE_INICIO_PERMITIDAS = {time(hora) for hora in range(9, 18)}
ANTICIPACION_MAXIMA = timedelta(hours=24)
MARGEN_CIERRE_INSCRIPCION = timedelta(minutes=15)


def consultar_horarios_por_actividad(
    actividad: Actividad, fecha: date | None = None
) -> list[Horario]:
    """Devuelve los horarios asociados a la actividad seleccionada."""
    horarios = Horario.objects.filter(actividad=actividad)
    if fecha is not None:
        horarios = horarios.filter(fecha=fecha)
    ahora = timezone.now()
    limite_anticipacion = ahora + ANTICIPACION_MAXIMA
    limite_cierre = ahora + MARGEN_CIERRE_INSCRIPCION
    return [
        horario
        for horario in horarios
        if horario.fecha.weekday() != DIA_LUNES
        and (horario.fecha.month, horario.fecha.day) not in FERIADOS_DE_CIERRE
        and horario.hora in HORAS_DE_INICIO_PERMITIDAS
        and limite_cierre
        <= timezone.make_aware(datetime.combine(horario.fecha, horario.hora))
        <= limite_anticipacion
    ]
