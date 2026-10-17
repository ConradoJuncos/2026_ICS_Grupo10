"""Comprueba las restricciones de edad de las actividades."""

import pytest

from core.validacion_edad import EdadNoPermitidaError, validar_edad_para_actividad


def test_rechaza_tirolesa_para_visitante_de_7_anios() -> None:
    """Rechaza la participación en Tirolesa de un visitante de 7 años."""
    actividad = "TIROLESA"
    edad = 7

    with pytest.raises(EdadNoPermitidaError):
        validar_edad_para_actividad(actividad, edad)
