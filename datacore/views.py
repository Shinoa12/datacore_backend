from rest_framework import viewsets
from django.db import transaction
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
import logging
from datetime import datetime
from .models import Facultad, Especialidad, EstadoPersona, CPU, GPU, User , Solicitud , Archivo , Recurso
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

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer

    def descargar(self, request, id_solicitud):
        archivos = self.queryset.filter(id_solicitud_id=id_solicitud)
        serializer = self.get_serializer(archivos, many=True)
        return Response(serializer.data)


class SolicitudViewSet(viewsets.ModelViewSet) : 
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def list_por_usuario(self, request, id_user):
        solicitudes = self.queryset.filter(id_user_id=id_user)
        serializer = SolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    
    def detalle_solicitud(self, request, id_solicitud):
        solicitud = self.queryset.get(id_solicitud=id_solicitud)
        return Response(SolicitudDetalleSerializer(solicitud).data)

    def create(self, request):
        data = request.data
        
        # Extraer los parámetros
        id_user = data.get('id_user')
        id_recurso = data.get('id_recurso')
        parametros_ejecucion = data.get('parametros_ejecucion')
        

        
        # Crear la instancia de Solicitud
        solicitud = Solicitud.objects.create(
            id_recurso_id=id_recurso,
            id_user_id=id_user,
            parametros_ejecucion=parametros_ejecucion,
            codigo_solicitud="ABD",
            fecha_registro=datetime.now(),
            estado_solicitud="creada",
            posicion_cola=1,
            fecha_finalizada=datetime(1, 1, 1),
            fecha_procesamiento=datetime(1, 1, 1),
        )
        
        # Serializa y devuelve la respuesta
        response_serializer = SolicitudSerializer(solicitud)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
class HistorialViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudesSerializer


    
@api_view(['DELETE'])
@transaction.atomic
def deleteSolicitud(request, id_solicitud):
    if request.method == 'DELETE':
        try:
            solicitud = Solicitud.objects.get(id_solicitud=id_solicitud)
            solicitud.estado_solicitud = "cancelada"
            solicitud.save()
            return Response(SolicitudSerializer(solicitud).data)
        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitud not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@transaction.atomic
def crear_solicitud(request):
    if request.method == 'POST':
        id_recurso = request.data.get('id_recurso')

        # Ensure 'id_recurso' is provided
        if not id_recurso:
            return Response({'error': 'id_recurso is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            posicionColaObtenida = encolar_solicitud(id_recurso)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        solicitud_serializer = CreateSolicitudSerializer(data=request.data, context={'posicion_cola_obtenida': posicionColaObtenida})

        if solicitud_serializer.is_valid():
            solicitud = solicitud_serializer.save()                
            return Response(CreateSolicitudSerializer(solicitud).data, status=status.HTTP_201_CREATED)
        
        return Response(solicitud_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@transaction.atomic
def encolar_solicitud(id_recurso):
    # Obtener el recurso por su ID
    recurso = get_object_or_404(Recurso, pk=id_recurso)
    
    # Incrementar el contador de solicitudes encoladas de manera atómica
    recurso.solicitudes_encoladas = F('solicitudes_encoladas') + 1
    recurso.save(update_fields=['solicitudes_encoladas'])
    
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
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Obtener valores predeterminados específicos por sus IDs
        default_estado_persona = EstadoPersona.objects.get(nombre="Pendiente")
        default_especialidad = Especialidad.objects.get(nombre="INFORMATICA")
        default_facultad = Facultad.objects.get(nombre="CIENCIA E INGENIERIA")
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
    return user


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

                user = authenticate_or_create_user(user_email, first_name, last_name)
                token = AccessToken.for_user(user)
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access_token': str(token), 
                    'username': user_email, 
                    'refresh_token': str(refresh), 
                    'first_name': first_name, 
                    'last_name': last_name,
                    'is_admin': user.groups.filter(name='ADMIN').exists(),
                    'estado':user.id_estado_persona.id_estado_persona,
                    'id_user':user.id
                })
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
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
