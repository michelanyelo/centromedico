from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("especialidades", views.especialidad, name="especialidades"),
    path("detalle_especialidad/<str:especialidad_id>", views.detalle_especialidad, name="detalle_especialidad"),
    path("reservas/especialidades", views.get_especialidad, name="get_especialidad"),
    path("reservas/subespecialidades/<int:especialidad_id>", views.get_subesp, name="get_subesp"),
    path("reservas/profesionales-con-subesp/<int:subespecialidad_id>", views.get_prof_con_subesp, name="get_prof_subesp"),
    path("reservas/profesionales-sin-subesp/<int:especialidad_id>", views.get_prof_sin_subesp, name="get_prof_sin_subesp"),
    path("reservas/", views.reservas, name="reservas"),
    path("reservas/horarios/<int:profesional_id>", views.get_horarios_disponibles, name="get_horarios_disponibles"),
    path("reservas/solicitar-datos-paciente/", views.reservas, name="solicitar_datos_paciente"),
    path("reservas/reservas-a-calendario/", views.reservas_a_calendario, name="reservas_a_calendario"),
]
