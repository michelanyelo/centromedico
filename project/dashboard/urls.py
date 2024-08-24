from django.urls import path
from . import views

urlpatterns = [
    path('', views.crud_reservas, name='dashboard'),
    path('listar-reservas/', views.listar_reservas, name='listar_reservas'),
    path('agregar-horario/', views.add_horario, name='agregar_horario'),
    path('agregar-profesional/', views.add_profesional, name='agregar_profesional'),
    path('agregar-especialidad/', views.add_especialidad, name='agregar_especialidad'),
    path('listar-especialidad/', views.get_especialidad, name='listar_especialidad'),
]
