"""Define la validación de edad para participar en una actividad."""

EDAD_MINIMA_TIROLESA = 8
EDAD_MINIMA_PALESTRA = 12
EDAD_MINIMA_VALIDA = 0


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
    if actividad == "TIROLESA" and edad < EDAD_MINIMA_TIROLESA:
        raise EdadNoPermitidaError(
            "La edad del visitante no permite realizar la actividad."
        )
    if actividad == "PALESTRA" and edad < EDAD_MINIMA_PALESTRA:
        raise EdadNoPermitidaError(
            "La edad del visitante no permite realizar la actividad."
        )
