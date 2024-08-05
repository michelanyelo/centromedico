from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('agregar-horario/', views.add_horario, name='agregar_horario'),
    path('agregar-medico/', views.add_medico, name='agregar_medico'),
    path('listar-reservas/', views.listar_reservas, name='listar_reservas'),
]
