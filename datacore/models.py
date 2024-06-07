from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser


class Facultad(models.Model):
    id_facultad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)


class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    id_facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=False)


class EstadoPersona(models.Model):
    id_estado_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)


class User(AbstractUser):
    motivo_desautorizado = models.TextField(blank=True)
    recursos_max = models.PositiveIntegerField(default=1)
    id_estado_persona = models.ForeignKey(
        EstadoPersona, on_delete=models.CASCADE, null=False
    )
    id_especialidad = models.ForeignKey(
        Especialidad, on_delete=models.CASCADE, null=False
    )
    id_facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.username


class Herramienta(models.Model):
    id_herramienta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)


class Libreria(models.Model):
    id_libreria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    version = models.CharField(max_length=50)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, null=False)


class Recurso(models.Model):
    id_recurso = models.AutoField(primary_key=True)
    solicitudes_encoladas = models.IntegerField()
    tamano_ram = models.IntegerField()
    estado = models.BooleanField()
    ubicacion = models.TextField(blank=True)
    herramientas = models.ManyToManyField(Herramienta, blank=True)


class CPU(models.Model):
    id_recurso = models.OneToOneField(
        Recurso, on_delete=models.CASCADE, primary_key=True
    )
    nombre = models.CharField(max_length=200)
    numero_nucleos_cpu = models.IntegerField()
    frecuencia_cpu = models.DecimalField(decimal_places=6, max_digits=15)


class GPU(models.Model):
    id_recurso = models.OneToOneField(
        Recurso, on_delete=models.CASCADE, primary_key=True
    )
    nombre = models.CharField(max_length=200)
    numero_nucleos_gpu = models.IntegerField()
    tamano_vram = models.IntegerField()
    frecuencia_gpu = models.DecimalField(decimal_places=6, max_digits=15)


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    codigo_solicitud = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    estado_solicitud = models.CharField(max_length=100)
    posicion_cola = models.IntegerField()
    fecha_finalizada = models.DateTimeField()
    parametros_ejecucion = models.TextField(blank=False)
    fecha_procesamiento = models.DateTimeField()
    id_recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, null=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Archivo(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    ruta = models.CharField(max_length=200)
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=False)
