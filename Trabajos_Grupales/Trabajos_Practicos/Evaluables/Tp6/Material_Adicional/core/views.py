"""Catálogo público de actividades del parque."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import Actividad
from core.validacion_edad import EDADES_MINIMAS_POR_ACTIVIDAD

DESCRIPCIONES = {
    "SAFARI": ("Un encuentro salvaje.", "Recorré el parque y descubrí su fauna de cerca.", "safari"),
    "TIROLESA": ("El bosque, desde arriba.", "Cambiá de perspectiva entre las copas de los árboles.", "tirolesa"),
    "PALESTRA": ("Un poco más alto.", "Encontrá tu camino hacia la cima, una presa a la vez.", "palestra"),
    "JARDINERIA": ("Manos a la tierra.", "Acercate al mundo de las plantas y a sus pequeños habitantes.", "jardineria"),
}


@require_GET
def catalogo(request: HttpRequest) -> HttpResponse:
    """Presenta las actividades disponibles y sus enlaces de inscripción."""
    capacidades = dict(Actividad.objects.values_list("nombre", "cupo_maximo"))
    nombres = dict(Actividad.OPCIONES_ACTIVIDAD)
    actividades = [
        {
            "codigo": codigo,
            "nombre": nombres[codigo],
            "titulo": contenido[0],
            "descripcion": contenido[1],
            "ilustracion": contenido[2],
            "edad_minima": EDADES_MINIMAS_POR_ACTIVIDAD[codigo],
            "cupo": capacidades.get(codigo),
            "requiere_talle": codigo in {"TIROLESA", "PALESTRA"},
        }
        for codigo, contenido in DESCRIPCIONES.items()
    ]
    return render(
        request,
        "core/catalogo.html",
        {
            "actividades": actividades,
        },
    )
