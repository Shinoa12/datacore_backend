from rest_framework import serializers
from .models import  Facultad , Especialidad , EstadoPersona 


class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'

class EstadoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPersona
        fields = '__all__'



