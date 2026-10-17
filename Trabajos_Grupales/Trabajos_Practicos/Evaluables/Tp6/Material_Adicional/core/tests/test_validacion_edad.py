"""Comprueba las restricciones de edad de las actividades."""

import pytest

from core.validacion_edad import (
    EdadInvalidaError,
    EdadNoPermitidaError,
    validar_edad_para_actividad,
)


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


def test_admite_palestra_para_visitante_de_12_anios() -> None:
    """Admite la participación en Palestra desde los 12 años."""
    actividad = "PALESTRA"
    edad = 12

    resultado = validar_edad_para_actividad(actividad, edad)

    assert resultado is None


@pytest.mark.parametrize("actividad", ["SAFARI", "JARDINERIA"])
def test_admite_actividades_sin_edad_minima(actividad: str) -> None:
    """Admite visitantes de 0 años en Safari y Jardinería."""
    edad = 0

    resultado = validar_edad_para_actividad(actividad, edad)

    assert resultado is None


@pytest.mark.parametrize("actividad", ["TIROLESA", "PALESTRA", "SAFARI", "JARDINERIA"])
def test_rechaza_edad_negativa(actividad: str) -> None:
    """Rechaza edades negativas como datos inválidos en cualquier actividad."""
    edad = -1

    with pytest.raises(EdadInvalidaError):
        validar_edad_para_actividad(actividad, edad)


@pytest.mark.parametrize("actividad", ["TIROLESA", "PALESTRA", "SAFARI", "JARDINERIA"])
def test_rechaza_edad_ausente(actividad: str) -> None:
    """Exige ingresar la edad del visitante en cualquier actividad."""
    edad = None

    with pytest.raises(EdadInvalidaError):
        validar_edad_para_actividad(actividad, edad)


@pytest.mark.parametrize("actividad", ["TIROLESA", "PALESTRA", "SAFARI", "JARDINERIA"])
@pytest.mark.parametrize("edad", ["ocho", "8", "", 8.5, 8.0])
def test_rechaza_edad_con_formato_invalido(actividad: str, edad: str | float) -> None:
    """Exige una edad entera, sin convertir textos ni redondear decimales."""
    with pytest.raises(EdadInvalidaError):
        validar_edad_para_actividad(actividad, edad)
