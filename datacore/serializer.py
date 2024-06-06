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

class UserSSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ['id_recurso', 'tamano_ram']

class SolicitudDetalleSerializer(serializers.ModelSerializer):
    recurso = RecursoSerializer(read_only=True)
    nombre = serializers.SerializerMethodField()
    numero_nucleos = serializers.SerializerMethodField()
    frecuencia = serializers.SerializerMethodField()
    tamano_ram = serializers.SerializerMethodField()

    class Meta:
        model = Solicitud
        fields = ['id_solicitud', 'fecha_registro', 'estado_solicitud', 'nombre', 'numero_nucleos', 'frecuencia', 'tamano_ram','recurso']

    def get_nombre(self, obj):
        try:
            cpu = CPU.objects.filter(id_recurso=obj.id_recurso).exists()
            if cpu:
                return CPU.objects.get(id_recurso=obj.id_recurso).nombre
            else:
                return GPU.objects.get(id_recurso=obj.id_recurso).nombre
        except (CPU.DoesNotExist, GPU.DoesNotExist):
            return None

    def get_numero_nucleos(self, obj):
        try:
            cpu = CPU.objects.filter(id_recurso=obj.id_recurso).exists()
            if cpu:
                return CPU.objects.get(id_recurso=obj.id_recurso).numero_nucleos_cpu
            else:
                return GPU.objects.get(id_recurso=obj.id_recurso).numero_nucleos_gpu
        except (CPU.DoesNotExist, GPU.DoesNotExist):
            return None

    def get_frecuencia(self, obj):
        try:
            cpu = CPU.objects.filter(id_recurso=obj.id_recurso).exists()
            if cpu:
                return CPU.objects.get(id_recurso=obj.id_recurso).frecuencia_cpu
            else:
                return GPU.objects.get(id_recurso=obj.id_recurso).frecuencia_gpu
        except (CPU.DoesNotExist, GPU.DoesNotExist):
            return None

    def get_tamano_ram(self, obj):
        try:
            return Recurso.objects.get(id_recurso=obj.id_recurso.id_recurso).tamano_ram
        except Recurso.DoesNotExist:
            return None

class SolicitudesSerializer(serializers.ModelSerializer):
    recurso = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    duracion = serializers.SerializerMethodField()
    cancelar = serializers.SerializerMethodField()
    detalle = serializers.SerializerMethodField()
    resultados = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = Solicitud
        fields = [
            'id','id_solicitud', 'duracion', 'fecha_registro', 'fecha_procesamiento', 
            'fecha_finalizada', 'estado_solicitud', 'cancelar', 'detalle', 
            'resultados', 'recurso', 'email'
        ]

    def get_id(self, obj):
        return obj.id_solicitud
    def get_cancelar(self, obj):
        return ""

    def get_detalle(self, obj):
        return ""

    def get_resultados(self, obj):
        return ""
    
    def get_duracion(self, obj):
        duracion = obj.fecha_finalizada - obj.fecha_procesamiento
        return str(duracion)

    def get_recurso(self, obj):
        try:
            cpu = CPU.objects.filter(id_recurso=obj.id_recurso).exists()
            if cpu:
                return "CPU"
            else:
                return "GPU"
        except CPU.DoesNotExist:
            return None

    def get_email(self, obj):
        try:
            user = User.objects.get(id=obj.id_user.id)
            return user.email
        except User.DoesNotExist:
            return None