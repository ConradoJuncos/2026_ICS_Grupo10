"""Registra inscripciones de visitantes a los horarios de las actividades."""

import re
from dataclasses import dataclass

from core.models import Horario, Inscripcion

FORMATO_DNI = re.compile(r"\d{7,8}")


class InscripcionSinParticipantesError(ValueError):
    """Indica que la inscripción no incluye participantes."""


class DniInvalidoError(ValueError):
    """Indica que el DNI de un participante no tiene un formato válido."""


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
    if not participantes:
        raise InscripcionSinParticipantesError("Agregá al menos un participante.")
    for participante in participantes:
        if not FORMATO_DNI.fullmatch(participante.dni):
            raise DniInvalidoError("El DNI debe tener 7 u 8 dígitos, sin puntos.")
    inscripcion = Inscripcion.objects.create(horario=horario, correo=correo)
    for participante in participantes:
        inscripcion.participantes.create(
            nombre=participante.nombre,
            dni=participante.dni,
            edad=participante.edad,
            talle=participante.talle,
        )
    return inscripcion
