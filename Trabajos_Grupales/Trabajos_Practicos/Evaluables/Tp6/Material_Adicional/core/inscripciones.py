"""Registra inscripciones de visitantes a los horarios de las actividades."""

import re
from dataclasses import dataclass

from core.consulta_horarios import consultar_horarios_por_actividad
from core.models import Horario, Inscripcion
from core.validacion_edad import validar_edad_para_actividad

FORMATO_DNI = re.compile(r"\d{7,8}")
ACTIVIDADES_CON_TALLE = {"TIROLESA", "PALESTRA"}
TALLES_DISPONIBLES = {"XS", "S", "M", "L", "XL", "XXL"}


class InscripcionSinParticipantesError(ValueError):
    """Indica que la inscripción no incluye participantes."""


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


def registrar_inscripcion(
    horario: Horario,
    correo: str,
    participantes: list[DatosParticipante],
    acepta_terminos: bool,
) -> Inscripcion:
    """Valida y guarda la inscripción de los participantes en el horario."""
    if horario not in consultar_horarios_por_actividad(
        horario.actividad, horario.fecha
    ):
        raise HorarioNoReservableError("El horario elegido ya no admite inscripciones.")
    if not acepta_terminos:
        raise TerminosNoAceptadosError("Aceptá los términos de la actividad.")
    if not participantes:
        raise InscripcionSinParticipantesError("Agregá al menos un participante.")
    for participante in participantes:
        _validar_participante(horario.actividad.nombre, participante)
    inscripcion = Inscripcion.objects.create(horario=horario, correo=correo)
    for participante in participantes:
        inscripcion.participantes.create(
            nombre=participante.nombre,
            dni=participante.dni,
            edad=participante.edad,
            talle=participante.talle,
        )
    return inscripcion
