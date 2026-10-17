"""Define la validación de edad para participar en una actividad."""

EDAD_MINIMA_TIROLESA = 8
EDAD_MINIMA_PALESTRA = 12


class EdadNoPermitidaError(ValueError):
    """Indica que la edad del visitante no permite realizar la actividad."""


class EdadInvalidaError(ValueError):
    """Indica que la edad ingresada no es un dato válido."""


def validar_edad_para_actividad(actividad: str, edad: int) -> None:
    """Valida que la edad del visitante permita realizar la actividad."""
    if actividad == "TIROLESA" and edad < EDAD_MINIMA_TIROLESA:
        raise EdadNoPermitidaError(
            "La edad del visitante no permite realizar la actividad."
        )
    if actividad == "PALESTRA" and edad < EDAD_MINIMA_PALESTRA:
        raise EdadNoPermitidaError(
            "La edad del visitante no permite realizar la actividad."
        )
