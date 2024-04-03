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
    # path("reservas/detalles", views.especialidad_json, name="especialidad_json"),
    path("reservas/", views.reservas, name="reservas"),
    path(
        "reservas/obtener-subespecialidades/",
        views.obtener_subespecialidades,
        name="obtener_subespecialidades",
    ),
]
