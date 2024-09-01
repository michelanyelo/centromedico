from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Especialidad, Subespecialidad, Profesional, HorarioAtencion, Paciente, Reserva
from googlecalendar import google_calendar_class as gc
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "armois/index.html")


def get_especialidad(request):
    especialidades = list(Especialidad.objects.values())
    data = {"message": "Success", "especialidad": especialidades} if especialidades else {
        "message": "Not found esp"}
    return JsonResponse(data)


def get_subesp(request, especialidad_id):
    sub_esp = list(Subespecialidad.objects.filter(
        especialidad_id=especialidad_id).values())
    data = {"message": "Success", "subespecialidad": sub_esp} if sub_esp else {
        "message": "Not found subesp"}
    return JsonResponse(data)


def get_prof_con_subesp(request, subespecialidad_id):
    profesional_subesp = list(Profesional.objects.filter(
        subespecialidad_id=subespecialidad_id).values())
    data = {"message": "Success", "profesional_subesp": profesional_subesp} if profesional_subesp else {
        "message": "Not found profesional con subesp"}
    return JsonResponse(data)


def get_prof_sin_subesp(request, especialidad_id):
    profesionales_sin_subesp = Profesional.objects.filter(
        subespecialidad__isnull=True, especialidad_id=especialidad_id)
    data = {"message": "Success", "profesionales_sin_subesp": list(profesionales_sin_subesp.values(
    ))} if profesionales_sin_subesp.exists() else {"message": "Not found profesional sin subesp"}
    return JsonResponse(data)


def get_horarios_disponibles(request, profesional_id):
    horarios = HorarioAtencion.objects.filter(
        profesional_id=profesional_id, is_available=True).values()
    data = {"message": "Success", "horarios": list(horarios)} if horarios else {
        "message": "No hay horarios disponibles"}
    return JsonResponse(data)


def reservas(request):
    if request.method == 'POST':
        id_profesional = request.POST.get('cboProfesional')
        id_horario = request.POST.get('id_horario_atencion')
        profesional = Profesional.objects.get(id=id_profesional)
        dia = request.POST.get('dia')
        mes_numero = request.POST.get('mes')
        anio = request.POST.get('anio')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        meses = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio',
                 '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'}
        mes_nombre = meses.get(mes_numero, '')

        fecha_hora_inicio = f"{anio}-{mes_numero}-{dia}-T{hora_inicio}"
        fecha_hora_final = f"{anio}-{mes_numero}-{dia}-T{hora_fin}"

        return render(request, "armois/solicitar_datos_paciente.html/", {
            "id_profesional": id_profesional,
            "nombre_profesional": profesional.nombre,
            "apellido_profesional": profesional.apellido,
            "dia": dia,
            "mes_numero": mes_numero,
            "mes_nombre": mes_nombre,
            "anio": anio,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "fecha_hora_inicio": fecha_hora_inicio,
            "fecha_hora_final": fecha_hora_final,
            "id_horario": id_horario
        })
    else:
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
        horario_id = request.POST.get('id_horario_atencion')

        # Obtener los datos del profesional
        profesional_id = request.POST.get('id_profesional')
        profesional = Profesional.objects.get(id=int(profesional_id))

        # Corregir el formato de la fecha y hora de inicio
        fecha_hora_inicio_str = request.POST.get('fecha_hora_inicio')
        fecha_hora_inicio_str = corregir_formato_fecha(fecha_hora_inicio_str)
        fecha_hora_inicio = datetime.strptime(fecha_hora_inicio_str, '%Y-%m-%dT%H:%M:%S')
        hora_inicio = fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M:%S')

        # Corregir el formato de la fecha y hora de finalización
        fecha_hora_final_str = request.POST.get('fecha_hora_final')
        fecha_hora_final_str = corregir_formato_fecha(fecha_hora_final_str)
        fecha_hora_final = datetime.strptime(fecha_hora_final_str, '%Y-%m-%dT%H:%M:%S')
        hora_final = fecha_hora_final.strftime('%Y-%m-%dT%H:%M:%S')

        # Verificación rápida de las fechas
        print(f"Inicio: {fecha_hora_inicio}, Fin: {fecha_hora_final}")

        # Lógica para agregar el evento al calendario con los datos del paciente y profesional
        especialidad_profesional = profesional.especialidad
        subespecialidad_profesional = profesional.subespecialidad
        correo_profesional = profesional.correo
        
        summary = (f"{profesional.nombre} {profesional.apellido} "
                   f"({subespecialidad_profesional}) \nAtención a: {nombre_paciente}"
                   if subespecialidad_profesional
                   else f"{profesional.nombre} {profesional.apellido}\n{especialidad_profesional} \nAtención a: {nombre_paciente}")

        timezone = "America/Santiago"
        attendees = [correo_profesional, correo_paciente]

        # Crear una instancia de GoogleCalendarManager y llamar a create_event
        calendar_manager = gc.GoogleCalendarManager()
        calendar_manager.create_event(summary, fecha_hora_inicio.isoformat(), fecha_hora_final.isoformat(), timezone, attendees)

        # Crear y guardar el nuevo paciente y la reserva
        nuevo_paciente = Paciente(
            nombre=nombre_paciente,
            correo=correo_paciente,
            sexo=sexo_paciente,
            direccion=direccion_paciente,
            telefono=telefono_paciente
        )
        nuevo_paciente.save()

        horario_atencion = HorarioAtencion.objects.get(id=int(horario_id))
        nueva_reserva = Reserva(
            horario=horario_atencion,
            paciente=nuevo_paciente,
            especialidad=especialidad_profesional,
            subespecialidad=subespecialidad_profesional,
            profesional=profesional,
            is_synced_with_google_calendar=True
        )
        nueva_reserva.save()

        # Marcar el horario como no disponible
        horario_atencion.is_available = False
        horario_atencion.save()

        # Redirigir a una página de éxito o renderizar una plantilla de éxito
        request.session['show_alert'] = True
        return redirect('reservas')

    else:
        return render(request, "armois/solicitar_datos_paciente.html/")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, "armois/login_profesional.html", {
                "message": "Usuario y/o contraseña incorrectos."
            })
    else:
        return render(request, "armois/login_profesional.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def profile_view(request):
    return render(request, 'dashboard/profile_profesional.html', {'user': request.user})


def corregir_formato_fecha(fecha_str):
    # Eliminar el nombre del día de la semana
    partes = fecha_str.split(',')
    if len(partes) == 2:
        fecha_str = partes[1].strip()

    # Reemplazar el guión entre la fecha y la hora
    fecha_str = fecha_str.replace('-T', 'T')
    return fecha_str
