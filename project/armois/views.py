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


def get_especialidad(request):
    especialidad = list(Especialidad.objects.values())
    if len(especialidad) > 0:
        data = {"message": "Success", "especialidad": especialidad}
    else:
        data = {"message": "Not found esp"}

    return JsonResponse(data)


def get_subesp(request, especialidad_id):
    sub_esp = list(
        Subespecialidad.objects.filter(especialidad_id=especialidad_id).values()
    )
    if len(sub_esp) > 0:
        data = {"message": "Success", "subespecialidad": sub_esp}
    else:
        data = {"message": "Not found subesp"}

    return JsonResponse(data)


def get_prof_subesp(request, subespecialidad_id):
    profesional_subesp = list(
        Profesional.objects.filter(subespecialidad_id=subespecialidad_id).values()
    )

    if len(profesional_subesp) > 0:
        data = {"message": "Success", "profesional_subesp": profesional_subesp}
    else:
        data = {"message": "Not found profesional con subesp"}

    return JsonResponse(data)


def get_prof_sin_subesp(request, especialidad_id):
    profesionales_sin_subesp = Profesional.objects.filter(
        subespecialidad__isnull=True, especialidad_id=especialidad_id
    )

    if profesionales_sin_subesp.exists():
        data = {
            "message": "Success",
            "profesionales_sin_subesp": list(profesionales_sin_subesp.values()),
        }
    else:
        data = {"message": "Not found profesional sin subesp"}

    return JsonResponse(data)


def reservas(request):
    return render(request, "armois/reservas.html")


def agendar_cita(request):
    if request.method == "POST":
        # Aquí procesa el formulario de agendamiento y guarda la cita en la base de datos
        # Podrías utilizar el modelo de cita y los datos enviados en el formulario para crear una nueva cita
        # Luego, redirige a una página de confirmación o muestra un mensaje de éxito
        pass
    else:
        return render(request, "armois/reservas.html", {})
