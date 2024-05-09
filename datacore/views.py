from rest_framework import viewsets
from rest_framework.response import Response
from .models import Facultad , Especialidad , EstadoPersona
from .serializer import FacultadSerializer , EspecialidadSerializer , EstadoPersonaSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.permissions import AllowAny
# Create your views here.

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
    
class VerifyTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            UntypedToken(token)
            return Response(status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [AllowAny]

