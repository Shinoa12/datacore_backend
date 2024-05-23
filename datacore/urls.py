from django.urls import path,include
from rest_framework import routers
from datacore import views
from .views import LoginWithGoogle
from rest_framework_simplejwt.views import TokenVerifyView

router = routers.DefaultRouter()
router.register(r'facultades',views.FacultadViewSet , 'facultades')
router.register(r'especialidades',views.EspecialidadViewSet , 'especialidades')
router.register(r'estadosPersonas',views.EstadoPersonaViewSet , 'estadosPersonas')

urlpatterns = [
    path('api/v1/',include(router.urls)),
    path('api/v1/especialidades/porFacultad/<int:id_facultad>/', views.EspecialidadViewSet.as_view({'get': 'getEspecialidadesPorFacultad'}), name='especialidadesPorFacultad'),
    path('api/v1/login-with-google/', LoginWithGoogle.as_view(), name = 'login-with-google'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
    
