from django.contrib import admin
from .models import User, Especialidad, Subespecialidad, Profesional
# Register your models here.
admin.site.register(User)
admin.site.register(Especialidad)
admin.site.register(Subespecialidad)
admin.site.register(Profesional)