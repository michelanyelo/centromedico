from django.http import JsonResponse
from django.shortcuts import render
from .models import Especialidad, Subespecialidad, Profesional


# Create your views here.
def index(request):
    return render(request, "armois/layout.html")


# specialty tab
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


def reservas(request):
    profesionales = Profesional.objects.all()
    especialidades = Especialidad.objects.all()
    return render(
        request,
        "armois/reservas.html",
        {"especialidades": especialidades, "profesionales": profesionales},
    )


def obtener_subespecialidades(request):
    especialidad_id = request.GET.get(
        "especialidad_id"
    )
    subespecialidades = Subespecialidad.objects.filter(
        especialidad_id=especialidad_id
    ).values()
    return JsonResponse(list(subespecialidades), safe=False)


def agendar_cita(request):
    if request.method == "POST":
        # Aquí procesa el formulario de agendamiento y guarda la cita en la base de datos
        # Podrías utilizar el modelo de cita y los datos enviados en el formulario para crear una nueva cita
        # Luego, redirige a una página de confirmación o muestra un mensaje de éxito
        pass
    else:
        return render(request, "armois/reservas.html", {})
