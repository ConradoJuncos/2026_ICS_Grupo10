"""Define la validación de edad para participar en una actividad."""


class EdadNoPermitidaError(ValueError):
    """Indica que la edad del visitante no permite realizar la actividad."""


def validar_edad_para_actividad(actividad: str, edad: int) -> None:
    """Valida que la edad del visitante permita realizar la actividad."""
    raise EdadNoPermitidaError("La edad del visitante no permite realizar la actividad.")
