from rest_framework import viewsets
from rest_framework.response import Response
from .models import Facultad , Especialidad , EstadoPersona , CPU , GPU
from .serializer import FacultadSerializer , EspecialidadSerializer , EstadoPersonaSerializer , CPUSerializer , GPUSerializer

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

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer
    



