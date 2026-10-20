"""Registra inscripciones de visitantes a los horarios de las actividades."""

from dataclasses import dataclass

from core.models import Horario, Inscripcion


class InscripcionSinParticipantesError(ValueError):
    """Indica que la inscripción no incluye participantes."""


@dataclass(frozen=True)
class DatosParticipante:
    """Datos que el visitante informa por cada participante."""

    nombre: str
    dni: str
    edad: int
    talle: str = ""


def registrar_inscripcion(
    horario: Horario,
    correo: str,
    participantes: list[DatosParticipante],
) -> Inscripcion:
    """Valida y guarda la inscripción de los participantes en el horario."""
    inscripcion = Inscripcion.objects.create(horario=horario, correo=correo)
    for participante in participantes:
        inscripcion.participantes.create(
            nombre=participante.nombre,
            dni=participante.dni,
            edad=participante.edad,
            talle=participante.talle,
        )
    return inscripcion
