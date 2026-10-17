"""Comprueba las restricciones de edad de las actividades."""

import pytest

from core.validacion_edad import EdadNoPermitidaError, validar_edad_para_actividad


def test_rechaza_tirolesa_para_visitante_de_7_anios() -> None:
    """Rechaza la participación en Tirolesa de un visitante de 7 años."""
    actividad = "TIROLESA"
    edad = 7

    with pytest.raises(EdadNoPermitidaError):
        validar_edad_para_actividad(actividad, edad)


def test_admite_tirolesa_para_visitante_de_8_anios() -> None:
    """Admite la participación en Tirolesa desde los 8 años."""
    actividad = "TIROLESA"
    edad = 8

    resultado = validar_edad_para_actividad(actividad, edad)

    assert resultado is None


def test_rechaza_palestra_para_visitante_de_11_anios() -> None:
    """Rechaza la participación en Palestra antes de los 12 años."""
    actividad = "PALESTRA"
    edad = 11

    with pytest.raises(EdadNoPermitidaError):
        validar_edad_para_actividad(actividad, edad)
