from django.urls import path
from . import views

urlpatterns = [
    path('', views.crud_reservas, name='dashboard'),
    path('listar-reservas/', views.listar_reservas, name='listar_reservas'),
    path('listar-profesionales/', views.listar_profesionales, name='listar_profesionales'),
    path('listar-horarios/<int:profesional_id>/', views.listar_horarios, name='listar_horarios'),
    path('agregar-horario/', views.add_horario, name='agregar_horario'),
    path('agregar-profesional/', views.add_profesional, name='agregar_profesional'),
    path('agregar-especialidad/', views.add_especialidad, name='agregar_especialidad'),
    path('listar-especialidad/<int:profesional_id>/', views.listar_especialidad, name='listar_especialidad'),
    path('listar-subespecialidades/<int:especialidad_id>/', views.listar_subespecialidades, name='listar_subespecialidades'),
    path('editar-reserva/', views.editar_reserva, name='editar_reserva'),
    path('eliminar-reserva/', views.eliminar_reserva, name='eliminar_reserva'),

]
