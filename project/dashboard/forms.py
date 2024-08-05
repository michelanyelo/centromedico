from django import forms
from armois.models import HorarioAtencion, Profesional


class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ['profesional', 'fecha', 'hora_inicio', 'hora_fin']


class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['nombre', 'apellido', 'especialidad',
                  'subespecialidad', 'descripcion', 'telefono', 'correo']
