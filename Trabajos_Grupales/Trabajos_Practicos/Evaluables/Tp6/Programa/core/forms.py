"""Formularios públicos para consultar las reglas de las actividades."""

from django import forms

from core.models import Actividad


class ConsultaEdadForm(forms.Form):
    """Interpreta la actividad y la edad sin registrar una inscripción."""

    actividad = forms.ChoiceField(
        choices=Actividad.OPCIONES_ACTIVIDAD,
        error_messages={
            "required": "Elegí una actividad válida.",
            "invalid_choice": "Elegí una actividad válida.",
        },
    )
    edad = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "Ingresá una edad en años enteros.",
            "invalid": "Ingresá una edad en años enteros.",
            "min_value": "Ingresá una edad en años enteros.",
        },
    )
