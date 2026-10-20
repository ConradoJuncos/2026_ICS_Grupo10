"""Comprueba el registro de inscripciones a las actividades."""

from collections.abc import Iterator
from dataclasses import replace
from datetime import date, datetime, time
from unittest.mock import patch

import pytest
from django.utils import timezone

from core.inscripciones import (
    DatosParticipante,
    DniInvalidoError,
    InscripcionSinParticipantesError,
    TalleObligatorioError,
    registrar_inscripcion,
)
from core.models import Actividad, Horario
from core.validacion_edad import EdadNoPermitidaError

PARTICIPANTE_VALIDO = DatosParticipante(
    nombre="Ana Pérez", dni="30111222", edad=35, talle="M"
)


@pytest.fixture(autouse=True)
def reloj_controlado() -> Iterator[None]:
    """Fija el reloj una hora antes del turno de las pruebas."""
    with patch(
        "django.utils.timezone.now",
        return_value=datetime(2026, 10, 20, 9, tzinfo=timezone.get_current_timezone()),
    ):
        yield


@pytest.fixture
def horario_tirolesa() -> Horario:
    """Crea un turno reservable de Tirolesa."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    return Horario.objects.create(
        actividad=tirolesa, fecha=date(2026, 10, 20), hora=time(10)
    )


@pytest.mark.django_db
def test_registra_inscripcion_con_todos_sus_participantes(
    horario_tirolesa: Horario,
) -> None:
    """Guarda el correo y los datos de cada participante."""
    participantes = [
        DatosParticipante(nombre="Ana Pérez", dni="30111222", edad=35, talle="M"),
        DatosParticipante(nombre="Juan Pérez", dni="50111222", edad=10, talle="S"),
    ]

    inscripcion = registrar_inscripcion(
        horario_tirolesa, correo="ana@ejemplo.com", participantes=participantes
    )

    inscripcion.refresh_from_db()
    assert inscripcion.horario == horario_tirolesa
    assert inscripcion.correo == "ana@ejemplo.com"
    assert list(
        inscripcion.participantes.order_by("dni").values_list(
            "nombre", "dni", "edad", "talle"
        )
    ) == [
        ("Ana Pérez", "30111222", 35, "M"),
        ("Juan Pérez", "50111222", 10, "S"),
    ]


@pytest.mark.django_db
def test_rechaza_inscripcion_sin_participantes(horario_tirolesa: Horario) -> None:
    """Exige al menos un participante para inscribirse."""
    with pytest.raises(InscripcionSinParticipantesError):
        registrar_inscripcion(
            horario_tirolesa, correo="ana@ejemplo.com", participantes=[]
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "dni",
    [
        pytest.param("", id="vacio"),
        pytest.param("123456", id="seis_digitos"),
        pytest.param("123456789", id="nueve_digitos"),
        pytest.param("30.111.222", id="con_puntos"),
        pytest.param("3011122A", id="con_letras"),
    ],
)
def test_rechaza_participante_con_dni_invalido(
    horario_tirolesa: Horario, dni: str
) -> None:
    """Exige un DNI de 7 u 8 dígitos sin separadores."""
    participante = replace(PARTICIPANTE_VALIDO, dni=dni)

    with pytest.raises(DniInvalidoError):
        registrar_inscripcion(
            horario_tirolesa, correo="ana@ejemplo.com", participantes=[participante]
        )


@pytest.mark.django_db
def test_rechaza_inscripcion_con_un_participante_menor_a_la_edad_minima(
    horario_tirolesa: Horario,
) -> None:
    """Rechaza el grupo si un integrante no alcanza la edad mínima de Tirolesa."""
    menor = replace(PARTICIPANTE_VALIDO, nombre="Juan Pérez", dni="50111222", edad=7)

    with pytest.raises(EdadNoPermitidaError):
        registrar_inscripcion(
            horario_tirolesa,
            correo="ana@ejemplo.com",
            participantes=[PARTICIPANTE_VALIDO, menor],
        )


@pytest.mark.django_db
@pytest.mark.parametrize("actividad", ["TIROLESA", "PALESTRA"])
def test_rechaza_participante_sin_talle_en_actividad_que_lo_requiere(
    actividad: str,
) -> None:
    """Exige el talle de vestimenta en Tirolesa y Palestra."""
    horario = Horario.objects.create(
        actividad=Actividad.objects.create(nombre=actividad, cupo_maximo=10),
        fecha=date(2026, 10, 20),
        hora=time(10),
    )
    participante = replace(PARTICIPANTE_VALIDO, talle="")

    with pytest.raises(TalleObligatorioError):
        registrar_inscripcion(
            horario, correo="ana@ejemplo.com", participantes=[participante]
        )
