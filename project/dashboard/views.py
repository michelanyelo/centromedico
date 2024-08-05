from django.shortcuts import render, redirect
from .models import HorarioAtencion, Profesional, Especialidad, Subespecialidad
from .forms import HorarioAtencionForm, ProfesionalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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
