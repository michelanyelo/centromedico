from django.shortcuts import render
from .models import Especialidad, Subespecialidad


# Create your views here.
def index(request):
    return render(request, "armois/layout.html")


def especialidad(request):
    especialidades = Especialidad.objects.all().order_by("nombre")
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return render(
        request,
        "armois/especialidades.html",
        {"especialidades": especialidades, "letras": letras},
    )


def detalle_especialidad(request, especialidad_id):
    especialidad = Especialidad.objects.get(id=especialidad_id)
    subespecialidades = especialidad.subespecialidades.all()
    return render(
        request,
        "armois/especialidad_detalle.html",
        {"especialidad": especialidad, "subespecialidades": subespecialidades},
    )
