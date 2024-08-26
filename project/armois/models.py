from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUser(AbstractUser):
    is_secretaria = models.BooleanField(default=False)

    def __str__(self):
        return self.username


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
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    subespecialidad = models.ForeignKey(
        Subespecialidad, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        if self.subespecialidad:
            return f"{self.nombre} especializado en {self.especialidad} y {self.subespecialidad}"
        else:
            return f"{self.nombre} especializado en {self.especialidad}"


class Paciente(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    sexo = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class HorarioAtencion(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profesional.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"

    def clean(self):
        # Validar que la hora de inicio sea anterior a la hora de finalización
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError(
                "La hora de inicio debe ser anterior a la hora de finalización.")


class Reserva(models.Model):
    horario = models.ForeignKey(HorarioAtencion, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    subespecialidad = models.ForeignKey(Subespecialidad, on_delete=models.CASCADE, null=True, blank=True)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    is_synced_with_google_calendar = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reserva de {self.paciente.nombre} con {self.horario.profesional.nombre} el {self.horario.fecha} desde las {self.horario.hora_inicio} hasta las {self.horario.hora_fin}"
