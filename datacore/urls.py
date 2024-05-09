from django.urls import path,include
from rest_framework import routers
from datacore import views

router = routers.DefaultRouter()
router.register(r'facultades',views.FacultadViewSet , 'facultades')
router.register(r'especialidades',views.EspecialidadViewSet , 'especialidades')
router.register(r'estadosPersonas',views.EstadoPersonaViewSet , 'estadosPersonas')
router.register(r'cpus',views.CPUViewSet , 'cpus')
router.register(r'gpus',views.GPUViewSet , 'gpus')
router.register(r'users',views.UsersViewSet , 'users')

urlpatterns = [
    path('api/v1/',include(router.urls)),
    path('api/v1/especialidades/porFacultad/<int:id_facultad>/', views.EspecialidadViewSet.as_view({'get': 'getEspecialidadesPorFacultad'}), name='especialidadesPorFacultad'),
]
    
