from rest_framework import viewsets
from django.db import transaction, models
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import get_id_token_with_code_method_1, get_id_token_with_code_method_2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from datacore.permissions import IsAdmin, IsUser
from django.contrib.auth.models import Group
from .utils import enviar_email
from django.conf import settings
import os
key_path = os.path.join(settings.BASE_DIR, 'key/linux-key.pem')
import logging

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import paramiko
from scp import SCPClient
from io import BytesIO
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models.functions import ExtractMonth
from django.db.models import F,Count,Avg,DurationField, ExpressionWrapper

from datetime import datetime
from .models import (
    Facultad,
    Especialidad,
    EstadoPersona,
    CPU,
    GPU,
    User,
    Solicitud,
    Archivo,
    Recurso,
    Herramienta,
    Libreria,
    Ajustes,
)
from .serializer import (
    FacultadSerializer,
    EspecialidadSerializer,
    EstadoPersonaSerializer,
    CPUSerializer,
    GPUSerializer,
    UserSerializer,
    SolicitudSerializer,
    ArchivoSerializer,
    CreateSolicitudSerializer,
    SolicitudesSerializer,
    SolicitudDetalleSerializer,
    HerramientaSerializer,
    LibreriaSerializer,
    AjustesSerializer,
)


class FacultadViewSet(viewsets.ModelViewSet):
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer


class EstadoPersonaViewSet(viewsets.ModelViewSet):
    queryset = EstadoPersona.objects.all()
    serializer_class = EstadoPersonaSerializer


class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

    # Método que lista todas las especialidades de una facultad
    def list_por_facultad(self, request, id_facultad):
        especialidades = self.queryset.filter(id_facultad_id=id_facultad)
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)


class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer

    @action(detail=True, methods=["get"])
    def librerias(self, request, pk=None):
        libs = Libreria.objects.filter(herramienta=pk)
        serializer = LibreriaSerializer(libs, many=True)
        return Response(serializer.data)


class LibreriaViewSet(viewsets.ModelViewSet):
    queryset = Libreria.objects.all()
    serializer_class = LibreriaSerializer


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def herramientas(self, request, pk=None):
        cpu = self.get_object()
        herramientas = cpu.id_recurso.herramientas.all()
        serializer = HerramientaSerializer(herramientas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def habilitados(self, request):
        cpus = CPU.objects.filter(id_recurso__estado=True)
        serializer = self.get_serializer(cpus, many=True)
        return Response(serializer.data)


class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def herramientas(self, request, pk=None):
        gpu = self.get_object()
        herramientas = gpu.id_recurso.herramientas.all()
        serializer = HerramientaSerializer(herramientas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def habilitados(self, request):
        gpus = GPU.objects.filter(id_recurso__estado=True)
        serializer = self.get_serializer(gpus, many=True)
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def validos(self, request):
        users = User.objects.exclude(id_estado_persona=1)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def desautorizados(self, request):
        users = User.objects.filter(id_estado_persona=1)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer

    def descargar(self, request, id_solicitud):
        archivos = self.queryset.filter(id_solicitud_id=id_solicitud)
        serializer = self.get_serializer(archivos, many=True)
        return Response(serializer.data)


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def list_por_usuario(self, request, id_user):
        solicitudes = self.queryset.filter(id_user_id=id_user).order_by(
            "-fecha_registro"
        )
        serializer = SolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def detalle_solicitud(self, request, id_solicitud):
        solicitud = self.queryset.get(id_solicitud=id_solicitud)
        return Response(SolicitudDetalleSerializer(solicitud).data)


class HistorialViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all().order_by("-fecha_registro")
    serializer_class = SolicitudesSerializer


@api_view(["DELETE"])
@transaction.atomic
def cancelarSolicitud(request, id_solicitud):
    if request.method == "DELETE":

        try:
            solicitud = Solicitud.objects.get(id_solicitud=id_solicitud)
            solicitud.estado_solicitud = "Cancelada"
            # Descolar del recurso
            desencolar_solicitud(solicitud)

            # Enviar correo una vez la solicitud ha sido cancelada
            enviar_email(
                "DATACORE-SOLICITUD CANCELADA",
                solicitud.id_user_id,
                "Su solicitud ha sido cancelada.",
            )

            return Response(SolicitudSerializer(solicitud).data)

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "Solicitud no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def download_and_send_to_ec2(solicitud):

    recurso = get_object_or_404(Recurso, pk=solicitud.id_recurso_id)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(recurso.direccion_ip, username=recurso.user, key_filename= key_path) #Conectar a EC2 requiere ip , username y key

    with SCPClient(ssh.get_transport()) as scp:
        archivos = Archivo.objects.filter(id_solicitud=solicitud.id_solicitud)
        for archivo in archivos:
            obj = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=archivo.ruta)
            file_stream = BytesIO(obj['Body'].read())
            scp.putfo(file_stream, f'/home/{archivo.ruta.split("/")[-1]}')

@api_view(["POST"])
def inicioProcesamientoSolicitud(request, id_solicitud):
    if request.method == "POST":

        try:
            solicitud = Solicitud.objects.get(id_solicitud=id_solicitud)
            solicitud.estado_solicitud = "En proceso"
            solicitud.fecha_procesamiento = datetime.now
            solicitud.save
            #Descarga de archivos de S3 
            download_and_send_to_ec2(solicitud)
            # Enviar correo una vez la solicitud ha sido cancelada
            enviar_email(
                "DATACORE-SOLICITUD EN PROCESO",
                solicitud.id_user_id,
                "Su solicitud {solicitud.id_solicitud} se encuentra en la posición 1 y ha iniciado su procesamiento",
            )

            return Response(1)

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "Solicitud no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["POST"])
@transaction.atomic
def finProcesamientoSolicitud(request):
    
        try:
            if request.method == "POST":
                id_solicitud = request.data.get("id_solicitud")

            solicitud = Solicitud.objects.get(id_solicitud=id_solicitud)
            solicitud.estado_solicitud = "Finalizada"
            solicitud.fecha_finalizada = datetime.now
            # Descolar del recurso
            desencolar_solicitud(solicitud)

            # SUBIR A S3 LOS ARCHIVOS ENVIADOS EN EL REQUEST QUE ESTAN EN UN ZIP
            zip_file = request.FILES['zip_file']
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            s3_key = f"archivos/{solicitud.id_solicitud}/{zip_file.name}"
            s3_client.upload_fileobj(zip_file, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
            s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"

            # Guardar el enlace en la base de datos en la tabla Archivo
            Archivo.objects.create(
                    ruta=s3_url,
                    id_solicitud=solicitud
            )

            # Enviar correo una vez la solicitud ha sido cancelada
            enviar_email(
                "DATACORE-SOLICITUD CANCELADA",
                solicitud.id_user_id,
                "Su solicitud ha sido cancelada.",
            )

            return Response(SolicitudSerializer(solicitud).data)

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "Solicitud no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
@transaction.atomic
def crear_solicitud(request):
    if request.method == "POST":
        id_recurso = request.data.get("id_recurso")

        if not id_recurso:
            return Response(
                {"error": "id_recurso is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            posicionColaObtenida = encolar_solicitud(id_recurso)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        solicitud_serializer = CreateSolicitudSerializer(
            data=request.data, context={"posicion_cola_obtenida": posicionColaObtenida}
        )

        if solicitud_serializer.is_valid():
            solicitud = solicitud_serializer.save()
            return Response(
                CreateSolicitudSerializer(solicitud).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(solicitud_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@transaction.atomic
def encolar_solicitud(id_recurso):
    # Obtener el recurso por su ID
    recurso = get_object_or_404(Recurso, pk=id_recurso)

    # Incrementar el contador de solicitudes encoladas de manera atómica
    recurso.solicitudes_encoladas = F("solicitudes_encoladas") + 1
    recurso.save(update_fields=["solicitudes_encoladas"])

    # Refrescar el objeto recurso para obtener el valor actualizado del campo
    recurso.refresh_from_db()

    return recurso.solicitudes_encoladas


@transaction.atomic
def desencolar_solicitud(solicitud):
    # Obtener el recurso por su ID
    recurso = get_object_or_404(Recurso, pk=solicitud.id_recurso_id)

    posicion_original = solicitud.posicion_cola
    solicitud.estado_solicitud = "Cancelada"
    solicitud.posicion_cola = 0
    solicitud.save()

    # Actualizar posiciones de otras solicitudes
    Solicitud.objects.filter(
        id_recurso=solicitud.id_recurso_id, posicion_cola__gt=posicion_original
    ).update(posicion_cola=models.F("posicion_cola") - 1)

    # Incrementar el contador de solicitudes encoladas de manera atómica
    recurso.solicitudes_encoladas = F("solicitudes_encoladas") - 1
    recurso.save(update_fields=["solicitudes_encoladas"])

    # Refrescar el objeto recurso para obtener el valor actualizado del campo
    recurso.refresh_from_db()

    return recurso.solicitudes_encoladas


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


def authenticate_or_create_user(email, fname, lname):
    is_new_user = False
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Obtener valores predeterminados específicos por sus IDs
        default_estado_persona = EstadoPersona.objects.get(nombre="PENDIENTE")
        default_especialidad = Especialidad.objects.get(nombre="INFORMATICA")
        default_facultad = Facultad.objects.get(nombre="CIENCIAS E INGENIERIA")
        user = User.objects.create_user(
            username=email,
            email=email,
            id_estado_persona=default_estado_persona,
            id_especialidad=default_especialidad,
            id_facultad=default_facultad,
            first_name=fname,
            last_name=lname,
        )
        default_group = Group.objects.get(name="USER")
        user.groups.add(default_group)
        is_new_user = True
    return user, is_new_user


class LoginWithGoogle(APIView):
    def post(self, request):
        try:
            if "code" in request.data.keys():
                code = request.data["code"]
                id_token = get_id_token_with_code_method_2(code)
                if id_token is None:
                    return Response(
                        {"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
                    )

                user_email = id_token["email"]
                first_name = id_token.get("given_name", "")
                last_name = id_token.get("family_name", "")

                user, is_new_user = authenticate_or_create_user(
                    user_email, first_name, last_name
                )
                token = AccessToken.for_user(user)
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "access_token": str(token),
                        "username": user_email,
                        "refresh_token": str(refresh),
                        "first_name": first_name,
                        "last_name": last_name,
                        "is_admin": user.groups.filter(name="ADMIN").exists(),
                        "estado": user.id_estado_persona.id_estado_persona,
                        "id_user": user.id,
                        "is_new_user": is_new_user,
                    }
                )
            return Response(
                {"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Hello, admin!"})


class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "Hello, user!"})


@api_view(["POST"])
def enviar_email_view(request):
    try:
        asunto = request.data.get("asunto")
        id_user = request.data.get("id_user")
        mensaje = request.data.get("mensaje")

        if not asunto or not id_user or not mensaje:
            return Response(
                {"error": "Todos los campos son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        enviar_email(asunto, id_user, mensaje)
        return Response(
            {"message": "Correo enviado exitosamente."}, status=status.HTTP_200_OK
        )

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AjustesViewSet(viewsets.ModelViewSet):
    queryset = Ajustes.objects.all()
    serializer_class = AjustesSerializer

    @action(detail=False, methods=["get"], url_path="codigo/(?P<codigo>\w+)")
    def get_by_code(self, request, codigo=None):
        try:
            ajuste = self.queryset.get(codigo=codigo)
            serializer = self.serializer_class(ajuste)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ajustes.DoesNotExist:
            return Response(
                {"error": f"Ajuste '{codigo}' no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["put"], url_path="actualizar-varios")
    def bulk_update(self, request):
        data = request.data

        try:
            for item in data:
                id = item.get("id")
                ajuste = self.queryset.get(id=id)
                serializer = self.serializer_class(ajuste, data=item)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response(
                {"message": "Tabla actualizada correctamente"},
                status=status.HTTP_200_OK,
            )
        except Ajustes.DoesNotExist:
            return Response(
                {"error": "Uno o más de los ajustes no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def requests_by_month(request):
    data = Solicitud.objects.annotate(month=ExtractMonth('fecha_registro')).values('month').annotate(count=Count('id_solicitud')).order_by('month')
    return Response(data)

@api_view(['GET'])
def requests_by_resource(request):
    cpu_count = CPU.objects.annotate(count=Count('id_recurso')).count()
    gpu_count = GPU.objects.annotate(count=Count('id_recurso')).count()
    return Response({'CPU': cpu_count, 'GPU': gpu_count})

@api_view(['GET'])
def requests_by_specialty(request):
    data = Especialidad.objects.annotate(count=Count('user__solicitud')).values('nombre', 'count')
    return Response(data)


@api_view(['GET'])
def average_processing_duration(request):
    data = Solicitud.objects.annotate(
        processing_duration=ExpressionWrapper(
            F('fecha_finalizada') - F('fecha_procesamiento'),
            output_field=DurationField()
        )
    ).aggregate(
        avg_duration=Avg('processing_duration')
    )
    return Response(data)
@api_view(['GET'])
def solicitudes_creadas(request):
    count = Solicitud.objects.filter(estado_solicitud="Creada").count()
    return Response({"count": count})

@api_view(['GET'])
def solicitudes_en_proceso(request):
    count = Solicitud.objects.filter(estado_solicitud="En Proceso").count()
    return Response({"count": count})

@api_view(['GET'])
def solicitudes_finalizadas(request):
    count = Solicitud.objects.filter(estado_solicitud="Cancelada").count()
    return Response({"count": count})
