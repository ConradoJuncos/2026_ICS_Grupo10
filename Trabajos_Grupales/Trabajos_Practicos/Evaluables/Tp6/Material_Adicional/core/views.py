"""Catálogo público de actividades del parque."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import Actividad
from core.validacion_edad import EDADES_MINIMAS_POR_ACTIVIDAD

CUPO_MAXIMO_POR_ACTIVIDAD = {
    "SAFARI": 8,
    "TIROLESA": 10,
    "PALESTRA": 12,
    "JARDINERIA": 12,
}

DESCRIPCIONES = {
    "SAFARI": ("Un encuentro salvaje.", "Recorré el parque y descubrí su fauna de cerca.", "safari"),
    "TIROLESA": ("El bosque, desde arriba.", "Cambiá de perspectiva entre las copas de los árboles.", "tirolesa"),
    "PALESTRA": ("Un poco más alto.", "Encontrá tu camino hacia la cima, una presa a la vez.", "palestra"),
    "JARDINERIA": ("Manos a la tierra.", "Acercate al mundo de las plantas y a sus pequeños habitantes.", "jardineria"),
}

TERMINOS_POR_ACTIVIDAD = {
    "SAFARI": "La actividad se realiza siguiendo las indicaciones del equipo del parque. "
    "Mantené una distancia segura de los animales y permanecé con tu grupo durante todo el recorrido.",
    "TIROLESA": "La actividad requiere el uso del equipo de seguridad provisto por el parque. "
    "Seguí las indicaciones del personal y utilizá la talla de vestimenta declarada.",
    "PALESTRA": "La actividad se realiza con el equipo de seguridad provisto por el parque. "
    "Respetá las indicaciones del personal y utilizá la talla de vestimenta declarada.",
    "JARDINERIA": "La actividad se realiza en espacios al aire libre y con materiales provistos por el parque. "
    "Seguí las indicaciones del equipo y cuidá las plantas y herramientas durante la experiencia.",
}


@require_GET
def catalogo(request: HttpRequest) -> HttpResponse:
    """Presenta las actividades disponibles y sus enlaces de inscripción."""
    nombres = dict(Actividad.OPCIONES_ACTIVIDAD)
    actividades = [
        {
            "codigo": codigo,
            "nombre": nombres[codigo],
            "titulo": contenido[0],
            "descripcion": contenido[1],
            "ilustracion": contenido[2],
            "edad_minima": EDADES_MINIMAS_POR_ACTIVIDAD[codigo],
            "cupo": CUPO_MAXIMO_POR_ACTIVIDAD[codigo],
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


@require_GET
def inscripcion(request: HttpRequest) -> HttpResponse:
    """Renderiza el formulario visual común para todas las actividades."""
    nombres = dict(Actividad.OPCIONES_ACTIVIDAD)
    cupos = dict(Actividad.objects.values_list("nombre", "cupo_maximo"))
    actividades = [
        {
            "codigo": codigo.lower(),
            "nombre": nombres[codigo],
            "descripcion": contenido[0],
            "cupo": cupos.get(codigo, CUPO_MAXIMO_POR_ACTIVIDAD[codigo]),
            "edad_minima": EDADES_MINIMAS_POR_ACTIVIDAD[codigo],
            "requiere_talle": codigo in {"TIROLESA", "PALESTRA"},
            "terminos": TERMINOS_POR_ACTIVIDAD[codigo],
        }
        for codigo, contenido in DESCRIPCIONES.items()
    ]
    return render(
        request,
        "core/inscripcion.html",
        {
            "actividades": actividades,
            "participantes": range(1, max(CUPO_MAXIMO_POR_ACTIVIDAD.values()) + 1),
        },
    )
