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
def test_no_se_puede_reservar_si_no_hay_cupo() -> None:
    """Rechaza la inscripción cuando el horario ya no tiene lugares."""
    palestra = Actividad.objects.create(nombre="PALESTRA", cupo_maximo=1)
    horario = Horario.objects.create(
        actividad=palestra, fecha=date(2024, 10, 10), hora=time(12)
    )
    Inscripcion.objects.create(horario=horario, nombre_participante="Ana")

    with pytest.raises(ValueError):
        horario.registrar_inscripcion("Juan")


@pytest.mark.django_db
def test_registrar_inscripcion_guarda_participante(horario_tirolesa: Horario) -> None:
    """Persiste la inscripción con el nombre del participante."""
    horario_tirolesa.registrar_inscripcion("Juan")

    assert horario_tirolesa.inscripciones.count() == 1
    assert horario_tirolesa.inscripciones.get().nombre_participante == "Juan"
