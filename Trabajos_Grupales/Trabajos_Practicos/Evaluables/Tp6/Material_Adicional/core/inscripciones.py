"""Define las reglas de los datos de una inscripción a una actividad."""

import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from core.validacion_edad import validar_edad_para_actividad

FORMATO_DNI = re.compile(r"\d{7,8}")
ACTIVIDADES_CON_TALLE = {"TIROLESA", "PALESTRA"}
TALLES_DISPONIBLES = {"XS", "S", "M", "L", "XL", "XXL"}


class InscripcionSinParticipantesError(ValueError):
    """Indica que la inscripción no incluye participantes."""


class CorreoInvalidoError(ValueError):
    """Indica que el correo de contacto no tiene un formato válido."""


class NombreObligatorioError(ValueError):
    """Indica que falta el nombre de un participante."""


class DniInvalidoError(ValueError):
    """Indica que el DNI de un participante no tiene un formato válido."""


class TalleObligatorioError(ValueError):
    """Indica que falta el talle de vestimenta que exige la actividad."""


class TalleInvalidoError(ValueError):
    """Indica que el talle informado no pertenece a los talles disponibles."""


class TerminosNoAceptadosError(ValueError):
    """Indica que el visitante no aceptó los términos de la actividad."""


class HorarioNoReservableError(ValueError):
    """Indica que el horario elegido no admite inscripciones."""


class CupoInsuficienteError(ValueError):
    """Indica que el horario no tiene lugares para todos los participantes."""


class DniRepetidoError(ValueError):
    """Indica que una misma persona figura dos veces en la inscripción."""


class InscripcionSimultaneaError(ValueError):
    """Indica que un participante ya está inscripto en otro turno a la misma hora."""


@dataclass(frozen=True)
class DatosParticipante:
    """Datos que el visitante informa por cada participante."""

    nombre: str
    dni: str
    edad: int
    talle: str = ""


def _validar_participante(actividad: str, participante: DatosParticipante) -> None:
    """Rechaza los datos del participante que no cumplen las reglas de la actividad."""
    if not FORMATO_DNI.fullmatch(participante.dni):
        raise DniInvalidoError("El DNI debe tener 7 u 8 dígitos, sin puntos.")
    validar_edad_para_actividad(actividad, participante.edad)
    if actividad in ACTIVIDADES_CON_TALLE and not participante.talle:
        raise TalleObligatorioError("Indicá el talle de cada participante.")
    if participante.talle and participante.talle not in TALLES_DISPONIBLES:
        raise TalleInvalidoError("Elegí un talle entre XS y XXL.")


def validar_solicitud(
    actividad: str,
    correo: str,
    participantes: list[DatosParticipante],
    acepta_terminos: bool,
) -> None:
    """Rechaza los datos de la solicitud que no cumplen las reglas de inscripción."""
    if not acepta_terminos:
        raise TerminosNoAceptadosError("Aceptá los términos de la actividad.")
    try:
        validate_email(correo)
    except ValidationError as error:
        raise CorreoInvalidoError("Ingresá un correo electrónico válido.") from error
    if not participantes:
        raise InscripcionSinParticipantesError("Agregá al menos un participante.")
    for participante in participantes:
        _validar_participante(actividad, participante)
    dnis = [participante.dni for participante in participantes]
    if len(set(dnis)) != len(dnis):
        raise DniRepetidoError("Cada participante debe tener un DNI distinto.")
