"""Comprueba el control de cupos de los horarios."""

from datetime import date, time

import pytest

from core.models import Actividad, Horario, Inscripcion


@pytest.fixture
def horario_tirolesa() -> Horario:
    """Crea un horario de Tirolesa con diez cupos."""
    tirolesa = Actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
    return Horario.objects.create(
        actividad=tirolesa, fecha=date(2024, 10, 10), hora=time(10)
    )


@pytest.mark.django_db
def test_horario_nuevo_tiene_disponibilidad_total(horario_tirolesa: Horario) -> None:
    """Un horario sin inscripciones ofrece el cupo máximo de la actividad."""
    assert horario_tirolesa.cupos_disponibles() == 10


@pytest.mark.django_db
def test_reserva_reduce_disponibilidad(horario_tirolesa: Horario) -> None:
    """Cada inscripción ocupa un lugar del horario."""
    Inscripcion.objects.create(horario=horario_tirolesa).participantes.create(
        nombre="Ana Pérez", dni="30111222", edad=35, talle="M"
    )

    assert horario_tirolesa.cupos_disponibles() == 9


@pytest.mark.django_db
def test_cada_participante_ocupa_un_lugar(horario_tirolesa: Horario) -> None:
    """Una inscripción grupal ocupa un lugar por integrante."""
    inscripcion = Inscripcion.objects.create(horario=horario_tirolesa)
    inscripcion.participantes.create(
        nombre="Ana Pérez", dni="30111222", edad=35, talle="M"
    )
    inscripcion.participantes.create(
        nombre="Beto Gómez", dni="31222333", edad=40, talle="L"
    )
    inscripcion.participantes.create(
        nombre="Carla Díaz", dni="32333444", edad=28, talle="S"
    )

    assert horario_tirolesa.cupos_disponibles() == 7
