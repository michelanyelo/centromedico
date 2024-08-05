from django.shortcuts import render, redirect
from .models import HorarioAtencion, Profesional, Especialidad, Subespecialidad
from .forms import HorarioAtencionForm, ProfesionalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from googlecalendar import google_calendar_class as gc
from datetime import datetime, timedelta, timezone


def dashboard_view(request):
    horarios = HorarioAtencion.objects.all()
    profesionales = Profesional.objects.all()
    return render(request, 'dashboard/dashboard.html', {'horarios': horarios, 'profesionales': profesionales})


@login_required
def add_horario(request):
    if request.method == 'POST':
        form = HorarioAtencionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')
    else:
        form = HorarioAtencionForm()
    return render(request, 'dashboard/add_horario.html', {'form': form})


@login_required
def add_medico(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')
    else:
        form = ProfesionalForm()
    return render(request, 'dashboard/add_medico.html', {'form': form})


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
