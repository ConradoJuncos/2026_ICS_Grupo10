"""Catálogo público y consulta de edad para las actividades del parque."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.forms import ConsultaEdadForm
from core.models import Actividad
from core.validacion_edad import (
    EDADES_MINIMAS_POR_ACTIVIDAD,
    EdadNoPermitidaError,
    validar_edad_para_actividad,
)

DESCRIPCIONES = {
    "SAFARI": ("Un encuentro salvaje.", "Recorré el parque y descubrí su fauna de cerca.", "safari"),
    "TIROLESA": ("El bosque, desde arriba.", "Cambiá de perspectiva entre las copas de los árboles.", "tirolesa"),
    "PALESTRA": ("Un poco más alto.", "Encontrá tu camino hacia la cima, una presa a la vez.", "palestra"),
    "JARDINERIA": ("Manos a la tierra.", "Acercate al mundo de las plantas y a sus pequeños habitantes.", "jardineria"),
}


@require_http_methods(["GET", "POST"])
def catalogo(request: HttpRequest) -> HttpResponse:
    """Presenta actividades y reutiliza la validación de edad del dominio."""
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
    formulario = ConsultaEdadForm(request.POST if request.method == "POST" else None)
    resultado = ""
    puede_participar = False
    if request.method == "POST" and formulario.is_valid():
        actividad = formulario.cleaned_data["actividad"]
        try:
            validar_edad_para_actividad(actividad, formulario.cleaned_data["edad"])
        except EdadNoPermitidaError:
            resultado = (
                f"{nombres[actividad]} es para mayores de "
                f"{EDADES_MINIMAS_POR_ACTIVIDAD[actividad]} años (inclusive)."
            )
        else:
            puede_participar = True
            resultado = "Tenés la edad para participar."
    return render(
        request,
        "core/catalogo.html",
        {
            "actividades": actividades,
            "formulario": formulario,
            "resultado": resultado,
            "puede_participar": puede_participar,
            "es_consulta": request.method == "POST",
        },
    )
