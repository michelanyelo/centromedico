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
]
