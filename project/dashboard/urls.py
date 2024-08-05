from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/agregar-horario/', views.add_horario, name='agregar_horario'),
    path('dashboard/agregar-medico/', views.add_medico, name='agregar_medico'),
]
