"""Valida la edad de los visitantes según la actividad elegida."""

EDAD_MINIMA_PALESTRA = 12
EDAD_MINIMA_TIROLESA = 8
EDAD_MINIMA_VALIDA = 0

EDADES_MINIMAS_POR_ACTIVIDAD = {
    "TIROLESA": EDAD_MINIMA_TIROLESA,
    "PALESTRA": EDAD_MINIMA_PALESTRA,
    "SAFARI": EDAD_MINIMA_VALIDA,
    "JARDINERIA": EDAD_MINIMA_VALIDA,
}


class ActividadDesconocidaError(ValueError):
    """Indica que la actividad no pertenece al catálogo del parque."""


class EdadNoPermitidaError(ValueError):
    """Indica que la edad del visitante no permite realizar la actividad."""


class EdadInvalidaError(ValueError):
    """Indica que la edad ingresada no es un dato válido."""


def validar_edad_para_actividad(actividad: str, edad: object) -> None:
    """Valida que la edad del visitante permita realizar la actividad."""
    if edad is None:
        raise EdadInvalidaError("Debe ingresar la edad del visitante.")
    if isinstance(edad, bool) or not isinstance(edad, int):
        raise EdadInvalidaError("La edad debe ser un número entero.")
    if edad < EDAD_MINIMA_VALIDA:
        raise EdadInvalidaError("La edad no puede ser negativa.")

    codigo_actividad = actividad.upper()
    if codigo_actividad not in EDADES_MINIMAS_POR_ACTIVIDAD:
        raise ActividadDesconocidaError("La actividad elegida no existe.")
    if edad < EDADES_MINIMAS_POR_ACTIVIDAD[codigo_actividad]:
        raise EdadNoPermitidaError(
            "La edad del visitante no permite realizar la actividad."
        )
