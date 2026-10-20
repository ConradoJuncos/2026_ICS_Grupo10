"""Comprueba el registro de inscripciones a las actividades."""

from collections.abc import Iterator
from dataclasses import replace
from datetime import date, datetime, time
from unittest.mock import patch

import pytest
from django.utils import timezone

from core.inscripciones import (
    CupoInsuficienteError,
    DatosParticipante,
    DniInvalidoError,
    HorarioNoReservableError,
    InscripcionSinParticipantesError,
    TalleInvalidoError,
    TalleObligatorioError,
    TerminosNoAceptadosError,
    registrar_inscripcion,
)
from core.models import Actividad, Horario, Inscripcion, Participante
from core.validacion_edad import EdadNoPermitidaError

PARTICIPANTE_VALIDO = DatosParticipante(
    nombre="Ana Pérez", dni="30111222", edad=35, talle="M"
)
GRUPO_DE_TRES = [
    PARTICIPANTE_VALIDO,
    replace(PARTICIPANTE_VALIDO, nombre="Beto Gómez", dni="31222333"),
    replace(PARTICIPANTE_VALIDO, nombre="Carla Díaz", dni="32333444"),
]


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
        horario_tirolesa,
        correo="ana@ejemplo.com",
        acepta_terminos=True,
        participantes=participantes,
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
            horario_tirolesa,
            correo="ana@ejemplo.com",
            acepta_terminos=True,
            participantes=[],
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
            horario_tirolesa,
            correo="ana@ejemplo.com",
            acepta_terminos=True,
            participantes=[participante],
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
            acepta_terminos=True,
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
            horario,
            correo="ana@ejemplo.com",
            acepta_terminos=True,
            participantes=[participante],
        )


@pytest.mark.django_db
@pytest.mark.parametrize("actividad", ["SAFARI", "JARDINERIA"])
def test_admite_participante_sin_talle_en_actividad_que_no_lo_requiere(
    actividad: str,
) -> None:
    """Permite omitir el talle en Safari y Jardinería."""
    horario = Horario.objects.create(
        actividad=Actividad.objects.create(nombre=actividad, cupo_maximo=10),
        fecha=date(2026, 10, 20),
        hora=time(10),
    )
    participante = replace(PARTICIPANTE_VALIDO, talle="")

    inscripcion = registrar_inscripcion(
        horario,
        correo="ana@ejemplo.com",
        acepta_terminos=True,
        participantes=[participante],
    )

    assert inscripcion.participantes.get().talle == ""


@pytest.mark.django_db
@pytest.mark.parametrize("talle", ["XXS", "XXXL", "m", "40"])
def test_rechaza_participante_con_talle_inexistente(
    horario_tirolesa: Horario, talle: str
) -> None:
    """Acepta solamente los talles XS, S, M, L, XL y XXL."""
    participante = replace(PARTICIPANTE_VALIDO, talle=talle)

    with pytest.raises(TalleInvalidoError):
        registrar_inscripcion(
            horario_tirolesa,
            correo="ana@ejemplo.com",
            acepta_terminos=True,
            participantes=[participante],
        )


@pytest.mark.django_db
def test_rechaza_inscripcion_sin_aceptar_terminos(horario_tirolesa: Horario) -> None:
    """Exige aceptar los términos y condiciones de la actividad."""
    with pytest.raises(TerminosNoAceptadosError):
        registrar_inscripcion(
            horario_tirolesa,
            correo="ana@ejemplo.com",
            participantes=[PARTICIPANTE_VALIDO],
            acepta_terminos=False,
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("fecha", "hora"),
    [
        pytest.param(date(2026, 10, 20), time(9), id="turno_cerrado"),
        pytest.param(date(2026, 10, 21), time(11), id="mas_de_24_horas"),
        pytest.param(date(2026, 10, 20), time(18), id="fuera_del_horario_del_parque"),
    ],
)
def test_rechaza_inscripcion_en_horario_no_reservable(fecha: date, hora: time) -> None:
    """Rechaza turnos cerrados, lejanos o fuera del horario del parque."""
    horario = Horario.objects.create(
        actividad=Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10),
        fecha=fecha,
        hora=hora,
    )

    with pytest.raises(HorarioNoReservableError):
        registrar_inscripcion(
            horario,
            correo="ana@ejemplo.com",
            participantes=[PARTICIPANTE_VALIDO],
            acepta_terminos=True,
        )


@pytest.mark.django_db
def test_inscripcion_rechazada_no_guarda_datos(horario_tirolesa: Horario) -> None:
    """Un participante inválido impide guardar a todo el grupo."""
    sin_talle = replace(PARTICIPANTE_VALIDO, dni="50111222", talle="")

    with pytest.raises(TalleObligatorioError):
        registrar_inscripcion(
            horario_tirolesa,
            correo="ana@ejemplo.com",
            participantes=[PARTICIPANTE_VALIDO, sin_talle],
            acepta_terminos=True,
        )

    assert not Inscripcion.objects.exists()
    assert not Participante.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("cupo_maximo", "participantes"),
    [
        pytest.param(1, [PARTICIPANTE_VALIDO], id="turno_lleno"),
        pytest.param(3, GRUPO_DE_TRES, id="grupo_mayor_al_cupo_restante"),
    ],
)
def test_rechaza_inscripcion_sin_cupo_suficiente(
    cupo_maximo: int, participantes: list[DatosParticipante]
) -> None:
    """Rechaza el grupo si no quedan lugares para todos sus integrantes."""
    horario = Horario.objects.create(
        actividad=Actividad.objects.create(nombre="TIROLESA", cupo_maximo=cupo_maximo),
        fecha=date(2026, 10, 20),
        hora=time(10),
    )
    Inscripcion.objects.create(horario=horario).participantes.create(
        nombre="Dora Ruiz", dni="40111222", edad=30, talle="M"
    )

    with pytest.raises(CupoInsuficienteError):
        registrar_inscripcion(
            horario,
            correo="ana@ejemplo.com",
            participantes=participantes,
            acepta_terminos=True,
        )
