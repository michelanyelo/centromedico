from django import forms
from .models import HorarioAtencion, Profesional


class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ['profesional', 'fecha', 'hora_inicio', 'hora_fin']


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['user', 'nombre', 'especialidad',
                  'subespecialidad', 'descripcion', 'telefono', 'correo']
