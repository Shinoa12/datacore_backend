from django.db import models
from datetime import date
#from django.contrib.auth.models import AbstractUser

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(max_length=100)
    foundation = models.PositiveIntegerField()

class Facultad(models.Model):
    id_facultad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    id_facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

# Aqui estaba tratando de exterder la clase auth_user
#class CustomUser(AbstractUser):
#    authorize_flag = models.BooleanField(default=False)
#    motivo = models.CharField(max_length=500)   
#    fecha_registro = models.DateTimeField(default=date.today)
#    recursos_max = models.IntegerField(default=1)
#    id_facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)
#    id_especialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE)
#    id_rol = models.ForeignKey(Rol,on_delete=models.CASCADE)


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)   
    username = models.CharField(max_length=200)   
    email = models.CharField(max_length=200)   
    authorize_flag = models.BooleanField(default=False)
    motivo = models.CharField(max_length=500)   
    fecha_registro = models.DateTimeField(default=date.today)
    recursos_max = models.IntegerField(default=1)
    id_facultad = models.ForeignKey(Facultad,on_delete=models.CASCADE)
    id_especialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol,on_delete=models.CASCADE)