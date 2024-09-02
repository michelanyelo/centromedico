from django import forms
from armois.models import Profesional, Especialidad


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['nombre', 'apellido', 'especialidad',
                  'subespecialidad', 'descripcion', 'telefono', 'correo']


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
