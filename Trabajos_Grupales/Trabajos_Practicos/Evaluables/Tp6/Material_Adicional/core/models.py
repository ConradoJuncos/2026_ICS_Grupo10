from datetime import datetime, time, timedelta
from typing import ClassVar

from django.db import models
from django.utils import timezone

from core.inscripciones import (
    CupoInsuficienteError,
    DatosParticipante,
    HorarioNoReservableError,
    InscripcionSimultaneaError,
    validar_solicitud,
)

DIA_LUNES = 0
FERIADOS_DE_CIERRE = {(1, 1), (12, 25)}
HORAS_DE_INICIO_PERMITIDAS = {time(hora) for hora in range(9, 18)}
ANTICIPACION_MAXIMA = timedelta(hours=24)
MARGEN_CIERRE_INSCRIPCION = timedelta(minutes=15)


class Actividad(models.Model):
    """Actividad del parque con su capacidad por turno."""

    OPCIONES_ACTIVIDAD: ClassVar[list[tuple[str, str]]] = [
        ("TIROLESA", "Tirolesa"),
        ("SAFARI", "Safari"),
        ("PALESTRA", "Palestra"),
        ("JARDINERIA", "Jardinería"),
    ]

    nombre = models.CharField(max_length=50, choices=OPCIONES_ACTIVIDAD, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.get_nombre_display()


class Horario(models.Model):
    """Turno de una actividad en una fecha y hora."""

    fecha = models.DateField()
    hora = models.TimeField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    def cupos_disponibles(self) -> int:
        """Devuelve los lugares que quedan libres en el turno."""
        ocupados = Participante.objects.filter(inscripcion__horario=self).count()
        return self.actividad.cupo_maximo - ocupados

    def admite_inscripciones(self) -> bool:
        """Indica si el parque abre, el turno está en la ventana y tiene lugar."""
        ahora = timezone.now()
        inicio = timezone.make_aware(datetime.combine(self.fecha, self.hora))
        return (
            self.fecha.weekday() != DIA_LUNES
            and (self.fecha.month, self.fecha.day) not in FERIADOS_DE_CIERRE
            and self.hora in HORAS_DE_INICIO_PERMITIDAS
            and ahora + MARGEN_CIERRE_INSCRIPCION
            <= inicio
            <= ahora + ANTICIPACION_MAXIMA
            and self.cupos_disponibles() > 0
        )

    def registrar_inscripcion(
        self,
        correo: str,
        participantes: list[DatosParticipante],
        acepta_terminos: bool,
    ) -> "Inscripcion":
        """Valida y guarda la inscripción de los participantes en el horario."""
        if len(participantes) > self.cupos_disponibles():
            raise CupoInsuficienteError(
                "No quedan lugares para todos los participantes."
            )
        if not self.admite_inscripciones():
            raise HorarioNoReservableError(
                "El horario elegido ya no admite inscripciones."
            )
        validar_solicitud(self.actividad.nombre, correo, participantes, acepta_terminos)
        if Participante.objects.filter(
            dni__in=[participante.dni for participante in participantes],
            inscripcion__horario__fecha=self.fecha,
            inscripcion__horario__hora=self.hora,
        ).exists():
            raise InscripcionSimultaneaError(
                "Un participante ya está inscripto en otra actividad a esa hora."
            )
        inscripcion = self.inscripciones.create(correo=correo)
        for participante in participantes:
            inscripcion.participantes.create(
                nombre=participante.nombre,
                dni=participante.dni,
                edad=participante.edad,
                talle=participante.talle,
            )
        return inscripcion


class Inscripcion(models.Model):
    """Reserva de un grupo de participantes en un horario."""

    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, related_name="inscripciones"
    )
    correo = models.EmailField(blank=True, default="")


class Participante(models.Model):
    """Persona incluida en una inscripción."""

    inscripcion = models.ForeignKey(
        Inscripcion, on_delete=models.CASCADE, related_name="participantes"
    )
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    edad = models.PositiveSmallIntegerField()
    talle = models.CharField(max_length=3, blank=True, default="")
