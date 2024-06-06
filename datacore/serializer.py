from rest_framework import serializers
from .models import Facultad, Especialidad, EstadoPersona, CPU, GPU, Recurso, User , Solicitud , Archivo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime

class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = "__all__"

class CreateSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id_recurso', 'id_user', 'parametros_ejecucion', 'archivos']

    archivos = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )

    def create(self, validated_data):
        archivos = validated_data.pop('archivos')
        posicion_cola_obtenida = self.context.get('posicion_cola_obtenida')
        solicitud = Solicitud.objects.create(
            id_recurso=validated_data['id_recurso'],
            id_user=validated_data['id_user'],
            parametros_ejecucion=validated_data['parametros_ejecucion'],
            codigo_solicitud="ABD",
            fecha_registro=datetime.now(),
            estado_solicitud="creada",
            posicion_cola=posicion_cola_obtenida,
            fecha_finalizada=datetime(1, 1, 1),
            fecha_procesamiento=datetime(1, 1, 1)
        )
        for archivo in archivos:
            archivo_ruta = f'archivos/{archivo.name}'
            
            Archivo.objects.create(
                ruta=archivo_ruta,
                id_solicitud=solicitud
            )
        return solicitud

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = "__all__"

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = "__all__"


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = "__all__"


class EstadoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPersona
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

    def update(self, instance, validated_data):
        recurso_data = validated_data.pop("id_recurso", None)

        if recurso_data:
            for attr, value in recurso_data.items():
                setattr(instance.id_recurso, attr, value)
            instance.id_recurso.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class GPUSerializer(serializers.ModelSerializer):
    id_recurso = RecursoSerializer()

    class Meta:
        model = GPU
        fields = "__all__"

    def create(self, validated_data):
        recurso_data = validated_data.pop("id_recurso")
        recurso_instance = Recurso.objects.create(**recurso_data)
        gpu_instance = GPU.objects.create(id_recurso=recurso_instance, **validated_data)
        return gpu_instance

    def update(self, instance, validated_data):
        recurso_data = validated_data.pop("id_recurso", None)

        if recurso_data:
            for attr, value in recurso_data.items():
                setattr(instance.id_recurso, attr, value)
            instance.id_recurso.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Añadir claim personalizado
        token['is_admin'] = user.groups.filter(name='ADMIN').exists()

        return token
    

class CPUResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ['nombre', 'numero_nucleos_cpu', 'frecuencia_cpu']

class GPUResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ['nombre', 'numero_nucleos_gpu', 'tamano_vram', 'frecuencia_gpu']

class SolicitudesSerializer(serializers.ModelSerializer):
    recurso_cpu = serializers.SerializerMethodField()
    recurso_gpu = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Solicitud
        fields = [
            'id_solicitud', 'codigo_solicitud', 'fecha_registro', 'estado_solicitud', 
            'posicion_cola', 'fecha_finalizada', 'parametros_ejecucion', 
            'fecha_procesamiento', 'id_recurso', 'id_user', 'recurso_cpu', 'recurso_gpu', 'user'
        ]

    def get_recurso_cpu(self, obj):
        try:
            cpu = CPU.objects.get(id_recurso=obj.id_recurso)
            return CPUResourceSerializer(cpu).data
        except CPU.DoesNotExist:
            return None

    def get_recurso_gpu(self, obj):
        try:
            gpu = GPU.objects.get(id_recurso=obj.id_recurso)
            return GPUResourceSerializer(gpu).data
        except GPU.DoesNotExist:
            return None
    
    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.id_user)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None