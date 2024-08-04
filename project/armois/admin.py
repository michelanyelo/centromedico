from django.contrib import admin
from .models import CustomUser, Especialidad, Subespecialidad, Profesional, HorarioAtencion
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Especialidad)
admin.site.register(Subespecialidad)
admin.site.register(Profesional)
admin.site.register(HorarioAtencion)