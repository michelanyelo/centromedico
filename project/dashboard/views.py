import json
from pyexpat.errors import messages
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
                sub_name = f"{sub_name}"
                Subespecialidad.objects.create(
                    nombre=sub_name, especialidad=specialty)
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


@login_required
def editar_reserva(request):
    try:
        data = json.loads(request.body)
        reserva_id = int(data.get('id'))
        nuevo_profesional_id = int(data.get('profesional_id'))
        nuevo_horario_id = int(data.get('horario_id'))
        nueva_especialidad_id = int(data.get('especialidad_id'))
        nueva_subespecialidad_id = int(
            data.get('subespecialidad_id'))  # Agregado

        # Validaciones previas
        if not reserva_id or not nuevo_profesional_id or not nuevo_horario_id:
            return JsonResponse({'success': False, 'error': 'Datos insuficientes para editar la reserva'})

        # Obtener la reserva existente
        reserva = Reserva.objects.get(id=reserva_id)

        # Obtener el profesional, el horario y la subespecialidad nuevos
        nuevo_profesional = Profesional.objects.get(id=nuevo_profesional_id)
        nuevo_horario = HorarioAtencion.objects.get(id=nuevo_horario_id)
        nueva_especialidad = Especialidad.objects.get(id=nueva_especialidad_id)
        nueva_subespecialidad = None
        if nueva_subespecialidad_id:
            nueva_subespecialidad = Subespecialidad.objects.get(
                id=nueva_subespecialidad_id)

        # Verificar que el nuevo horario esté disponible
        if not nuevo_horario.is_available:
            return JsonResponse({'success': False, 'error': 'El horario seleccionado no está disponible'})

        # Marcar el horario anterior como disponible si no es el mismo
        if reserva.horario != nuevo_horario:
            reserva.horario.is_available = True
            reserva.horario.save()

            # Actualizar la reserva con el nuevo profesional, horario y subespecialidad
            reserva.profesional = nuevo_profesional
            reserva.horario = nuevo_horario
            reserva.especialidad = nueva_especialidad
            if nueva_subespecialidad:
                reserva.subespecialidad = nueva_subespecialidad
            reserva.save()

            # Marcar el nuevo horario como no disponible
            nuevo_horario.is_available = False
            nuevo_horario.save()

        return JsonResponse({'success': True, 'message': 'Reserva actualizada exitosamente'})

    except Reserva.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Reserva no encontrada'})
    except Profesional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profesional no encontrado'})
    except HorarioAtencion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Horario no encontrado'})
    except Subespecialidad.DoesNotExist:  # Agregado
        # Agregado
        return JsonResponse({'success': False, 'error': 'Subespecialidad no encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Ocurrió un error inesperado: {str(e)}'})


def listar_profesionales(request):
    profesionales = Profesional.objects.all().values('id', 'nombre', 'apellido')
    return JsonResponse(list(profesionales), safe=False)


def listar_horarios(request, profesional_id):
    try:
        horarios = HorarioAtencion.objects.filter(
            profesional_id=profesional_id, is_available=True).values('id', 'hora_inicio', 'hora_fin')
        return JsonResponse(list(horarios), safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def listar_especialidad(request, profesional_id):
    try:
        profesional = Profesional.objects.get(id=profesional_id)
        especialidad = profesional.especialidad
        especialidad_data = {
            'id': especialidad.id,
            'nombre': especialidad.nombre,
        }
        return JsonResponse({'success': True, 'especialidad': especialidad_data})
    except Profesional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profesional no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def listar_subespecialidades(request, especialidad_id):
    subespecialidades = Subespecialidad.objects.filter(
        especialidad_id=especialidad_id)
    data = {
        'success': True,
        'subespecialidades': list(subespecialidades.values('id', 'nombre'))
    }
    return JsonResponse(data)


@login_required
def eliminar_reserva(request):
    try:
        data = json.loads(request.body)
        reserva_id = int(data.get('id'))

        # Obtener la reserva existente
        reserva = Reserva.objects.get(id=reserva_id)

        # Marcar el horario como disponible
        horario = reserva.horario
        horario.is_available = True
        horario.save()

        # Eliminar la reserva
        reserva.delete()

        return JsonResponse({'success': True, 'message': 'Reserva eliminada exitosamente'})

    except Reserva.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Reserva no encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Ocurrió un error inesperado: {str(e)}'})


@login_required
def eliminar_reserva_calendario(request, reserva_id):
    # Crear una instancia del administrador de Google Calendar
    calendar_manager = gc.GoogleCalendarManager()

    # Eliminar el evento de Google Calendar
    calendar_manager.delete_event(reserva_id)

    return redirect('listar_reservas')
