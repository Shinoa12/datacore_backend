from rest_framework import serializers
from .models import Facultad, Especialidad, EstadoPersona, CPU, GPU, Recurso, User


class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = "__all__"


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = "__all__"


class EstadoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPersona
        fields = "__all__"


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = "__all__"


class CPUSerializer(serializers.ModelSerializer):
    id_recurso = RecursoSerializer()

    class Meta:
        model = CPU
        fields = "__all__"

    def create(self, validated_data):
        recurso_data = validated_data.pop("id_recurso")
        recurso_instance = Recurso.objects.create(**recurso_data)
        cpu_instance = CPU.objects.create(id_recurso=recurso_instance, **validated_data)
        return cpu_instance


class GPUSerializer(serializers.ModelSerializer):
    id_recurso = RecursoSerializer()

    class Meta:
        model = GPU
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
