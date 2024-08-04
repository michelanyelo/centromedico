from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Especialidad, Subespecialidad, Profesional, HorarioAtencion
from googlecalendar import google_calendar_class as gc
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from googlecalendar.google_calendar_class import GoogleCalendarManager


# Create your views here.


def index(request):
    return render(request, "armois/index.html")


def dashboard(request):
    return render(request, "armois/dashboard.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_secretaria:
                return redirect(reverse("dashboard"))
            else:
                return redirect(reverse("index"))
        else:
            return render(request, "armois/profesional_login.html", {
                "message": "Usuario y/o contraseña incorrectos."
            })
    else:
        return render(request, "armois/profesional_login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("template"))


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
        Subespecialidad.objects.filter(
            especialidad_id=especialidad_id).values()
    )
    if len(sub_esp) > 0:
        data = {"message": "Success", "subespecialidad": sub_esp}
    else:
        data = {"message": "Not found subesp"}

    return JsonResponse(data)


def get_prof_con_subesp(request, subespecialidad_id):
    profesional_subesp = list(
        Profesional.objects.filter(
            subespecialidad_id=subespecialidad_id).values()
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


def get_horarios_disponibles(request, profesional_id):
    horarios = HorarioAtencion.objects.filter(profesional_id=profesional_id)
    if horarios.exists():
        data = {
            "message": "Success",
            "horarios": list(horarios.values())
        }
    else:
        data = {"message": "No hay horarios disponibles"}
    return JsonResponse(data)


def reservas(request):
    if request.method == 'POST':
        # summary = "Psicología(Psicología Infanto Juvenil) - Camila Maulén"
        id_profesional = request.POST.get('cboProfesional')
        nombre_profesional = Profesional.objects.get(id=id_profesional).nombre
        dia = request.POST.get('dia')
        mes_numero = request.POST.get('mes')
        anio = request.POST.get('anio')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        # Mapeo de números de meses a nombres
        meses = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }

        # Transformar el número del mes en nombre
        mes_nombre = meses.get(mes_numero, '')

        fecha_hora_inicio = f"{anio}-{mes_numero}-{dia}-T{hora_inicio}"
        fecha_hora_final = f"{anio}-{mes_numero}-{dia}-T{hora_fin}"

        return render(request, "armois/solicitar_datos_paciente.html/", {
            "id_profesional": id_profesional,
            "nombre_profesional": nombre_profesional,
            "dia": dia,
            "mes_numero": mes_numero,
            "mes_nombre": mes_nombre,
            "anio": anio,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "fecha_hora_inicio": fecha_hora_inicio,
            "fecha_hora_final": fecha_hora_final
        })
    else:
        # Renderizar el formulario de selección de horario
        show_alert = request.session.pop('show_alert', False)
        return render(request, 'armois/reservas.html', {'show_alert': show_alert})


def reservas_a_calendario(request):
    if request.method == 'POST':
        # Obtener los datos del paciente
        nombre_paciente = request.POST.get('inputNombrePaciente')
        correo_paciente = request.POST.get('inputCorreoPaciente')
        sexo_paciente = request.POST.get('radioSexo')
        direccion_paciente = request.POST.get('inputDireccion')
        telefono_paciente = request.POST.get('inputTelefono')

        # Obtener los datos del profesional
        profesional_id = request.POST.get('id_profesional')
        nombre_profesional = request.POST.get('nombre_profesional')
        fecha_hora_inicio_str = request.POST.get('fecha_hora_inicio')
        fecha_hora_inicio_str = fecha_hora_inicio_str.replace('-T', 'T')
        fecha_hora_inicio = datetime.strptime(
            fecha_hora_inicio_str, '%Y-%m-%dT%H:%M:%S')
        hora_inicio = fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M:%S')

        fecha_hora_final_str = request.POST.get('fecha_hora_final')
        fecha_hora_final_str = fecha_hora_final_str.replace('-T', 'T')
        fecha_hora_final = datetime.strptime(
            fecha_hora_final_str, '%Y-%m-%dT%H:%M:%S')
        hora_final = fecha_hora_final.strftime('%Y-%m-%dT%H:%M:%S')

        # Lógica para agregar el evento al calendario con los datos del paciente y profesional
        especialidad_profesional = Profesional.objects.get(
            id=profesional_id).especialidad
        subespecialidad_profesional = Profesional.objects.get(
            id=profesional_id).subespecialidad
        correo_profesional = Profesional.objects.get(id=profesional_id).correo
        if subespecialidad_profesional is not None:
            summary = f"{nombre_profesional} ({subespecialidad_profesional}) \nAtención a: {
                nombre_paciente}"
        else:
            summary = f"{nombre_profesional} \n{
                especialidad_profesional} \nAtención a: {nombre_paciente}"
        timezone = "America/Santiago"
        attendees = [correo_profesional, correo_paciente]

        # Crear una instancia de GoogleCalendarManager y llamar a create_event

        calendar_manager = gc.GoogleCalendarManager()
        calendar_manager.create_event(str(summary),
                                      str(hora_inicio),
                                      str(hora_final),
                                      timezone,
                                      attendees)

        # Redirigir a una página de éxito o renderizar una plantilla de éxito
        request.session['show_alert'] = True
        return redirect('reservas')

    else:
        # Si no es un método POST, redirigir a la página de reserva
        return render(request, "armois/solicitar_datos_paciente.html/")


# def listar_incoming_reservas(request):
#     calendar_manager = gc.GoogleCalendarManager()
#     events = calendar_manager.list_upcoming_events()
#     return render(request, 'armois/listar_reservas.html', {'events': events})

@login_required
def listar_reservas(request):
    if request.user.is_secretaria:
        calendar_manager = gc.GoogleCalendarManager()
        start_date = datetime.now(timezone.utc) - timedelta(days=30)
        end_date = datetime.now(timezone.utc) + timedelta(days=30)
        events = calendar_manager.list_events_in_date_range(
            start_date, end_date)

        for event in events:
            if 'dateTime' in event['start']:
                event['start']['dateTime'] = datetime.strptime(
                    event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            if 'dateTime' in event['end']:
                event['end']['dateTime'] = datetime.strptime(
                    event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')

        return render(request, 'armois/listar_reservas.html', {'events': events})
    else:
        return redirect('armois/index')
