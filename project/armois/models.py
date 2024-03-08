from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Puedes agregar campos adicionales si es necesario
    pass


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Subespecialidad(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.CASCADE, related_name="subespecialidades"
    )

    def __str__(self):
        return self.nombre
    


class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre
