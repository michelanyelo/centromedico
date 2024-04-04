from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("especialidades", views.especialidad, name="especialidades"),
    path(
        "detalle_especialidad/<str:especialidad_id>",
        views.detalle_especialidad,
        name="detalle_especialidad",
    ),
    path("reservas/especialidades", views.get_especialidad, name="get_especialidad"),
    path(
        "reservas/subespecialidades/<int:especialidad_id>",
        views.get_subesp,
        name="get_subesp",
    ),
    path(
        "reservas/profesionales/<int:subespecialidad_id>",
        views.get_prof_subesp,
        name="get_prof_subesp",
    ),
    path(
        "reservas/profesionales-sin-subesp/<int:especialidad_id>",
        views.get_prof_sin_subesp,
        name="get_prof_sin_subesp",
    ),
    path("reservas/", views.reservas, name="reservas"),
]
