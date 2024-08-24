from django.http import JsonResponse
from django.shortcuts import render, redirect
from armois.models import HorarioAtencion, Profesional, Especialidad, Subespecialidad, Reserva
from .forms import ProfesionalForm, EspecialidadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from googlecalendar import google_calendar_class as gc
from datetime import datetime, timedelta, timezone


@login_required
def add_horario(request):
    if request.method == 'POST':
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        profesional = Profesional.objects.get(id=profesional_id)
        horario = HorarioAtencion(
            profesional=profesional,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        horario.save()
        return redirect('agregar_horario')  # Redirige a una URL de éxito
    else:
        return render(request, 'dashboard/nuevo_horario.html', {'profesionales': Profesional.objects.all()})


@login_required
def add_profesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_profesional')
    else:
        form = ProfesionalForm()
    return render(request, 'dashboard/nuevo_profesional.html', {'form': form})


@login_required
def add_especialidad(request):
    if request.method == 'POST':
        specialty_name = request.POST.get('specialty_name')
        specialty_description = request.POST.get('specialty_description')
        sub_name = request.POST.get('sub_name')
        specialty_id = request.POST.get('specialty')

        if specialty_name:
            # Capitalizar el nombre de la especialidad
            specialty_name = specialty_name.title()
            specialty = Especialidad.objects.create(
                nombre=specialty_name, descripcion=specialty_description)
            return JsonResponse({'status': 'success', 'message': 'Especialidad creada con éxito.'})

        elif specialty_id and sub_name:
            # Capitalizar el nombre de la subespecialidad y concatenar con el nombre de la especialidad
            sub_name = sub_name.title()
            try:
                specialty = Especialidad.objects.get(id=specialty_id)
                full_sub_name = f"{specialty.nombre} {sub_name}"
                Subespecialidad.objects.create(
                    nombre=full_sub_name, especialidad=specialty)
                return JsonResponse({'status': 'success', 'message': 'Subespecialidad creada con éxito.'})
            except Especialidad.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Especialidad no encontrada.'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Datos insuficientes para crear especialidad o subespecialidad.'})

    return render(request, 'dashboard/nueva_especialidad.html')


def get_especialidad(request):
    specialties = Especialidad.objects.all().values('id', 'nombre', 'descripcion')
    return JsonResponse(list(specialties), safe=False)


@login_required
def listar_reservas(request):
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

    return render(request, 'dashboard/listar_reservas.html', {'events': events})

@login_required
def crud_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'dashboard/dashboard.html', {'reservas': reservas})
