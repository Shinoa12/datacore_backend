from rest_framework import viewsets
from rest_framework.response import Response
from .models import Facultad , Especialidad , EstadoPersona , User 
from .serializer import FacultadSerializer , EspecialidadSerializer , EstadoPersonaSerializer
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
import logging
# Create your views here.

# Configurar el logger
logger = logging.getLogger(__name__)
class FacultadViewSet(viewsets.ModelViewSet):
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer


class EstadoPersonaViewSet(viewsets.ModelViewSet):
    queryset = EstadoPersona.objects.all()
    serializer_class = EstadoPersonaSerializer


class EspecialidadViewSet(viewsets.ModelViewSet) : 
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

    #Metodo que lista todas las especialidades de una facultad
    def getEspecialidadesPorFacultad(self, request, id_facultad):
        especialidades = self.queryset.filter(id_facultad_id = id_facultad)
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)
    

def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token

def authenticate_or_create_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Obtener valores predeterminados específicos por sus IDs
        default_estado_persona = EstadoPersona.objects.get(id_estado_persona=1)
        default_especialidad = Especialidad.objects.get(id_especialidad=1)
        user = User.objects.create_user(
            username=email,
            email=email,
            id_estado_persona=default_estado_persona,
            id_especialidad=default_especialidad
        )
    return user

class LoginWithGoogle(APIView):
    def post(self, request):
        try:
            if 'code' in request.data.keys():
                code = request.data['code']
                id_token = get_id_token_with_code_method_2(code)
                if id_token is None:
                    return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
                
                user_email = id_token['email']
                first_name = id_token.get('given_name', '')
                last_name = id_token.get('family_name', '')

                user = authenticate_or_create_user(user_email)
                token = AccessToken.for_user(user)
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access_token': str(token), 
                    'username': user_email, 
                    'refresh_token': str(refresh), 
                    'first_name': first_name, 
                    'last_name': last_name
                })
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error in LoginWithGoogle: %s", e, exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)